$(function () {
  // Create arrows between the steps in the diagram
  $('#step1').connections({ to: "#step2" });
  $('#step2').connections({ to: "#step3" });
  $('#step3').connections({ to: "#step4" });
  $('#step4').connections({ to: "#step5" });

  var c = $('connection');

  // Arrange the initial arrows
  c.connections('update');

  // Rearrange the arrows whenever the window is resized
  $(window).on("resize", function() {
    c.connections('update');
  });
});

