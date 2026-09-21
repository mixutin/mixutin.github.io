/* Live roadmap progress for the Dauntless Revived pages.
 *
 * Fetches the raw ROADMAP.md and counts checklist items per milestone:
 *   "- [x] **1.14 ..."  -> done, milestone 1
 *   "- [ ] **2.7 ..."   -> open, milestone 2
 * The page already lists every milestone as plain HTML, so without JavaScript
 * (or if GitHub can't be reached) readers still get the names and a link to
 * the live checklist. Text comes from data-* attributes, so the same script
 * serves the English and the Finnish page.
 */
(function () {
  "use strict";

  var list = document.querySelector("[data-roadmap-src]");
  if (!list || !window.fetch) return;

  var src = list.getAttribute("data-roadmap-src");
  var statusText = document.querySelector("[data-roadmap-text]");
  var fmtCount = list.getAttribute("data-fmt-count") || "{done} of {total} done";
  var fmtNone = list.getAttribute("data-fmt-none") || "no items yet";
  var fmtStatus = list.getAttribute("data-fmt-status") || "{done} of {total} items done.";
  var fmtError = list.getAttribute("data-fmt-error") || "Couldn't load the live checklist.";
  var ITEM = /^- \[([ xX])\] \*\*(\d+)\.\d+/;

  function fill(template, values) {
    return template.replace(/\{(\w+)\}/g, function (_, key) {
      return Object.prototype.hasOwnProperty.call(values, key) ? String(values[key]) : "";
    });
  }

  function count(markdown) {
    var counts = {};
    markdown.split(/\r?\n/).forEach(function (line) {
      var m = ITEM.exec(line);
      if (!m) return;
      var c = counts[m[2]] || (counts[m[2]] = { done: 0, open: 0 });
      if (m[1] === " ") c.open += 1;
      else c.done += 1;
    });
    return counts;
  }

  function render(counts) {
    var allDone = 0;
    var allTotal = 0;
    var rows = list.querySelectorAll("[data-milestone]");
    Array.prototype.forEach.call(rows, function (row) {
      var c = counts[row.getAttribute("data-milestone")] || { done: 0, open: 0 };
      var total = c.done + c.open;
      var pct = total ? Math.round((c.done / total) * 100) : 0;
      var label = total ? fill(fmtCount, { done: c.done, total: total, pct: pct }) : fmtNone;
      allDone += c.done;
      allTotal += total;

      var countEl = row.querySelector("[data-count]");
      if (countEl) countEl.textContent = label;

      var bar = row.querySelector(".ms-bar");
      var fillEl = bar && bar.querySelector(".ms-fill");
      if (!bar || !fillEl) return;
      var id = row.querySelector(".ms-id");
      var name = row.querySelector(".ms-name");
      bar.setAttribute("role", "progressbar");
      bar.setAttribute("aria-label", ((id ? id.textContent : "") + " " + (name ? name.textContent : "")).trim());
      bar.setAttribute("aria-valuemin", "0");
      bar.setAttribute("aria-valuemax", "100");
      bar.setAttribute("aria-valuenow", String(pct));
      bar.setAttribute("aria-valuetext", label);
      bar.removeAttribute("aria-hidden");
      window.requestAnimationFrame(function () {
        fillEl.style.width = pct + "%";
      });
    });
    list.classList.add("is-live");
    if (statusText) statusText.textContent = fill(fmtStatus, { done: allDone, total: allTotal });
  }

  var controller = window.AbortController ? new AbortController() : null;
  var timer = controller ? window.setTimeout(function () { controller.abort(); }, 10000) : null;

  fetch(src, {
    cache: "no-cache",
    credentials: "omit",
    referrerPolicy: "no-referrer",
    signal: controller ? controller.signal : undefined
  })
    .then(function (response) {
      if (!response.ok) throw new Error("HTTP " + response.status);
      return response.text();
    })
    .then(function (markdown) {
      if (timer) window.clearTimeout(timer);
      render(count(markdown));
    })
    .catch(function () {
      if (timer) window.clearTimeout(timer);
      if (statusText) statusText.textContent = fmtError;
    });
})();
