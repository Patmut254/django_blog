(function () {
  // ---- Hero slider ----
  var slider = document.querySelector('[data-slider]');
  if (slider) {
    var slides = slider.querySelectorAll('[data-slide]');
    var dots = slider.querySelectorAll('[data-dot]');
    var current = 0;
    var timer = null;

    function show(i) {
      if (!slides.length) return;
      current = (i + slides.length) % slides.length;
      slides.forEach(function (s, n) { s.classList.toggle('is-active', n === current); });
      dots.forEach(function (d, n) { d.classList.toggle('is-active', n === current); });
    }
    function start() {
      stop();
      if (slides.length > 1) timer = setInterval(function () { show(current + 1); }, 6000);
    }
    function stop() { if (timer) clearInterval(timer); }

    var next = slider.querySelector('[data-next]');
    var prev = slider.querySelector('[data-prev]');
    if (next) next.addEventListener('click', function () { show(current + 1); start(); });
    if (prev) prev.addEventListener('click', function () { show(current - 1); start(); });
    dots.forEach(function (d) {
      d.addEventListener('click', function () { show(+d.dataset.dot); start(); });
    });
    slider.addEventListener('mouseenter', stop);
    slider.addEventListener('mouseleave', start);

    // swipe on touch screens
    var startX = null;
    slider.addEventListener('touchstart', function (e) { startX = e.touches[0].clientX; }, { passive: true });
    slider.addEventListener('touchend', function (e) {
      if (startX === null) return;
      var dx = e.changedTouches[0].clientX - startX;
      if (Math.abs(dx) > 40) { show(current + (dx < 0 ? 1 : -1)); start(); }
      startX = null;
    });
    start();
  }

  // ---- Mobile menu ----
  var menu = document.querySelector('[data-menu]');
  document.querySelectorAll('[data-menu-toggle]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var open = menu.classList.toggle('open');
      btn.setAttribute('aria-expanded', open);
      btn.querySelector('i').className = open ? 'fa fa-times' : 'fa fa-bars';
    });
  });

  // ---- User dropdown ----
  var dropdown = document.querySelector('[data-dropdown]');
  if (dropdown) {
    var toggle = dropdown.querySelector('[data-dropdown-toggle]');
    toggle.addEventListener('click', function (e) {
      e.stopPropagation();
      var open = dropdown.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open);
    });
    document.addEventListener('click', function (e) {
      if (!dropdown.contains(e.target)) dropdown.classList.remove('open');
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') dropdown.classList.remove('open');
    });
  }

  // ---- Toast messages ----
  document.querySelectorAll('.toast-msg').forEach(function (toast) {
    var close = function () { toast.remove(); };
    toast.querySelector('[data-dismiss-toast]').addEventListener('click', close);
    setTimeout(close, 6000);
  });

  // ---- Copy link ----
  document.querySelectorAll('[data-copy]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var label = btn.querySelector('span');
      var done = function () {
        label.textContent = 'Copied!';
        setTimeout(function () { label.textContent = 'Copy link'; }, 2000);
      };
      if (navigator.clipboard) {
        navigator.clipboard.writeText(btn.dataset.copy).then(done);
      } else {
        var input = document.createElement('input');
        input.value = btn.dataset.copy;
        document.body.appendChild(input);
        input.select();
        document.execCommand('copy');
        input.remove();
        done();
      }
    });
  });
})();
