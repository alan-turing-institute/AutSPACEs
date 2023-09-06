let searchForm = document.getElementById("search-form");
let trigger_array = ["abuse-checkbox", "drug-checkbox", "negbody-checkbox", "violence-checkbox", "mentalhealth-checkbox", "other-checkbox"]

// Check if the all toggle has been changed
let all = document.getElementById("all-checkbox");
let abuse = document.getElementById("abuse-checkbox")
let vio = document.getElementById('violence-chcekbox')

$(function() {
    
}
    )


$(function() {
    $(".custom-control-input").on("change", pressSubmit)

    function pressSubmit() {
        all_checkbox = document.getElementById("all-checkbox").checked

        all_sing = trigger_array.forEach(item => console.log(document.getElementById(item).checked))

        alert(all_checkbox)
        
        $("#search-form").submit()

        // var state_after_submit_all = $("#all-checkbox").is(":checked")

        // var state_after_submit_indi = [
        //     $("#abuse-checkbox").is(":checked"),
        //     $("#drug-checkbox").is(":checked"),
        //     $("#negbody-checkbox").is(":checked"),
        //     $("#violence-checkbox").is(":checked"),
        //     $("#mentalhealth-checkbox").is(":checked"),
        //     $("#other-checkbox").is(":checked"),
        // ]

        // var isAllTrue = (x) => x == true;

        // var all_checked = state_after_submit_indi.every(isAllTrue)
        // alert("all " + state_after_submit_all + " indi " + state_after_submit_indi + "-----" + all_checked)
    }


  })

document.addEventListener("DOMContentLoaded", function(event) { 
    var scrollpos = localStorage.getItem('scrollpos');
    if (scrollpos) window.scrollTo(0, scrollpos);
});

window.onbeforeunload = function(e) {
    localStorage.setItem('scrollpos', window.scrollY);
};


  
