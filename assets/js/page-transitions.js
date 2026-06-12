(function () {
  if (!window.fetch || !window.history.replaceState) return;
  if (window.location.protocol === "file:") return;

  var prefersReduced =
    window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function sameBasename(a, b) {
    var fa = (a.split("/").pop() || "index.html").replace(/^\//, "");
    var fb = (b.split("/").pop() || "index.html").replace(/^\//, "");
    if (fa === "" || fa === "/") fa = "index.html";
    if (fb === "" || fb === "/") fb = "index.html";
    return fa === fb;
  }

  function loadAndSwap(urlStr, isPop) {
    var fullUrl = new URL(urlStr, window.location.href);
    var fetchPath = fullUrl.pathname + fullUrl.search;

    return fetch(fetchPath, { credentials: "same-origin" })
      .then(function (r) {
        if (!r.ok) throw new Error("fetch failed");
        return r.text();
      })
      .then(function (html) {
        var doc = new DOMParser().parseFromString(html, "text/html");
        var newMain = doc.querySelector("#page-main");
        var cur = document.querySelector("#page-main");
        if (!newMain || !cur) {
          window.location.href = fullUrl.href;
          return;
        }

        var swap = function () {
          cur.innerHTML = newMain.innerHTML;
          var t = doc.querySelector("title");
          if (t) document.title = t.textContent || document.title;
          if (doc.body && doc.body.className.trim()) {
            document.body.className = doc.body.className;
          }
          if (!isPop) {
            history.pushState({ spa: 1 }, "", fullUrl.pathname + fullUrl.search + fullUrl.hash);
          }
          window.scrollTo(0, 0);
          if (fullUrl.hash) {
            requestAnimationFrame(function () {
              var el = document.querySelector(fullUrl.hash);
              if (el) el.scrollIntoView({ behavior: prefersReduced ? "auto" : "smooth", block: "start" });
            });
          }
          document.body.classList.remove("is-page-loading");
          if (typeof window.reinitPage === "function") window.reinitPage();
        };

        document.body.classList.add("is-page-loading");

        if (!prefersReduced && document.startViewTransition) {
          document.startViewTransition(swap);
        } else {
          swap();
        }
      })
      .catch(function () {
        document.body.classList.remove("is-page-loading");
        window.location.href = urlStr;
      });
  }

  document.addEventListener("click", function (e) {
    var a = e.target.closest("a[href]");
    if (!a) return;
    if (a.target === "_blank" || a.getAttribute("download")) return;
    if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    if (a.hasAttribute("data-no-spa")) return;

    var href = a.getAttribute("href");
    if (!href || href.startsWith("mailto:") || href.startsWith("tel:") || href.startsWith("javascript:"))
      return;

    var url;
    try {
      url = new URL(href, window.location.href);
    } catch (err) {
      return;
    }

    if (url.origin !== window.location.origin) return;

    var path = url.pathname;
    if (!/\.html$/i.test(path) && path !== "/" && path !== "") return;

    if (sameBasename(url.pathname, window.location.pathname) && url.hash) {
      e.preventDefault();
      var target = document.querySelector(url.hash);
      if (target) {
        target.scrollIntoView({ behavior: prefersReduced ? "auto" : "smooth", block: "start" });
        history.pushState({ spa: 1 }, "", url.pathname + url.search + url.hash);
      }
      return;
    }

    if (sameBasename(url.pathname, window.location.pathname) && !url.hash) return;

    e.preventDefault();
    loadAndSwap(url.pathname + url.search + url.hash, false);
  });

  window.addEventListener("popstate", function () {
    loadAndSwap(
      window.location.pathname + window.location.search + window.location.hash,
      true
    );
  });
})();
