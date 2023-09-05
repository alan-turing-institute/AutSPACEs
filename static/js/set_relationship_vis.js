document.addEventListener("DOMContentLoaded", function() { 
    change_viz(chk_radio(), 'id_authorship_relation')
    }
);

$(function() {
    $('input:radio').on('change', function() {
        change_viz(chk_radio(), 'id_authorship_relation');
  })});

function chk_radio(){
    var rb = document.querySelectorAll('input[name="first_hand_authorship"]');
    if (rb[1].checked){ return true } else {return false}
}

function change_viz (viz, field_id) {
  r = document.getElementById(field_id)
  if (viz == true) {
    r.parentElement.style.visibility = ""}
  else {
    r.parentElement.style.visibility = "hidden"
    r.value = ""
    }
}

