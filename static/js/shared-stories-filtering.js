let all_check = document.getElementById("all-checkbox")
let trigger_array = ["abuse-checkbox",
                     "drug-checkbox", 
                     "negbody-checkbox", 
                     "violence-checkbox", 
                     "mentalhealth-checkbox", "other-checkbox"]


$(all_check).change(function(){
    // If the all-trigger checkbox is checked ensure all single triggers are checked
    // If the all-trigger checkbox is unchecked, ensure all single triggers are unchecked
    if (all_check.checked == true) {
        for (let i = 0; i < trigger_array.length; i++) {
            document.getElementById(trigger_array[i]).checked = true
        }
    } else {
        for (let i = 0; i < trigger_array.length; i++) {
            document.getElementById(trigger_array[i]).checked = false
        }
    }

    $("#search-form").submit()
})

$("#single_trigger_warnings :checkbox").change(function(){
    // check if all the single trigger warnings are checked
    // if so check the "all" checkbox

    var all_sing = [];
    for (let i = 0; i < trigger_array.length; i++) {
        all_sing.push(document.getElementById(trigger_array[i]).checked)
    }

    if (all_sing.includes(false)) {
        document.getElementById("all-checkbox").checked = false
    } else {
        document.getElementById("all-checkbox").checked = true
    }

    $("#search-form").submit()

});

document.addEventListener("DOMContentLoaded", function(event) { 
    var scrollpos = localStorage.getItem('scrollpos');
    if (scrollpos) window.scrollTo(0, scrollpos);
});

window.onbeforeunload = function(e) {
    localStorage.setItem('scrollpos', window.scrollY);
};


  
