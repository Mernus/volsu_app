$(document).ready(function () {
  $("#btn")[0].onclick = function () {
    console.log($(window).width());
    if ($(window).width() < 950) {
      return;
    }
    $(".sidebar")[0].classList.toggle("active");
    if ($("#btn")[0].classList.contains("bx-menu")) {
      $("#btn")[0].classList.replace("bx-menu", "bx-menu-alt-right");
    } else {
      $("#btn")[0].classList.replace("bx-menu-alt-right", "bx-menu");
    }
  }

  $(".bx-search")[0].onclick = function () {
    console.log($(window).width());
    if ($(window).width() < 950) {
      return;
    }
    $(".sidebar")[0].classList.toggle("active");
  }

  function resize() {
    console.log($(window).width());
    if ($(window).width() < 950) {
      $(".sidebar")[0].classList.remove("active");
      if ($("#btn")[0].classList.contains("bx-menu")) {
        $("#btn")[0].classList.replace("bx-menu", "bx-menu-alt-right");
      }
    }
  }

  $(window).on("resize", resize);
  resize(); // call on init
});
