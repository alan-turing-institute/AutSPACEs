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

