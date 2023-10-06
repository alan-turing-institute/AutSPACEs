$(function () {
  above = false;
  menu = $("#content-bar")
  // Determine at which viewport height the menu should move to the top
  threshold = menu.position().top + menu.height() + 100

  // Moves the menu to the top or left
  // set_above: true to move the menu to the top
  //            false to move it to the left
  function force_above(set_above) {
    if (set_above) {
      $("#menu-container").addClass("col-lg-12").removeClass("col-lg-3")
      $("#text-container").addClass("col-lg-12").removeClass("col-lg-9")
      menu.addClass("col-lg-12").removeClass("col-lg-3")
      menu.css("position", "relative")
    } else {
      $("#menu-container").removeClass("col-lg-12").addClass("col-lg-3")
      $("#text-container").removeClass("col-lg-12").addClass("col-lg-9")
      menu.removeClass("col-lg-12").addClass("col-lg-3")
      menu.css("position", "")
    }
    above = set_above;
  }

  // Function for checking whether the menu needs to be moved
  function test_threshold() {
    height = window.innerHeight;
    if (height >= threshold && above) {
      force_above(false);
    } else if (height < threshold && !above) {
      force_above(true);
    }
  }

  // Call the check whenever the window is resized
  $(window).on("resize", function() {
    test_threshold();
  });

  // Call the check on document ready
  test_threshold();
});
