$(function () {
  // Activate the help popovers
  $('[data-toggle="popover"]').popover()

  // Control the visibility of a field
  function set_visibility(visible, field_id, instant) {
    duration = instant ? 0 : 200;
    $(field_id).prop('disabled', !visible);
    if (visible) {
      $(field_id).parent().show(duration);
    }
    else {
      $(field_id).parent().hide(duration);
    }
  }

  // Set the initial visibility
  set_visibility($('#id_gender').val() == 'self_identify', '#id_gender_self_identification', true)

  // Update the visibility when the selection changes
  $('#id_gender').on('change', function() {
    set_visibility(
      this.value == 'self_identify', '#id_gender_self_identification', false);
    }
  );
});

// Example starter JavaScript for disabling form submissions if there are invalid fields
(function() {
  'use strict';
  window.addEventListener('load', function() {
    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    var forms = document.getElementsByClassName('needs-validation');
    // Loop over them and prevent submission
    var validation = Array.prototype.filter.call(forms, function(form) {
      form.addEventListener('submit', function(event) {
        if (form.checkValidity() === false) {
          event.preventDefault();
          event.stopPropagation();
        }
        form.classList.add('was-validated');
      }, false);
    });
  }, false);
})();