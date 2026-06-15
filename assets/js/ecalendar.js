/**
 * ECalendar — UI pública de reservas (agenda.html).
 * Consume API EN1 cuando mockMode es false.
 */
(function () {
  "use strict";

  var MONTHS = [
    "enero", "febrero", "marzo", "abril", "mayo", "junio",
    "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre",
  ];
  var WEEKDAYS = ["Do", "Lu", "Ma", "Mi", "Ju", "Vi", "Sa"];

  function cfg() {
    return window.EASYTECH_ECALENDAR_CONFIG || {};
  }

  function products() {
    return window.EASYTECH_ECALENDAR_PRODUCTS || [];
  }

  function apiBase() {
    var c = cfg();
    if (c.apiBase) return c.apiBase.replace(/\/$/, "");
    var portal = window.EASYTECH_PORTAL_URLS || {};
    if (portal.ecalendarApiBase) return portal.ecalendarApiBase.replace(/\/$/, "");
    return "";
  }

  function pad(n) {
    return n < 10 ? "0" + n : String(n);
  }

  function toDateStr(d) {
    return d.getFullYear() + "-" + pad(d.getMonth() + 1) + "-" + pad(d.getDate());
  }

  function startOfDayMs(d) {
    return new Date(d.getFullYear(), d.getMonth(), d.getDate()).getTime();
  }

  function todayMs() {
    return startOfDayMs(new Date());
  }

  function maxSelectableMs() {
    var max = new Date();
    max.setDate(max.getDate() + (cfg().horizonDays || 30));
    return startOfDayMs(max);
  }

  function canGoPrevMonth(viewMonth) {
    var now = new Date();
    return (
      viewMonth.getFullYear() > now.getFullYear() ||
      (viewMonth.getFullYear() === now.getFullYear() && viewMonth.getMonth() > now.getMonth())
    );
  }

  function isFutureMonth(viewMonth) {
    var now = new Date();
    return (
      viewMonth.getFullYear() > now.getFullYear() ||
      (viewMonth.getFullYear() === now.getFullYear() && viewMonth.getMonth() > now.getMonth())
    );
  }

  function isSelectableDay(dObj) {
    var ms = startOfDayMs(dObj);
    return ms >= todayMs() && ms <= maxSelectableMs() && isWeekday(dObj);
  }

  function parseDateStr(s) {
    var p = s.split("-");
    return new Date(Number(p[0]), Number(p[1]) - 1, Number(p[2]));
  }

  function isWeekday(d) {
    var day = d.getDay();
    return day >= 1 && day <= 5;
  }

  function timeToMinutes(t) {
    var p = t.split(":");
    return Number(p[0]) * 60 + Number(p[1]);
  }

  function minutesToTime(m) {
    return pad(Math.floor(m / 60)) + ":" + pad(m % 60);
  }

  function getQueryProduct() {
    try {
      return new URLSearchParams(window.location.search).get("product") || "";
    } catch (e) {
      return "";
    }
  }

  function mockBusySlot(dateStr, time) {
    var h = 0;
    var i;
    var seed = dateStr + time;
    for (i = 0; i < seed.length; i++) h = (h * 31 + seed.charCodeAt(i)) % 997;
    return h % 7 === 0;
  }

  function effectiveLeadTimeHours() {
    var c = cfg();
    if (c.mockMode && c.mockLeadTimeHours != null) return c.mockLeadTimeHours;
    return c.leadTimeHours != null ? c.leadTimeHours : 4;
  }

  function generateMockSlots(dateStr, durationMin) {
    var c = cfg();
    var wh = c.workingHours || {};
    var start = timeToMinutes(wh.start || "09:00");
    var end = timeToMinutes(wh.end || "17:00");
    var step = durationMin;
    var d = parseDateStr(dateStr);
    var now = new Date();
    var leadMs = effectiveLeadTimeHours() * 3600000;
    var slots = [];
    var t;

    if (!isWeekday(d)) return slots;
    if (startOfDayMs(d) < todayMs()) return slots;

    for (t = start; t + durationMin <= end; t += step) {
      var time = minutesToTime(t);
      var slotStart = new Date(d.getFullYear(), d.getMonth(), d.getDate(), Math.floor(t / 60), t % 60);
      var available = slotStart.getTime() >= now.getTime() + leadMs;
      if (available && mockBusySlot(dateStr, time)) available = false;
      slots.push({ time: time, available: available });
    }
    return slots;
  }

  function normalizeSlots(data) {
    if (!data) return [];
    if (Array.isArray(data.slots) && data.slots.length && typeof data.slots[0] === "object") {
      return data.slots;
    }
    if (Array.isArray(data.slots)) {
      var all = generateMockSlots(data.date, data.slot_duration_minutes || cfg().defaultDurationMinutes || 30);
      var set = {};
      data.slots.forEach(function (t) {
        set[t] = true;
      });
      if (!cfg().showUnavailableSlots) {
        return data.slots.map(function (t) {
          return { time: t, available: true };
        });
      }
      return all.map(function (slot) {
        return { time: slot.time, available: !!set[slot.time] };
      });
    }
    return [];
  }

  function fetchAvailability(dateStr, durationMin) {
    if (cfg().mockMode || !apiBase()) {
      return Promise.resolve({
        date: dateStr,
        timezone: cfg().timezone || "America/Panama",
        slot_duration_minutes: durationMin,
        slots: generateMockSlots(dateStr, durationMin),
      });
    }
    var url =
      apiBase() +
      "/availability?date=" +
      encodeURIComponent(dateStr) +
      "&duration=" +
      encodeURIComponent(String(durationMin));
    return fetch(url, { credentials: "omit" })
      .then(function (r) {
        if (!r.ok) throw new Error("availability_error");
        return r.json();
      })
      .then(function (data) {
        return {
          date: data.date,
          timezone: data.timezone,
          slot_duration_minutes: data.slot_duration_minutes || durationMin,
          slots: normalizeSlots(data),
        };
      });
  }

  function submitBooking(payload) {
    if (cfg().mockMode || !apiBase()) {
      return Promise.resolve({
        ok: true,
        mock: true,
        booking_id: "mock-" + Date.now(),
      });
    }
    return fetch(apiBase() + "/bookings", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "omit",
      body: JSON.stringify(payload),
    }).then(function (r) {
      return r.json().then(function (body) {
        return { ok: r.ok, status: r.status, body: body };
      });
    });
  }

  function normalizeEmail(value) {
    return (value || "").trim().toLowerCase();
  }

  function siteCaptcha() {
    return window.EasyTechSiteCaptcha || null;
  }

  function buildWhatsAppUrl(productLabel, dateStr, time) {
    var base = cfg().whatsappBase || "https://wa.me/50766884938";
    var text =
      "Reservé cita EasyTech — " +
      productLabel +
      " — " +
      dateStr +
      " " +
      time;
    return base + "?text=" + encodeURIComponent(text);
  }

  function isMobileLayout() {
    return window.matchMedia("(max-width: 640px)").matches;
  }

  function scrollMobileSection(el) {
    if (!el || !isMobileLayout()) return;
    el.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  function updateMobileProgress(root, state) {
    var nav = root.querySelector("[data-ecal-mobile-progress]");
    if (!nav) return;
    var steps = nav.querySelectorAll("[data-ecal-step]");
    var phase = "date";
    if (state.selectedDate && state.selectedTime) phase = "data";
    else if (state.selectedDate) phase = "time";

    steps.forEach(function (step) {
      var key = step.getAttribute("data-ecal-step");
      step.classList.remove("is-current", "is-done");
      if (key === phase) step.classList.add("is-current");
      else if (
        (key === "date" && (phase === "time" || phase === "data")) ||
        (key === "time" && phase === "data")
      ) {
        step.classList.add("is-done");
      }
    });
  }

  function initApp(root) {
    if (!root || root.dataset.ecalendarReady === "1") return;
    root.dataset.ecalendarReady = "1";

    var state = {
      viewMonth: new Date(),
      selectedDate: "",
      selectedTime: "",
      duration: cfg().defaultDurationMinutes || 30,
      slots: [],
      loading: false,
    };

    var els = {
      monthLabel: root.querySelector("[data-ecal-month-label]"),
      monthPrev: root.querySelector("[data-ecal-month-prev]"),
      monthNext: root.querySelector("[data-ecal-month-next]"),
      days: root.querySelector("[data-ecal-days]"),
      duration: root.querySelector("[data-ecal-duration]"),
      slots: root.querySelector("[data-ecal-slots]"),
      slotsHint: root.querySelector("[data-ecal-slots-hint]"),
      selectedTimeEl: root.querySelector("[data-ecal-selected-time]"),
      form: root.querySelector("[data-ecal-form]"),
      product: root.querySelector("#ecal-product"),
      name: root.querySelector("#ecal-name"),
      company: root.querySelector("#ecal-company"),
      email: root.querySelector("#ecal-email"),
      emailConfirm: root.querySelector("#ecal-email-confirm"),
      phone: root.querySelector("#ecal-phone"),
      message: root.querySelector("#ecal-message"),
      honeypot: root.querySelector("#ecal-website"),
      captchaMount: root.querySelector("[data-site-captcha]"),
      submit: root.querySelector("[data-ecal-submit]"),
      alert: root.querySelector("[data-ecal-alert]"),
      success: root.querySelector("[data-ecal-success]"),
      successDetail: root.querySelector("[data-ecal-success-detail]"),
      successWa: root.querySelector("[data-ecal-success-wa]"),
      panel: root.querySelector("[data-ecal-panel]"),
      slotsBlock: root.querySelector("[data-ecal-slots-block]"),
      dataBlock: root.querySelector(".booking-data"),
    };

    function showAlert(msg, type) {
      if (!els.alert) return;
      els.alert.hidden = !msg;
      els.alert.textContent = msg || "";
      els.alert.className = "ecalendar-alert" + (type ? " ecalendar-alert--" + type : "");
    }

    function populateProducts() {
      if (!els.product) return;
      var q = getQueryProduct();
      els.product.innerHTML = "";
      products().forEach(function (p) {
        var opt = document.createElement("option");
        opt.value = p.slug;
        opt.textContent = p.label;
        if (p.slug === q) opt.selected = true;
        els.product.appendChild(opt);
      });
    }

    function populateDuration() {
      if (!els.duration) return;
      var opts = cfg().durationOptions || [30, 45];
      els.duration.innerHTML = "";
      opts.forEach(function (m) {
        var opt = document.createElement("option");
        opt.value = String(m);
        opt.textContent = m + " minutos";
        if (m === state.duration) opt.selected = true;
        els.duration.appendChild(opt);
      });
    }

    function renderMonth() {
      var y = state.viewMonth.getFullYear();
      var m = state.viewMonth.getMonth();
      if (els.monthLabel) els.monthLabel.textContent = MONTHS[m] + " " + y;

      if (els.monthPrev) {
        var prevAllowed = canGoPrevMonth(state.viewMonth);
        els.monthPrev.disabled = !prevAllowed;
        els.monthPrev.setAttribute("aria-disabled", prevAllowed ? "false" : "true");
      }

      var first = new Date(y, m, 1);
      var startPad = first.getDay();
      var daysInMonth = new Date(y, m + 1, 0).getDate();
      var html = "";
      var i;

      if (state.selectedDate) {
        var sel = parseDateStr(state.selectedDate);
        if (!isSelectableDay(sel)) {
          state.selectedDate = "";
          state.selectedTime = "";
          state.slots = [];
        }
      }

      for (i = 0; i < startPad; i++) html += '<span class="ecalendar-day ecalendar-day--pad"></span>';

      for (i = 1; i <= daysInMonth; i++) {
        var dObj = new Date(y, m, i);
        var ds = toDateStr(dObj);

        if (!isSelectableDay(dObj)) {
          if (startOfDayMs(dObj) < todayMs() && !isFutureMonth(state.viewMonth)) {
            html += '<span class="ecalendar-day ecalendar-day--pad" aria-hidden="true"></span>';
          } else {
            html += '<span class="ecalendar-day ecalendar-day--disabled" aria-hidden="true">' + i + "</span>";
          }
          continue;
        }

        var cls = "ecalendar-day";
        if (ds === state.selectedDate) cls += " is-selected";
        html +=
          '<button type="button" class="' +
          cls +
          '" data-date="' +
          ds +
          '">' +
          i +
          "</button>";
      }
      if (els.days) els.days.innerHTML = html;
    }

    function updateSelectedTimeLabel() {
      if (!els.selectedTimeEl) return;
      if (state.selectedDate && state.selectedTime) {
        els.selectedTimeEl.hidden = false;
        els.selectedTimeEl.textContent =
          "Horario elegido: " + state.selectedTime + " (" + state.duration + " min)";
      } else {
        els.selectedTimeEl.hidden = true;
        els.selectedTimeEl.textContent = "";
      }
    }

    function renderSlots() {
      if (!els.slots) return;
      if (!state.selectedDate) {
        els.slots.innerHTML = "";
        if (els.slotsHint) els.slotsHint.textContent = "Elegí una fecha para ver horarios.";
        updateSelectedTimeLabel();
        return;
      }
      if (state.loading) {
        els.slots.innerHTML = '<p class="ecalendar-slots-loading">Cargando horarios…</p>';
        updateSelectedTimeLabel();
        return;
      }
      var available = state.slots.filter(function (s) {
        return s.available;
      });
      if (!state.slots.length) {
        if (els.slotsHint) els.slotsHint.textContent = "No hay horarios este día.";
        els.slots.innerHTML = "";
        updateSelectedTimeLabel();
        return;
      }
      if (!available.length) {
        if (els.slotsHint) {
          els.slotsHint.textContent =
            "No quedan horarios libres este día. Probá otro día o cambiá la duración.";
        }
        els.slots.innerHTML = "";
        state.selectedTime = "";
        updateSelectedTimeLabel();
        return;
      }
      if (els.slotsHint) {
        els.slotsHint.textContent =
          available.length +
          " horario" +
          (available.length === 1 ? "" : "s") +
          " disponible" +
          (available.length === 1 ? "" : "s");
      }
      var html = "";
      state.slots.forEach(function (slot) {
        if (!slot.available && !cfg().showUnavailableSlots) return;
        var sel = slot.time === state.selectedTime && slot.available;
        var cls = "ecalendar-slot";
        if (!slot.available) cls += " ecalendar-slot--busy";
        if (sel) cls += " is-selected";
        html +=
          '<button type="button" class="' +
          cls +
          '" data-ecal-time="' +
          slot.time +
          '"' +
          (slot.available ? "" : ' disabled aria-label="No disponible"') +
          ">" +
          (slot.available ? slot.time : "No disponible") +
          "</button>";
      });
      els.slots.innerHTML = html;
      updateSelectedTimeLabel();
      updateMobileProgress(root, state);
    }

    function loadSlots() {
      if (!state.selectedDate) return;
      state.loading = true;
      state.selectedTime = "";
      renderSlots();
      fetchAvailability(state.selectedDate, state.duration)
        .then(function (data) {
          state.slots = data.slots || [];
        })
        .catch(function () {
          state.slots = [];
          showAlert("No pudimos cargar los horarios. Intentá de nuevo o escribinos por WhatsApp.", "error");
        })
        .finally(function () {
          state.loading = false;
          renderSlots();
          scrollMobileSection(els.slotsBlock);
        });
    }

    populateProducts();
    populateDuration();
    renderMonth();
    renderSlots();
    updateMobileProgress(root, state);
    var cap = siteCaptcha();
    if (cap && els.captchaMount) cap.mount(els.captchaMount);

    root.addEventListener("click", function (e) {
      var dayBtn = e.target.closest("[data-date]");
      if (dayBtn && dayBtn.tagName === "BUTTON") {
        var picked = parseDateStr(dayBtn.getAttribute("data-date"));
        if (!isSelectableDay(picked)) return;
        state.selectedDate = dayBtn.getAttribute("data-date");
        state.selectedTime = "";
        renderMonth();
        loadSlots();
        showAlert("");
        updateMobileProgress(root, state);
        return;
      }
    });

    if (els.slots) {
      els.slots.addEventListener("click", function (e) {
        var slotBtn = e.target.closest("[data-ecal-time]");
        if (!slotBtn || slotBtn.disabled || !slotBtn.classList.contains("ecalendar-slot")) return;
        e.preventDefault();
        e.stopPropagation();
        state.selectedTime = slotBtn.getAttribute("data-ecal-time");
        renderSlots();
        showAlert("");
        updateMobileProgress(root, state);
        if (isMobileLayout()) {
          scrollMobileSection(els.dataBlock);
        } else if (els.selectedTimeEl && els.selectedTimeEl.scrollIntoView) {
          els.selectedTimeEl.scrollIntoView({ behavior: "smooth", block: "nearest" });
        }
      });
    }

    if (els.monthPrev) {
      els.monthPrev.addEventListener("click", function () {
        if (!canGoPrevMonth(state.viewMonth)) return;
        state.viewMonth = new Date(state.viewMonth.getFullYear(), state.viewMonth.getMonth() - 1, 1);
        renderMonth();
      });
    }
    if (els.monthNext) {
      els.monthNext.addEventListener("click", function () {
        state.viewMonth = new Date(state.viewMonth.getFullYear(), state.viewMonth.getMonth() + 1, 1);
        renderMonth();
      });
    }
    if (els.duration) {
      els.duration.addEventListener("change", function () {
        state.duration = Number(els.duration.value) || 30;
        loadSlots();
      });
    }

    if (els.form) {
      els.form.addEventListener("submit", function (e) {
        e.preventDefault();
        showAlert("");

        if (!state.selectedDate || !state.selectedTime) {
          showAlert("Elegí fecha y hora antes de confirmar.", "error");
          return;
        }

        if (els.honeypot && els.honeypot.value.trim()) {
          return;
        }

        var email = normalizeEmail(els.email && els.email.value);
        var emailConfirm = normalizeEmail(els.emailConfirm && els.emailConfirm.value);

        var productSlug = els.product ? els.product.value : "";
        var productLabel = productSlug;
        products().forEach(function (p) {
          if (p.slug === productSlug) productLabel = p.label;
        });

        var captchaCheck = { ok: true, token: "" };
        var capApi = siteCaptcha();
        if (capApi) captchaCheck = capApi.validate(els.captchaMount);

        var payload = {
          product_slug: productSlug,
          duration_minutes: state.duration,
          start_at: state.selectedDate + "T" + state.selectedTime + ":00-05:00",
          captcha_token: captchaCheck.token || "",
          client: {
            full_name: (els.name && els.name.value.trim()) || "",
            company: (els.company && els.company.value.trim()) || "",
            email: email,
            whatsapp: (els.phone && els.phone.value.trim()) || "",
            notes: (els.message && els.message.value.trim()) || "",
          },
        };

        if (payload.client.full_name.length < 2) {
          showAlert("Ingresá tu nombre.", "error");
          return;
        }
        if (!email || email.indexOf("@") < 1) {
          showAlert("Ingresá un correo válido.", "error");
          return;
        }
        if (!emailConfirm || emailConfirm.indexOf("@") < 1) {
          showAlert("Confirmá tu correo electrónico.", "error");
          return;
        }
        if (email !== emailConfirm) {
          showAlert("Los correos no coinciden. Revisalos e intentá de nuevo.", "error");
          return;
        }
        if (!payload.client.whatsapp) {
          showAlert("Ingresá tu teléfono o WhatsApp.", "error");
          return;
        }

        if (!captchaCheck.ok) {
          showAlert(captchaCheck.message || "Completá la verificación de seguridad.", "error");
          return;
        }

        if (els.submit) {
          els.submit.disabled = true;
          els.submit.textContent = "Confirmando…";
        }

        submitBooking(payload)
          .then(function (res) {
            if (cfg().mockMode || res.mock) {
              if (els.panel) els.panel.hidden = true;
              if (els.success) els.success.hidden = false;
              if (els.successDetail) {
                els.successDetail.textContent =
                  productLabel +
                  " · " +
                  state.selectedDate +
                  " · " +
                  state.selectedTime +
                  " (" +
                  state.duration +
                  " min). Modo demo: la reserva se confirmará cuando EN1 esté conectado.";
              }
              if (els.successWa) {
                els.successWa.href = buildWhatsAppUrl(productLabel, state.selectedDate, state.selectedTime);
              }
              return;
            }
            if (!res.ok) {
              if (res.status === 409) {
                showAlert("Ese horario ya no está disponible. Elegí otro.", "error");
                loadSlots();
                if (capApi) capApi.reset(els.captchaMount);
                return;
              }
              showAlert("No se pudo confirmar la cita. Intentá de nuevo.", "error");
              if (capApi) capApi.reset(els.captchaMount);
              return;
            }
            if (els.panel) els.panel.hidden = true;
            if (els.success) els.success.hidden = false;
            if (els.successDetail) {
              els.successDetail.textContent =
                productLabel + " · " + state.selectedDate + " · " + state.selectedTime;
            }
            if (els.successWa) {
              els.successWa.href = buildWhatsAppUrl(productLabel, state.selectedDate, state.selectedTime);
            }
          })
          .catch(function () {
            showAlert("Error de conexión. Revisá tu red o contactanos por WhatsApp.", "error");
            if (siteCaptcha()) siteCaptcha().reset(els.captchaMount);
          })
          .finally(function () {
            if (els.submit) {
              els.submit.disabled = false;
              els.submit.textContent = "Confirmar cita";
            }
          });
      });
    }
  }

  function boot() {
    document.querySelectorAll("[data-ecalendar-app]").forEach(initApp);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }

  window.initEasyTechECalendar = boot;
})();
