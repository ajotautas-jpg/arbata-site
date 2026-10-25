/* El. pašto formos: siunčia į /subscribe.php be perkrovimo; be JS veikia kaip įprasta forma. */
(function () {
  var forms = document.querySelectorAll('form[data-subscribe]');
  Array.prototype.forEach.call(forms, function (form) {
    form.addEventListener('submit', function (e) {
      if (!window.fetch || !window.FormData) return;
      e.preventDefault();
      var msg = form.querySelector('.form-msg');
      var btn = form.querySelector('button[type=submit]');
      if (btn) btn.disabled = true;
      fetch(form.getAttribute('action'), {
        method: 'POST',
        body: new FormData(form),
        headers: { 'Accept': 'application/json' }
      }).then(function (r) {
        return r.json().then(function (j) { return { ok: r.ok && j && j.ok }; }, function () { return { ok: false }; });
      }).then(function (res) {
        if (res.ok) {
          if (msg) { msg.textContent = form.getAttribute('data-ok'); }
          if (window.arbataTrack) window.arbataTrack('newsletter');
          form.reset();
        } else if (msg) {
          msg.textContent = form.getAttribute('data-err');
        }
      }).catch(function () {
        if (msg) msg.textContent = form.getAttribute('data-err');
      }).then(function () {
        if (btn) btn.disabled = false;
      });
    });
  });
})();
