$(function () {




    $(document).ready(function() {
        $('input:radio').change(function() {
          var ele = document.getElementsByName('authorship_status');

          for (i = 0; i < ele.length; i++) {
            if (ele[i].checked)
                   op = ele[i].value;}

        // set_visibility(

        if (op == "Experience is someone else's")
            // set_visibility(false, '#id_authorship_relation', true)
            alert("MAKE VISIBLE")

        });
    });

    // // Set the initial visibility
    // set_visibility(false, '#id_author_relationship', true)

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
