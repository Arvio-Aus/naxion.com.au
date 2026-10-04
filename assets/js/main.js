/* Naxion site script — no dependencies. */
(function () {
  "use strict";

  var PRODUCTS = window.NAXION_PRODUCTS || [];
  var $ = function (sel, root) { return (root || document).querySelector(sel); };
  var $$ = function (sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); };

  function esc(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  /* ------------------------------------------------------------ Nav */
  var toggle = $(".nav-toggle");
  var links = $(".nav-links");
  if (toggle && links) {
    toggle.addEventListener("click", function () {
      var open = links.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }
  $$("[data-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); });

  /* ------------------------------------------------------------ Product cards */
  function card(p) {
    var specs = p.highlights.slice(0, 4).map(function (h) {
      return "<div><span>" + esc(h[0]) + "</span><strong>" + esc(h[1]) + "</strong></div>";
    }).join("");
    return (
      '<a class="product-card reveal" href="product.html?id=' + encodeURIComponent(p.id) + '">' +
        '<div class="media"><span class="badge">' + (p.type === "cell" ? "Cell" : "Pack") + "</span>" +
          '<img src="' + esc(p.image) + '" alt="' + esc(p.name + " " + p.title) + '" loading="lazy" width="480" height="400"></div>' +
        '<div class="body"><span class="model">' + esc(p.name) + "</span>" +
          "<h3>" + esc(p.title) + "</h3><p>" + esc(p.tagline) + "</p>" +
          '<div class="mini-specs">' + specs + "</div></div></a>"
    );
  }

  $$("[data-product-grid]").forEach(function (grid) {
    var mode = grid.getAttribute("data-product-grid"); // "featured" | "all"
    var filterBar = $("[data-filter]");
    var params = new URLSearchParams(location.search);
    var current = params.get("type") || "all";

    function draw() {
      var list = PRODUCTS.filter(function (p) {
        if (mode === "featured") return p.featured;
        return current === "all" || p.type === current;
      });
      grid.innerHTML = list.length ? list.map(card).join("") : '<p class="empty">No products found.</p>';
      observe(grid);
    }

    if (filterBar && mode !== "featured") {
      $$(".chip", filterBar).forEach(function (chip) {
        chip.setAttribute("aria-pressed", chip.dataset.type === current ? "true" : "false");
        chip.addEventListener("click", function () {
          current = chip.dataset.type;
          $$(".chip", filterBar).forEach(function (c) { c.setAttribute("aria-pressed", c === chip ? "true" : "false"); });
          var url = new URL(location.href);
          if (current === "all") url.searchParams.delete("type"); else url.searchParams.set("type", current);
          history.replaceState(null, "", url);
          draw();
        });
      });
    }
    draw();
  });

  /* ------------------------------------------------------------ Product detail */
  var detail = $("[data-product-detail]");
  if (detail) {
    var id = new URLSearchParams(location.search).get("id");
    var p = PRODUCTS.filter(function (x) { return x.id === id; })[0];
    if (!p) {
      detail.innerHTML = '<div class="empty"><h2>Product not found</h2><p>That product may have moved.</p><a class="btn btn-ghost" href="products.html">Browse all products</a></div>';
    } else {
      renderDetail(p);
    }
  }

  function renderDetail(p) {
    var typeLabel = p.type === "cell" ? "Cells" : "Battery packs";
    document.title = p.name + " " + p.title + " | Naxion";
    var md = $('meta[name="description"]');
    if (md) md.setAttribute("content", p.name + ": " + p.tagline);

    var images = [p.image].concat(p.gallery || []);
    var thumbs = images.length > 1
      ? '<div class="pd-thumbs">' + images.map(function (src, i) {
          return '<button type="button" data-src="' + esc(src) + '" aria-current="' + (i === 0) + '" aria-label="View image ' + (i + 1) + '"><img src="' + esc(src) + '" alt=""></button>';
        }).join("") + "</div>"
      : "";

    var highlights = p.highlights.map(function (h) {
      return "<div><span>" + esc(h[0]) + "</span><strong>" + esc(h[1]) + "</strong></div>";
    }).join("");
    var tags = (p.applications || []).map(function (a) { return "<li>" + esc(a) + "</li>"; }).join("");
    var groups = p.specs.map(function (g) {
      return '<div class="spec-group"><h3>' + esc(g[0]) + "</h3><table><tbody>" +
        g[1].map(function (r) { return "<tr><th scope=\"row\">" + esc(r[0]) + "</th><td>" + esc(r[1]) + "</td></tr>"; }).join("") +
        "</tbody></table></div>";
    }).join("");

    detail.innerHTML =
      '<section class="page-hero" style="padding-bottom:24px"><div class="container">' +
        '<nav class="breadcrumb" aria-label="Breadcrumb"><a href="index.html">Home</a> / <a href="products.html?type=' + p.type + '">' + typeLabel + "</a> / " + esc(p.name) + "</nav>" +
        '<div class="pd">' +
          '<div class="pd-gallery"><div class="pd-main"><img id="pd-img" src="' + esc(p.image) + '" alt="' + esc(p.name + " " + p.title) + '" width="480" height="400"></div>' + thumbs + "</div>" +
          '<div class="pd-info"><span class="model">' + esc(p.name) + " · " + esc(p.format) + "</span>" +
            "<h1>" + esc(p.title) + '</h1><p class="lead">' + esc(p.description) + "</p>" +
            '<div class="highlights">' + highlights + "</div>" +
            (tags ? '<ul class="tags" aria-label="Applications">' + tags + "</ul>" : "") +
            '<div class="btn-row">' +
              '<a class="btn btn-primary" href="contact.html?product=' + encodeURIComponent(p.name) + '">Enquire about ' + esc(p.name) + ' <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 5l7 7-7 7"/></svg></a>' +
              '<a class="btn btn-ghost" href="contact.html?product=' + encodeURIComponent(p.name) + '&amp;need=Datasheet">Request datasheet</a>' +
            "</div></div></div></div></section>" +
      '<section style="padding-top:24px"><div class="container">' +
        '<div class="section-head"><div><span class="eyebrow">Specifications</span><h2>' + esc(p.name) + " technical data</h2></div></div>" +
        '<div class="spec-groups">' + groups + "</div>" +
        (p.tempCurve ? chartCard(p) : "") +
        '<p class="note">Specifications are typical values and may change without notice. Contact us for the latest datasheet.</p>' +
      "</div></section>";

    $$(".pd-thumbs button", detail).forEach(function (b) {
      b.addEventListener("click", function () {
        $("#pd-img").src = b.dataset.src;
        $$(".pd-thumbs button", detail).forEach(function (x) { x.setAttribute("aria-current", x === b ? "true" : "false"); });
      });
    });
    bindChart();
  }

  /* Capacity retention vs temperature — single series, bars by test temperature. */
  function chartCard(p) {
    var data = p.tempCurve;
    var W = 640, H = 260, m = { t: 24, r: 8, b: 36, l: 40 };
    var iw = W - m.l - m.r, ih = H - m.t - m.b;
    var step = iw / data.length, bw = Math.min(44, step * 0.56);
    var y = function (v) { return m.t + ih - (v / 100) * ih; };
    var grid = [0, 25, 50, 75, 100].map(function (v) {
      return '<line class="grid" x1="' + m.l + '" x2="' + (W - m.r) + '" y1="' + y(v) + '" y2="' + y(v) + '"/>' +
        '<text x="' + (m.l - 8) + '" y="' + (y(v) + 4) + '" text-anchor="end">' + v + "%</text>";
    }).join("");
    var bars = data.map(function (d, i) {
      var cx = m.l + step * i + step / 2, top = y(d[1]), h = m.t + ih - top, r = 4;
      var cls = d[0] < 0 ? "bar cold" : "bar";
      var path = "M" + (cx - bw / 2) + "," + (m.t + ih) + "V" + (top + r) + "q0,-" + r + " " + r + ",-" + r + "H" + (cx + bw / 2 - r) + "q" + r + ",0 " + r + "," + r + "V" + (m.t + ih) + "Z";
      return '<g data-tip="' + d[0] + ' °C: ' + d[1] + '% of rated capacity">' +
        '<rect class="hit" x="' + (m.l + step * i) + '" y="' + m.t + '" width="' + step + '" height="' + ih + '"/>' +
        '<path class="' + cls + '" d="' + path + '"/>' +
        '<text class="val" x="' + cx + '" y="' + (top - 8) + '" text-anchor="middle">' + d[1] + "%</text>" +
        '<text x="' + cx + '" y="' + (H - 12) + '" text-anchor="middle">' + d[0] + " °C</text></g>";
    }).join("");
    return '<div class="chart-card"><h3>Discharge capacity vs temperature</h3>' +
      '<p class="sub">Capacity retained at 0.5C discharge, as % of rated capacity at 25 °C.</p>' +
      '<svg class="temp-chart" viewBox="0 0 ' + W + " " + H + '" role="img" aria-label="Discharge capacity by temperature: ' +
        data.map(function (d) { return d[0] + " °C " + d[1] + "%"; }).join(", ") + '">' + grid +
        '<line class="axis" x1="' + m.l + '" x2="' + (W - m.r) + '" y1="' + (m.t + ih) + '" y2="' + (m.t + ih) + '"/>' + bars + "</svg>" +
      '<div class="chart-legend"><span class="cold">Below 0 °C</span><span>0 °C and above</span></div></div>';
  }

  function bindChart() {
    var tip;
    $$(".temp-chart g[data-tip]").forEach(function (g) {
      g.addEventListener("mousemove", function (e) {
        if (!tip) { tip = document.createElement("div"); tip.className = "chart-tip"; document.body.appendChild(tip); }
        tip.textContent = g.getAttribute("data-tip");
        tip.style.left = e.clientX + 14 + "px";
        tip.style.top = e.clientY - 36 + "px";
        tip.style.opacity = "1";
      });
      g.addEventListener("mouseleave", function () { if (tip) tip.style.opacity = "0"; });
    });
  }

  /* ------------------------------------------------------------ Contact form (Web3Forms) */
  var form = $("#enquiry-form");
  if (form) {
    var sel = $("#product", form);
    if (sel) {
      ["cell", "pack"].forEach(function (t) {
        var og = document.createElement("optgroup");
        og.label = t === "cell" ? "Cells" : "Battery packs";
        PRODUCTS.filter(function (p) { return p.type === t; }).forEach(function (p) {
          var o = document.createElement("option");
          o.value = p.name;
          o.textContent = p.name + " — " + p.title;
          og.appendChild(o);
        });
        sel.appendChild(og);
      });
      var q = new URLSearchParams(location.search);
      if (q.get("product")) sel.value = q.get("product");
      var need = q.get("need");
      if (need) $$('input[name="interest"]', form).forEach(function (c) { if (c.value === need) c.checked = true; });
    }

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var status = $(".form-status", form);
      var btn = $('button[type="submit"]', form);
      var data = new FormData(form);
      if (String(data.get("access_key")).indexOf("YOUR_") === 0) {
        status.className = "form-status err";
        status.textContent = "The form isn't connected yet: add your Web3Forms access key in contact.html.";
        return;
      }
      var interests = data.getAll("interest");
      data.delete("interest");
      data.set("interest", interests.join(", ") || "Not specified");
      var topic = data.get("product") || (interests.indexOf("UltraCap") > -1 ? "UltraCap" : "General");
      data.set("subject", "Naxion enquiry: " + topic + " (" + (data.get("company") || data.get("name")) + ")");

      btn.disabled = true;
      var label = btn.innerHTML;
      btn.textContent = "Sending…";
      status.className = "form-status";

      fetch("https://api.web3forms.com/submit", {
        method: "POST",
        headers: { "Content-Type": "application/json", Accept: "application/json" },
        body: JSON.stringify(Object.fromEntries(data)),
      })
        .then(function (r) { return r.json(); })
        .then(function (res) {
          if (res.success) {
            form.reset();
            status.className = "form-status ok";
            status.textContent = "Thanks, your enquiry has been sent. We'll be in touch shortly.";
          } else {
            throw new Error(res.message || "Submission failed");
          }
        })
        .catch(function (err) {
          status.className = "form-status err";
          status.textContent = "Sorry, something went wrong (" + err.message + "). Please try again.";
        })
        .finally(function () { btn.disabled = false; btn.innerHTML = label; });
    });
  }

  /* ------------------------------------------------------------ Reveal on scroll */
  var io = "IntersectionObserver" in window
    ? new IntersectionObserver(function (entries) {
        entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); } });
      }, { rootMargin: "0px 0px -8% 0px" })
    : null;
  function observe(root) {
    $$(".reveal", root).forEach(function (el) { if (io) io.observe(el); else el.classList.add("in"); });
  }
  observe(document);
})();
