// Keep the current section when opening the other language of the same page.
(function () {
  function updateLanguageLinks() {
    document.querySelectorAll('[data-language-link]').forEach(function (link) {
      var target = new URL(link.getAttribute('href'), window.location.href);
      target.hash = window.location.hash;
      link.href = target.href;
    });
  }
  updateLanguageLinks();
  window.addEventListener('hashchange', updateLanguageLinks);
})();
