(function () {
  var prefersReduced =
    window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function markImageMissing(img) {
    var layer = img.closest(
      ".hero-stack-layer, .demo-layer, .hero-mega, .hero-product-card, .hero-laptop-bezel, .value-card"
    );
    if (layer) layer.classList.add("is-missing");
    if (img.getAttribute("alt") === "") img.setAttribute("aria-hidden", "true");
  }

  document.addEventListener(
    "error",
    function (e) {
      var t = e.target;
      if (t && t.matches && t.matches("img[data-demo-img]")) markImageMissing(t);
    },
    true
  );

  document.addEventListener(
    "load",
    function (e) {
      var t = e.target;
      if (t && t.matches && t.matches("img[data-demo-img]") && t.naturalWidth === 0) markImageMissing(t);
    },
    true
  );

  document.addEventListener("click", function (e) {
    var a = e.target.closest('a[href^="#"]');
    if (!a) return;
    if (a.hasAttribute("data-no-smooth")) return;
    var id = a.getAttribute("href");
    if (!id || id === "#") return;
    var el = document.querySelector(id);
    if (el) {
      e.preventDefault();
      el.scrollIntoView({ behavior: prefersReduced ? "auto" : "smooth", block: "start" });
    }
  });

  function bindDemoImagesIn(container) {
    var root = container || document;
    root.querySelectorAll("img[data-demo-img]").forEach(function (img) {
      if (img.complete && img.naturalWidth === 0) markImageMissing(img);
    });
  }

  /** Parámetros que Calendly usa para el iframe inline (ayuda al render completo). */
  function withCalendlyEmbedParams(url) {
    try {
      var u = new URL(url, window.location.href);
      if (!u.searchParams.has("embed_domain")) {
        u.searchParams.set("embed_domain", window.location.hostname || "localhost");
      }
      if (!u.searchParams.has("embed_type")) {
        u.searchParams.set("embed_type", "Inline");
      }
      return u.toString();
    } catch (err) {
      return url;
    }
  }

  var scheduleLoaderTimeoutId = null;

  function dismissScheduleLoader() {
    var shell = document.getElementById("schedule-shell");
    var loadingEl = document.getElementById("schedule-calendly-loading");
    if (scheduleLoaderTimeoutId) {
      clearTimeout(scheduleLoaderTimeoutId);
      scheduleLoaderTimeoutId = null;
    }
    if (shell) shell.classList.remove("schedule-shell--loading");
    if (loadingEl) loadingEl.setAttribute("aria-busy", "false");
  }

  function armScheduleLoader(shell) {
    dismissScheduleLoader();
    if (!shell) return;
    var loadingEl = document.getElementById("schedule-calendly-loading");
    shell.classList.add("schedule-shell--loading");
    if (loadingEl) loadingEl.setAttribute("aria-busy", "true");
    scheduleLoaderTimeoutId = setTimeout(function () {
      dismissScheduleLoader();
    }, 20000);
  }

  /** Calendly envía la altura real del iframe por postMessage; sin esto el área queda colapsada. */
  var calendlyPageHeightBound = false;
  function bindCalendlyPageHeightListener() {
    if (calendlyPageHeightBound) return;
    calendlyPageHeightBound = true;
    window.addEventListener("message", function (e) {
      if (e.origin !== "https://calendly.com") return;
      var d = e.data;
      if (!d || typeof d !== "object") return;
      if (d.event === "calendly.profile_page_viewed") {
        dismissScheduleLoader();
        return;
      }
      if (d.event !== "calendly.page_height" || !d.payload) return;
      var h = d.payload.height;
      if (typeof h !== "number" || h < 320) return;
      var wrap = document.getElementById("schedule-calendly-wrap");
      if (!wrap || wrap.hasAttribute("hidden")) return;
      var px = Math.ceil(h + 24);
      wrap.style.minHeight = px + "px";
      var inner = wrap.querySelector(".calendly-inline-widget");
      if (inner) inner.style.minHeight = px + "px";
      var calIframe = wrap.querySelector("iframe");
      if (calIframe) {
        calIframe.style.minHeight = Math.ceil(h) + "px";
        calIframe.style.height = Math.ceil(h) + "px";
      }
      dismissScheduleLoader();
    });
  }

  function initScheduleEmbed() {
    var shell = document.getElementById("schedule-shell");
    var iframe = document.querySelector(".schedule-iframe");
    var calWrap = document.getElementById("schedule-calendly-wrap");
    if (!shell) return;

    dismissScheduleLoader();

    if (calWrap) {
      calWrap.innerHTML = "";
      calWrap.setAttribute("hidden", "");
    }
    if (iframe) {
      iframe.src = "about:blank";
      iframe.style.display = "";
    }
    shell.classList.remove("schedule-shell--has-calendly");
    shell.classList.add("schedule-shell--fallback");

    var calUrl = (shell.getAttribute("data-calendly-url") || "").trim();
    if (
      !calUrl &&
      typeof window.EASYTECH_CALENDLY_EVENT_URL === "string" &&
      window.EASYTECH_CALENDLY_EVENT_URL.length > 0
    ) {
      calUrl = window.EASYTECH_CALENDLY_EVENT_URL.trim();
    }
    var calOk =
      calUrl.length > 0 && /^https?:\/\/(www\.)?calendly\.com\/.+/i.test(calUrl);

    function loadCalendlyScript(done) {
      var existing = document.querySelector('script[data-calendly-loader="1"]');
      if (existing) {
        if (done) done();
        return;
      }
      var s = document.createElement("script");
      s.src = "https://assets.calendly.com/assets/external/widget.js";
      s.async = true;
      s.setAttribute("data-calendly-loader", "1");
      s.onerror = function () {
        dismissScheduleLoader();
      };
      s.onload = function () {
        if (done) done();
      };
      document.body.appendChild(s);
    }

    function runCalendly() {
      if (!calWrap || !window.Calendly || typeof window.Calendly.initInlineWidget !== "function") {
        dismissScheduleLoader();
        return;
      }
      bindCalendlyPageHeightListener();
      calWrap.removeAttribute("hidden");
      shell.classList.remove("schedule-shell--fallback");
      shell.classList.add("schedule-shell--has-calendly");
      if (iframe) iframe.style.display = "none";
      calWrap.style.minHeight = "";
      try {
        window.Calendly.initInlineWidget({
          url: withCalendlyEmbedParams(calUrl),
          parentElement: calWrap,
        });
      } catch (err) {
        dismissScheduleLoader();
      }
    }

    if (calOk && calWrap) {
      armScheduleLoader(shell);
      loadCalendlyScript(function () {
        runCalendly();
      });
      return;
    }

    if (iframe) {
      var url = (iframe.getAttribute("data-schedule-src") || "").trim();
      var valid = url.length > 0 && /^https?:\/\//i.test(url);
      if (valid) {
        shell.classList.remove("schedule-shell--fallback");
        iframe.src = url;
      }
    }
  }

  var revealIo = null;

  function initRevealObserver() {
    if (revealIo) {
      revealIo.disconnect();
      revealIo = null;
    }

    var revealEls = document.querySelectorAll("#page-main .reveal:not(.reveal--instant)");

    if (prefersReduced || !("IntersectionObserver" in window)) {
      revealEls.forEach(function (el) {
        el.classList.add("is-visible");
      });
      return;
    }

    revealIo = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) entry.target.classList.add("is-visible");
        });
      },
      { threshold: 0.1, rootMargin: "0px 0px -32px 0px" }
    );
    revealEls.forEach(function (el) {
      revealIo.observe(el);
    });
  }

  function initDemoStack() {
    document.querySelectorAll(".demo-overlap[data-demo-stack]").forEach(function (container) {
      if (container.getAttribute("data-demo-stack-bound") === "1") return;
      container.setAttribute("data-demo-stack-bound", "1");

      var layers = [].slice.call(container.querySelectorAll(".demo-layer"));
      if (layers.length < 2) return;

      var prefersReduced =
        window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

      function rankOf(el) {
        return parseInt(el.getAttribute("data-stack-rank"), 10) || 0;
      }

      function reorder(clicked) {
        if (clicked.classList.contains("is-missing")) return;
        var sorted = layers.slice().sort(function (a, b) {
          return rankOf(a) - rankOf(b);
        });
        var ix = sorted.indexOf(clicked);
        if (ix < 0) return;
        if (ix === sorted.length - 1) {
          if (!prefersReduced) {
            clicked.classList.add("is-stack-pulse");
            window.setTimeout(function () {
              clicked.classList.remove("is-stack-pulse");
            }, 450);
          }
          return;
        }
        sorted.splice(ix, 1);
        sorted.push(clicked);
        sorted.forEach(function (el, i) {
          el.setAttribute("data-stack-rank", String(i));
        });
      }

      layers.forEach(function (layer) {
        layer.addEventListener("click", function () {
          reorder(layer);
        });
        layer.addEventListener("keydown", function (e) {
          if (e.key !== "Enter" && e.key !== " ") return;
          e.preventDefault();
          reorder(layer);
        });
      });
    });
  }

  function applyNavCurrent() {
    var body = document.body;
    if (!body) return;

    var key = body.getAttribute("data-nav-page");
    if (!key) {
      var map = {
        "page-home": "index",
        "page-soluciones": "soluciones",
        "page-econverso": "econverso",
        "page-easynodeone": "easynodeone",
        "page-agenda": "agenda",
        "page-contacto": "contacto",
        "page-facturacion-electronica": "facturacion-electronica",
        "page-eclassone": "eclassone",
        "page-ethesisone": "ethesisone",
        "page-eposone": "eposone",
        "page-epayroll": "epayroll",
        "page-desarrollo-software": "desarrollo-software",
        "page-consultoria-ti": "consultoria-ti",
      };
      var cls = body.className.split(/\s+/);
      for (var i = 0; i < cls.length; i++) {
        if (map[cls[i]]) {
          key = map[cls[i]];
          break;
        }
      }
    }

    if (!key) {
      var path = window.location.pathname.split("/").pop() || "index.html";
      if (!path || path === "/") key = "index";
      else key = path.replace(/\.html$/i, "") || "index";
    }

    var header = document.querySelector(".site-header");
    if (!header || key === "index") return;

    header.querySelectorAll("[aria-current]").forEach(function (el) {
      el.removeAttribute("aria-current");
    });

    header.querySelectorAll('[data-nav-match="' + key + '"]').forEach(function (el) {
      el.setAttribute("aria-current", "page");
    });
  }

  function initNavDropdowns() {
    var mq = window.matchMedia("(max-width: 900px)");

    function closeAll() {
      document.querySelectorAll("[data-dropdown].is-open").forEach(function (w) {
        w.classList.remove("is-open");
        var b = w.querySelector(".nav-dropdown-toggle");
        if (b) b.setAttribute("aria-expanded", "false");
      });
    }

    function setOpen(wrap, open) {
      var btn = wrap.querySelector(".nav-dropdown-toggle");
      if (!btn) return;
      wrap.classList.toggle("is-open", open);
      btn.setAttribute("aria-expanded", open ? "true" : "false");
    }

    document.querySelectorAll("[data-dropdown]").forEach(function (wrap) {
      var btn = wrap.querySelector(".nav-dropdown-toggle");
      if (!btn) return;
      btn.addEventListener("click", function (e) {
        if (!mq.matches) return;
        e.preventDefault();
        e.stopPropagation();
        var wasOpen = wrap.classList.contains("is-open");
        closeAll();
        if (!wasOpen) setOpen(wrap, true);
      });
    });

    document.addEventListener("click", function (e) {
      if (!mq.matches) return;
      if (!e.target.closest("[data-dropdown]")) closeAll();
    });

    document.addEventListener("keydown", function (e) {
      if (e.key !== "Escape") return;
      if (!mq.matches) return;
      closeAll();
    });

    document.querySelectorAll("[data-dropdown] a").forEach(function (a) {
      a.addEventListener("click", function () {
        if (!mq.matches) return;
        closeAll();
      });
    });

    window.addEventListener(
      "resize",
      function () {
        if (!mq.matches) closeAll();
      },
      { passive: true }
    );
  }

  function initCasesCarousel() {
    document.querySelectorAll("[data-cases-carousel]").forEach(function (root) {
      if (root.dataset.casesBound === "1") return;

      var track = root.querySelector(".home-cases-track");
      if (!track) return;

      var cards = Array.from(track.querySelectorAll(".home-case-card"));
      if (!cards.length) return;

      root.dataset.casesBound = "1";

      var setA = document.createElement("div");
      setA.className = "home-cases-set";
      var setB = document.createElement("div");
      setB.className = "home-cases-set";
      setB.setAttribute("aria-hidden", "true");

      cards.forEach(function (card) {
        setA.appendChild(card);
      });
      cards.forEach(function (card) {
        setB.appendChild(card.cloneNode(true));
      });

      track.replaceChildren(setA, setB);
      if (!prefersReduced) {
        track.classList.add("home-cases-track--loop");
      }
    });
  }

  window.reinitPage = function () {
    bindDemoImagesIn(document.getElementById("page-main"));
    initScheduleEmbed();
    initRevealObserver();
    initDemoStack();
    initCasesCarousel();
  };

  window.bootEasyTechPage = function () {
    var y = document.getElementById("y");
    if (y) y.textContent = new Date().getFullYear();

    applyNavCurrent();
    initScheduleEmbed();
    bindDemoImagesIn(document);
    initRevealObserver();
    initDemoStack();
    initNavDropdowns();
    initCasesCarousel();
  };

  window.bootEasyTechPage();
})();
