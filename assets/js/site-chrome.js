(function () {
  var HEADER_SLOT_ID = "site-chrome-header";
  var FOOTER_SLOT_ID = "site-chrome-footer";

  function partialUrl(name) {
    return new URL("assets/partials/" + name, window.location.href).href;
  }

  function navPageKey() {
    var body = document.body;
    if (!body) return "index";

    var map = {
      "page-home": "index",
      "page-soluciones": "soluciones",
      "page-econverso": "econverso",
      "page-easynodeone": "easynodeone",
      "page-agenda": "agenda",
      "page-contacto": "contacto",
    };

    var cls = body.className.split(/\s+/);
    for (var i = 0; i < cls.length; i++) {
      if (map[cls[i]]) return map[cls[i]];
    }

    var path = window.location.pathname.split("/").pop() || "index.html";
    if (!path || path === "/") return "index";
    return path.replace(/\.html$/i, "") || "index";
  }

  function applyNavCurrent() {
    var key = navPageKey();
    var header = document.querySelector(".site-header");
    if (!header || key === "index") return;

    header.querySelectorAll("[aria-current]").forEach(function (el) {
      el.removeAttribute("aria-current");
    });

    header.querySelectorAll('[data-nav-match="' + key + '"]').forEach(function (el) {
      el.setAttribute("aria-current", "page");
    });
  }

  function injectPartial(slot, html) {
    if (!slot || !html) return;
    slot.outerHTML = html.trim();
  }

  function loadChrome(done) {
    var headerSlot = document.getElementById(HEADER_SLOT_ID);
    var footerSlot = document.getElementById(FOOTER_SLOT_ID);

    if (!headerSlot && !footerSlot) {
      done();
      return;
    }

    if (window.location.protocol === "file:") {
      console.warn(
        "[EasyTech] Header/footer compartidos requieren servir el sitio por HTTP (ej. npx serve)."
      );
      done();
      return;
    }

    var tasks = [];

    if (headerSlot) {
      tasks.push(
        fetch(partialUrl("header.html"), { credentials: "same-origin" })
          .then(function (r) {
            if (!r.ok) throw new Error("header partial");
            return r.text();
          })
          .then(function (html) {
            injectPartial(headerSlot, html);
            applyNavCurrent();
          })
      );
    }

    if (footerSlot) {
      tasks.push(
        fetch(partialUrl("footer.html"), { credentials: "same-origin" })
          .then(function (r) {
            if (!r.ok) throw new Error("footer partial");
            return r.text();
          })
          .then(function (html) {
            injectPartial(footerSlot, html);
          })
      );
    }

    Promise.all(tasks)
      .catch(function (err) {
        console.warn("[EasyTech] No se pudo cargar header/footer compartido.", err);
      })
      .then(done);
  }

  window.__siteChromePending = true;

  function onReady() {
    loadChrome(function () {
      window.__siteChromePending = false;
      if (typeof window.bootEasyTechPage === "function") {
        window.bootEasyTechPage();
      }
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", onReady);
  } else {
    onReady();
  }
})();
