/**
 * EasyTech Site CAPTCHA — Turnstile en todo el sitio.
 * Montar en formularios: <div data-site-captcha></div>
 * API: window.EasyTechSiteCaptcha
 */
(function () {
  "use strict";

  var turnstilePromise = null;

  function config() {
    return window.EASYTECH_SITE_CAPTCHA_CONFIG || {};
  }

  function isEnabled() {
    var c = config();
    return !!(c.required && c.siteKey && c.provider === "turnstile");
  }

  function loadTurnstile() {
    if (window.turnstile) return Promise.resolve();
    if (turnstilePromise) return turnstilePromise;
    turnstilePromise = new Promise(function (resolve, reject) {
      var existing = document.querySelector('script[src*="turnstile/v0/api.js"]');
      if (existing) {
        existing.addEventListener("load", function () {
          resolve();
        });
        if (window.turnstile) resolve();
        return;
      }
      var s = document.createElement("script");
      s.src = "https://challenges.cloudflare.com/turnstile/v0/api.js";
      s.async = true;
      s.defer = true;
      s.onload = function () {
        resolve();
      };
      s.onerror = function () {
        turnstilePromise = null;
        reject(new Error("turnstile_load_failed"));
      };
      document.head.appendChild(s);
    });
    return turnstilePromise;
  }

  function mountEl(el) {
    if (!el || el.dataset.captchaReady === "1") return Promise.resolve(el);
    if (!isEnabled()) {
      el.dataset.captchaReady = "1";
      el.hidden = true;
      return Promise.resolve(el);
    }

    var c = config();
    return loadTurnstile().then(function () {
      if (!window.turnstile || el.dataset.captchaReady === "1") return el;
      el.dataset.captchaReady = "1";
      el.classList.add("site-captcha");
      el.innerHTML = "";

      var renderOpts = {
        sitekey: c.siteKey,
        theme: c.theme || "light",
        language: c.language || "es",
        callback: function () {
          el.dataset.captchaPassed = "1";
          el.dispatchEvent(new CustomEvent("easytech:captcha-success", { bubbles: true }));
        },
        "expired-callback": function () {
          el.dataset.captchaPassed = "0";
          el.dispatchEvent(new CustomEvent("easytech:captcha-expired", { bubbles: true }));
        },
        "error-callback": function () {
          el.dataset.captchaPassed = "0";
          el.dispatchEvent(new CustomEvent("easytech:captcha-error", { bubbles: true }));
        },
      };
      if (el.dataset.captchaSize === "compact" || el.classList.contains("booking-captcha")) {
        renderOpts.size = "compact";
      }

      var widgetId = window.turnstile.render(el, renderOpts);

      el.dataset.captchaWidgetId = String(widgetId);
      return el;
    });
  }

  function getToken(el) {
    if (!el || !isEnabled()) return "";
    var widgetId = el.dataset.captchaWidgetId;
    if (widgetId == null || !window.turnstile) return "";
    return window.turnstile.getResponse(Number(widgetId)) || window.turnstile.getResponse(widgetId) || "";
  }

  function reset(el) {
    if (!el || el.dataset.captchaWidgetId == null || !window.turnstile) return;
    var widgetId = el.dataset.captchaWidgetId;
    window.turnstile.reset(Number(widgetId));
    el.dataset.captchaPassed = "0";
  }

  function validate(el) {
    if (!isEnabled()) return { ok: true, token: "" };
    if (!el) return { ok: false, message: "Falta verificación de seguridad." };
    var token = getToken(el);
    if (!token) {
      return {
        ok: false,
        message: "Completá la verificación de seguridad (captcha) antes de continuar.",
      };
    }
    return { ok: true, token: token };
  }

  function boot(root) {
    var scope = root && root.querySelectorAll ? root : document;
    var mounts = scope.querySelectorAll("[data-site-captcha]");
    var jobs = [];
    mounts.forEach(function (el) {
      jobs.push(mountEl(el));
    });
    return Promise.all(jobs);
  }

  window.EasyTechSiteCaptcha = {
    config: config,
    isEnabled: isEnabled,
    boot: boot,
    mount: mountEl,
    getToken: getToken,
    reset: reset,
    validate: validate,
  };

  function autoBoot() {
    boot(document).catch(function () {
      /* Turnstile blocked — forms show error on submit */
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", autoBoot);
  } else {
    autoBoot();
  }
})();
