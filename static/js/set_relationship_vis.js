document.addEventListener("DOMContentLoaded", function(event) { 
    set_visibility(chk_radio(), '#id_authorship_relation', false)
    }
);

$(function() {
    $('input:radio').on('change', function() {
        set_visibility(chk_radio(), '#id_authorship_relation', false)
  })});

function chk_radio(){
    var rb = document.querySelectorAll('input[name="first_hand_authorship"]');
    if (rb[1].checked){ return true } else {return false}
}

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