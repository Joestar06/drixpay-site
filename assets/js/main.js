/* DrixPay website v2 — shared script (no dependencies) */
(function () {
  'use strict';

  var $ = function (s, r) { return (r || document).querySelector(s); };
  var ZH = (document.documentElement.lang || '').indexOf('zh') === 0;
  var TXT = ZH ? {
    copied: '链接已复制，请在手机浏览器中打开',
    qrFail: '二维码加载失败<br>请使用下方按钮',
    mail: '正在打开邮件客户端…'
  } : {
    copied: 'Link copied. Open it in your mobile browser.',
    qrFail: 'QR code unavailable.<br>Please use the button below.',
    mail: 'Opening your email client…'
  };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  /* ---------- Toast ---------- */
  var toastEl, toastTimer;
  function toast(msg) {
    if (!toastEl) {
      toastEl = document.createElement('div');
      toastEl.className = 'toast';
      toastEl.setAttribute('role', 'status');
      document.body.appendChild(toastEl);
    }
    toastEl.textContent = msg;
    toastEl.classList.add('show');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () { toastEl.classList.remove('show'); }, 2600);
  }
  window.drixToast = toast;

  /* ---------- Header: scrolled state ---------- */
  var header = $('.site-header');
  function onScroll() { if (header) header.classList.toggle('scrolled', window.scrollY > 8); }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ---------- Mobile nav ---------- */
  var toggle = $('.nav-toggle'), mnav = $('.mobile-nav');
  if (toggle && mnav) {
    toggle.addEventListener('click', function () {
      var open = mnav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open);
      document.body.style.overflow = open ? 'hidden' : '';
    });
    $$('a', mnav).forEach(function (a) {
      a.addEventListener('click', function () {
        mnav.classList.remove('open');
        toggle.setAttribute('aria-expanded', 'false');
        document.body.style.overflow = '';
      });
    });
  }

  /* ---------- Language menu ----------
     English (root) and 简体中文 (/zh/) are live; other languages show a notice. */
  $$('.lang').forEach(function (lang) {
    var btn = $('.lang-btn', lang);
    btn.addEventListener('click', function (e) {
      e.stopPropagation();
      var open = lang.classList.toggle('open');
      btn.setAttribute('aria-expanded', open);
    });
    $$('.lang-menu [data-soon]', lang).forEach(function (b) {
      b.addEventListener('click', function () {
        lang.classList.remove('open');
        btn.setAttribute('aria-expanded', 'false');
        toast(b.getAttribute('data-soon'));
      });
    });
  });
  document.addEventListener('click', function () {
    $$('.lang.open').forEach(function (l) { l.classList.remove('open'); });
  });
  $$('.lang-select').forEach(function (sel) {
    var initial = sel.selectedIndex;
    sel.addEventListener('change', function () {
      var opt = sel.options[sel.selectedIndex];
      if (opt.getAttribute('data-soon')) {
        toast(opt.getAttribute('data-soon'));
        sel.selectedIndex = initial;
      } else if (sel.selectedIndex !== initial) {
        window.location.href = opt.value;
      }
    });
  });

  /* ---------- Reveal on scroll ---------- */
  var reveals = $$('.reveal');
  if ('IntersectionObserver' in window && reveals.length) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add('in'); });
  }

  /* ---------- Code tabs ---------- */
  $$('.code').forEach(function (code) {
    var tabs = $$('.code-tabs button', code);
    tabs.forEach(function (t) {
      t.addEventListener('click', function () {
        tabs.forEach(function (x) { x.setAttribute('aria-selected', x === t); });
        $$('.code-panel', code).forEach(function (p) { p.hidden = p.id !== t.getAttribute('aria-controls'); });
      });
    });
  });

  /* ---------- FAQ: search + category filter ---------- */
  var faqRoot = $('[data-faq]');
  if (faqRoot) {
    var input = $('.faq-search input'), chips = $$('.chips button'), empty = $('.faq-empty');
    var cat = 'all';
    function applyFaq() {
      var q = (input.value || '').trim().toLowerCase(), shown = 0;
      $$('.faq-group', faqRoot).forEach(function (g) {
        var inCat = cat === 'all' || g.getAttribute('data-cat') === cat, groupShown = 0;
        $$('.faq-item', g).forEach(function (item) {
          var hit = inCat && (!q || item.textContent.toLowerCase().indexOf(q) > -1);
          item.style.display = hit ? '' : 'none';
          if (hit) { groupShown++; if (q) item.open = true; }
        });
        g.style.display = groupShown ? '' : 'none';
        shown += groupShown;
      });
      empty.style.display = shown ? 'none' : 'block';
    }
    input.addEventListener('input', applyFaq);
    chips.forEach(function (c) {
      c.addEventListener('click', function () {
        chips.forEach(function (x) { x.setAttribute('aria-pressed', x === c); });
        cat = c.getAttribute('data-cat');
        applyFaq();
      });
    });
    if (location.hash) {
      var target = $(location.hash);
      if (target && target.tagName === 'DETAILS') target.open = true;
    }
  }

  /* ---------- Download: QR codes, copy, device detection ---------- */
  $$('[data-qr]').forEach(function (el) {
    if (window.QRCode) {
      new window.QRCode(el, { text: el.getAttribute('data-qr'), width: 252, height: 252, colorDark: '#0a0e0b', colorLight: '#ffffff', correctLevel: window.QRCode.CorrectLevel.M });
    } else {
      el.innerHTML = '<span style="font-size:12px;color:#7a857d;text-align:center">' + TXT.qrFail + '</span>';
    }
  });
  $$('[data-copy]').forEach(function (b) {
    b.addEventListener('click', function () {
      var text = b.getAttribute('data-copy');
      var done = function () { toast(TXT.copied); };
      if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(text).then(done, function () { fallbackCopy(text); done(); });
      } else { fallbackCopy(text); done(); }
    });
  });
  function fallbackCopy(text) {
    var ta = document.createElement('textarea');
    ta.value = text; ta.style.position = 'fixed'; ta.style.opacity = '0';
    document.body.appendChild(ta); ta.select();
    try { document.execCommand('copy'); } catch (e) { /* noop */ }
    document.body.removeChild(ta);
  }
  var ua = navigator.userAgent || '';
  var platform = /android/i.test(ua) ? 'android' : (/iphone|ipad|ipod/i.test(ua) ? 'ios' : null);
  if (platform) {
    var card = $('.dl-card[data-platform="' + platform + '"]');
    if (card) card.classList.add('recommended');
  }

  /* ---------- Mailto form (business inquiry) ---------- */
  $$('[data-mailto-form]').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var lines = $$('input, select, textarea', form).map(function (f) { return f.name + ': ' + (f.value || '-'); });
      var company = (form.querySelector('[data-company]') || {}).value || '';
      var href = 'mailto:' + form.getAttribute('data-mailto-form') +
        '?subject=' + encodeURIComponent(form.getAttribute('data-subject') + ' ' + company) +
        '&body=' + encodeURIComponent(lines.join('\n'));
      window.location.href = href;
      toast(TXT.mail);
    });
  });

  /* ---------- Footer year ---------- */
  $$('[data-year]').forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();
