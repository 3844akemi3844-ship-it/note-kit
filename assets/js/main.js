// 画面に入った要素をふわっと表示（控えめなスクロール演出）
(function () {
  var targets = document.querySelectorAll(
    '.hero__head, .hero__title, .hero__lead, .hero__photo, .hero__cta, ' +
    '.title-rule, .checklist, .label-rule, .point, .title-sides, .after__card, ' +
    '.script--center, .title-bar, .title-bar__sub, .menu__card, ' +
    '.therapist__body, .closing__title, .closing__text, .closing__actions'
  );
  if (!('IntersectionObserver' in window) || !targets.length) return;
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  Array.prototype.forEach.call(targets, function (el) { el.classList.add('reveal'); });

  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (!entry.isIntersecting) return;
      entry.target.classList.add('is-visible');
      io.unobserve(entry.target);
    });
  }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });

  Array.prototype.forEach.call(targets, function (el) { io.observe(el); });
})();
