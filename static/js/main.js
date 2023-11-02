$(function () {
  function selectTheme(media) {
    $("html").attr("data-bs-theme", media.matches ? "dark" : "light");
  }

  const media = window.matchMedia('(prefers-color-scheme: dark)');
  selectTheme(media);
  media.addListener(selectTheme);
});