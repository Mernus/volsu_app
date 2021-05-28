$(document).ready(function () {
  $("#btn")[0].onclick = function () {
    if ($(window).width() < 950) {
      return;
    }
    $(".sidebar")[0].classList.toggle("active");
    if ($("#btn")[0].classList.contains("bx-menu")) {
      $("#btn")[0].classList.replace("bx-menu", "bx-menu-alt-right");
      $(".profile_details")[0].style.opacity = 1;
    } else {
      $("#btn")[0].classList.replace("bx-menu-alt-right", "bx-menu")
      $(".profile_details")[0].style.opacity = 0;
    }
  }

  function resize() {
    if ($(window).width() < 950) {
      $(".sidebar")[0].classList.remove("active");
      $(".profile_details")[0].style.opacity = 0;
      if ($("#btn")[0].classList.contains("bx-menu-alt-right")) {
        $("#btn")[0].classList.replace("bx-menu-alt-right", "bx-menu")
      }
    }
  }

  $(window).on("resize", resize);
  resize(); // call on init
});
