/* ==========================================================================
   ORLANDO IV CARE — main.js
   Vanilla JavaScript. No frameworks, no dependencies.
   --------------------------------------------------------------------------
   01. Header scroll state
   02. Mobile navigation drawer
   03. Dropdown menus
   04. Scroll reveal animations
   05. FAQ accordion
   06. Services category filter
   07. Booking / contact form validation
   08. Footer year
   ========================================================================== */

(function () {
  'use strict';

  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var isDesktop = function () { return window.matchMedia('(min-width: 1025px)').matches; };

  document.addEventListener('DOMContentLoaded', function () {
    initHeaderScroll();
    initMobileNav();
    initDropdowns();
    initReveal();
    initAccordion();
    initServiceFilter();
    initForms();
    initYear();
  });


  /* ======================================================================
     01. HEADER SCROLL STATE
     ====================================================================== */
  function initHeaderScroll() {
    var header = document.querySelector('.site-header');
    if (!header) return;

    var ticking = false;
    function update() {
      header.classList.toggle('is-scrolled', window.scrollY > 12);
      ticking = false;
    }
    window.addEventListener('scroll', function () {
      if (!ticking) { window.requestAnimationFrame(update); ticking = true; }
    }, { passive: true });
    update();
  }


  /* ======================================================================
     02. MOBILE NAVIGATION DRAWER
     ====================================================================== */
  function initMobileNav() {
    var toggle = document.querySelector('.nav-toggle');
    var nav = document.getElementById('primary-nav');
    var scrim = document.querySelector('.nav-scrim');
    if (!toggle || !nav) return;

    function open() {
      document.body.classList.add('nav-open');
      toggle.setAttribute('aria-expanded', 'true');
      // Wait for the slide-in before moving focus, or iOS scrolls the page
      setTimeout(function () {
        var first = nav.querySelector('.nav__close') || nav.querySelector('a, button');
        if (first) first.focus();
      }, 120);
    }

    function close(returnFocus) {
      document.body.classList.remove('nav-open');
      toggle.setAttribute('aria-expanded', 'false');
      if (returnFocus) toggle.focus();
    }

    toggle.addEventListener('click', function () {
      if (document.body.classList.contains('nav-open')) { close(true); } else { open(); }
    });

    if (scrim) scrim.addEventListener('click', function () { close(false); });

    var closeBtn = nav.querySelector('.nav__close');
    if (closeBtn) closeBtn.addEventListener('click', function () { close(true); });

    // Tapping any real link closes the drawer (incl. same-page anchors)
    nav.addEventListener('click', function (e) {
      var link = e.target.closest('a[href]');
      if (link && !isDesktop()) close(false);
    });

    // Escape closes the drawer
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && document.body.classList.contains('nav-open')) close(true);
    });

    // Keep focus inside the drawer while it is open
    nav.addEventListener('keydown', function (e) {
      if (e.key !== 'Tab' || !document.body.classList.contains('nav-open')) return;
      var items = nav.querySelectorAll('a[href], button:not([disabled])');
      if (!items.length) return;
      var first = items[0];
      var last = items[items.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    });

    // Reset when resizing up to desktop
    window.addEventListener('resize', function () {
      if (isDesktop() && document.body.classList.contains('nav-open')) close(false);
    });
  }


  /* ======================================================================
     03. DROPDOWN MENUS  (click on all sizes, hover assist on desktop)
     ====================================================================== */
  function initDropdowns() {
    var items = document.querySelectorAll('.nav__item');

    items.forEach(function (item) {
      var btn = item.querySelector('.nav__toggle');
      if (!btn) return;

      btn.addEventListener('click', function (e) {
        e.stopPropagation();
        var willOpen = !item.classList.contains('is-open');
        closeAll();
        item.classList.toggle('is-open', willOpen);
        btn.setAttribute('aria-expanded', String(willOpen));
      });

      item.addEventListener('mouseenter', function () {
        if (!isDesktop()) return;
        closeAll();
        item.classList.add('is-open');
        btn.setAttribute('aria-expanded', 'true');
      });
      item.addEventListener('mouseleave', function () {
        if (!isDesktop()) return;
        item.classList.remove('is-open');
        btn.setAttribute('aria-expanded', 'false');
      });
    });

    function closeAll() {
      items.forEach(function (i) {
        i.classList.remove('is-open');
        var b = i.querySelector('.nav__toggle');
        if (b) b.setAttribute('aria-expanded', 'false');
      });
    }

    document.addEventListener('click', closeAll);
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeAll(); });
  }


  /* ======================================================================
     04. SCROLL REVEAL
     ====================================================================== */
  function initReveal() {
    var els = document.querySelectorAll('.reveal');
    if (!els.length) return;

    if (reduceMotion || !('IntersectionObserver' in window)) {
      els.forEach(function (el) { el.classList.add('is-visible'); });
      return;
    }

    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          io.unobserve(entry.target);
        }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });

    els.forEach(function (el) { io.observe(el); });
  }


  /* ======================================================================
     05. FAQ ACCORDION
     ====================================================================== */
  function initAccordion() {
    document.querySelectorAll('.faq__q').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var item = btn.closest('.faq__item');
        var isOpen = item.classList.contains('is-open');
        item.classList.toggle('is-open', !isOpen);
        btn.setAttribute('aria-expanded', String(!isOpen));
      });
    });
  }


  /* ======================================================================
     06. SERVICES CATEGORY FILTER
     ====================================================================== */
  function initServiceFilter() {
    var bar = document.querySelector('.filter-bar');
    var grid = document.querySelector('[data-filter-target]');
    if (!bar || !grid) return;

    var cards = Array.prototype.slice.call(grid.querySelectorAll('[data-category]'));
    var empty = document.querySelector('[data-filter-empty]');
    var count = document.querySelector('[data-filter-count]');

    bar.addEventListener('click', function (e) {
      var chip = e.target.closest('.chip');
      if (!chip) return;

      bar.querySelectorAll('.chip').forEach(function (c) { c.setAttribute('aria-pressed', 'false'); });
      chip.setAttribute('aria-pressed', 'true');

      var filter = chip.dataset.filter;
      var shown = 0;

      cards.forEach(function (card) {
        var match = filter === 'all' || card.dataset.category.split(' ').indexOf(filter) !== -1;
        card.hidden = !match;
        if (match) shown++;
      });

      if (empty) empty.hidden = shown !== 0;
      if (count) count.textContent = shown === cards.length
        ? 'Showing all ' + cards.length + ' therapies'
        : 'Showing ' + shown + ' of ' + cards.length + ' therapies';
    });
  }


  /* ======================================================================
     07. FORM VALIDATION
     --------------------------------------------------------------------
     This is a static site, so nothing is sent anywhere by default.
     To connect a real backend, replace the body of submitBooking() below
     with your own fetch() call (Formspree, Netlify Forms, your API, etc.).
     ====================================================================== */

  /* >>> EDIT ME: hook your booking backend up here <<< */
  function submitBooking(data) {
    // Example with Formspree:
    //   return fetch('https://formspree.io/f/XXXXXXX', {
    //     method: 'POST',
    //     headers: { 'Accept': 'application/json', 'Content-Type': 'application/json' },
    //     body: JSON.stringify(data)
    //   }).then(function (r) { if (!r.ok) throw new Error('Request failed'); });
    console.log('Booking request (demo only — not sent anywhere):', data);
    return new Promise(function (resolve) { setTimeout(resolve, 900); });
  }

  var VALIDATORS = {
    required: function (v) { return v.trim() !== '' || 'This field is required.'; },
    email: function (v) { return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v.trim()) || 'Enter a valid email address, e.g. name@example.com'; },
    tel: function (v) {
      var digits = v.replace(/\D/g, '');
      return (digits.length >= 10 && digits.length <= 15) || 'Enter a valid phone number with area code.';
    },
    name: function (v) { return v.trim().length >= 2 || 'Please enter your full name.'; }
  };

  function validateField(field) {
    var input = field.querySelector('input, select, textarea');
    if (!input) return true;

    var errorEl = field.querySelector('.field__error');
    var value = input.value || '';
    var message = '';

    if (input.required && VALIDATORS.required(value) !== true) {
      message = 'This field is required.';
    } else if (value.trim() !== '') {
      var rule = input.dataset.validate;
      if (rule && VALIDATORS[rule]) {
        var result = VALIDATORS[rule](value);
        if (result !== true) message = result;
      }
    }

    field.classList.toggle('has-error', !!message);
    input.setAttribute('aria-invalid', message ? 'true' : 'false');
    if (errorEl) errorEl.textContent = message;
    return !message;
  }

  function initForms() {
    document.querySelectorAll('form[data-validate-form]').forEach(function (form) {
      var fields = Array.prototype.slice.call(form.querySelectorAll('.field'));
      var status = form.querySelector('.form-status');
      var summary = form.querySelector('.form-summary');
      var submitBtn = form.querySelector('[type="submit"]');

      // Validate on blur, never on every keystroke
      fields.forEach(function (field) {
        var input = field.querySelector('input, select, textarea');
        if (!input) return;
        input.addEventListener('blur', function () { validateField(field); });
        input.addEventListener('input', function () {
          if (field.classList.contains('has-error')) validateField(field);
        });
      });

      form.addEventListener('submit', function (e) {
        e.preventDefault();

        var invalid = fields.filter(function (f) { return !validateField(f); });

        if (invalid.length) {
          if (summary) {
            summary.textContent = invalid.length === 1
              ? 'Please correct 1 field below before sending your request.'
              : 'Please correct ' + invalid.length + ' fields below before sending your request.';
            summary.classList.add('is-visible');
          }
          if (status) status.classList.remove('is-visible');
          var firstInput = invalid[0].querySelector('input, select, textarea');
          if (firstInput) firstInput.focus();
          return;
        }

        if (summary) summary.classList.remove('is-visible');

        var data = {};
        new FormData(form).forEach(function (value, key) { data[key] = value; });

        if (submitBtn) {
          submitBtn.classList.add('is-loading');
          submitBtn.setAttribute('aria-busy', 'true');
        }

        submitBooking(data)
          .then(function () {
            form.reset();
            if (status) {
              status.classList.add('is-visible');
              status.setAttribute('tabindex', '-1');
              status.focus();
            }
          })
          .catch(function () {
            if (summary) {
              summary.textContent = 'Something went wrong sending your request. Please try again, or call us instead.';
              summary.classList.add('is-visible');
            }
          })
          .finally(function () {
            if (submitBtn) {
              submitBtn.classList.remove('is-loading');
              submitBtn.removeAttribute('aria-busy');
            }
          });
      });
    });
  }


  /* ======================================================================
     08. FOOTER YEAR
     ====================================================================== */
  function initYear() {
    document.querySelectorAll('[data-year]').forEach(function (el) {
      el.textContent = new Date().getFullYear();
    });
  }


  /* ======================================================================
     UTILITIES
     ====================================================================== */
  function throttle(fn, wait) {
    var last = 0, timer = null;
    return function () {
      var now = Date.now();
      var args = arguments;
      if (now - last >= wait) { last = now; fn.apply(null, args); }
      else if (!timer) {
        timer = setTimeout(function () { timer = null; last = Date.now(); fn.apply(null, args); }, wait - (now - last));
      }
    };
  }
})();
