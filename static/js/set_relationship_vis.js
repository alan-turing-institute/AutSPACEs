$(function () {
    $(document).ready(function() {
        $('input:radio').change(function() {
          var ele = document.getElementsByName('first_hand_authorship');

          for (i = 0; i < ele.length; i++) {
            if (ele[i].checked)
                   op = ele[i].value;}

        if (op == "False")
            set_visibility(true, '#id_authorship_relation', true)

        if (op == "True")
            set_visibility(false, '#id_authorship_relation', true)

        });
    });

    // Set the initial visibility
    // alert($('input[name="first_hand_authorship"]:checked').val()==undefined)
    set_visibility($('input[name="first_hand_authorship"]:checked').val()!=undefined, '#id_authorship_relation', true)

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

});
