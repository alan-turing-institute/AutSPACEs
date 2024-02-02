document.addEventListener("DOMContentLoaded", function() { 
    change_viz(chk_radio(), 'id_authorship_relation');
    check_checkbox('id_other');
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

$("#id_other").on("keyup", function(e){
  if(this.value!=""){
        $("#id_other_trigger").prop("checked", "checked");
  }else{
        $("#id_other_trigger").prop('checked', "");
  }
});

function check_checkbox (field_id) {
  r = document.getElementById(field_id)
  if (r.value != "") {
    $("#id_other_trigger").prop("checked", "checked");}
  else {
    $("#id_other_trigger").prop("checked", "");
    }
}