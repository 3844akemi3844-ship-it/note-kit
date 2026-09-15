// 画面に入った要素をふわっと表示（控えめなスクロール演出）
(function () {
  var targets = document.querySelectorAll(
    '.hero__inner > *, .worry__body, .message__text, .feature, .after__card, ' +
    '.range__text, .range__figure, .voice__card, .menu__card, .therapist__body, ' +
    '.faq__item, .closing__title, .closing__text, .closing__actions'
  );
  if (!('IntersectionObserver' in window) || !targets.length) return;

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
