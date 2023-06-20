let searchForm = document.getElementById("search-form");

$(function() {
    $(".custom-control-input").on("change", pressSubmit)
  
    function pressSubmit() {
        $("#search-form").submit()
    }
  })

document.addEventListener("DOMContentLoaded", function(event) { 
    var scrollpos = localStorage.getItem('scrollpos');
    if (scrollpos) window.scrollTo(0, scrollpos);
});

window.onbeforeunload = function(e) {
    localStorage.setItem('scrollpos', window.scrollY);
};


  
