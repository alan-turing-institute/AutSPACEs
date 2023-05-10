let abuse = document.getElementById("abuse-checkbox");
let drug = document.getElementById("drug-checkbox");
let negbody = document.getElementById("negbody-checkbox");
let violence = document.getElementById("violence-checkbox");
let mentalhealth = document.getElementById("mentalhealth-checkbox");
let other = document.getElementById("other-checkbox");

let searchForm = document.getElementById("search-form");

abuse.addEventListener("change", pressSubmit);
drug.addEventListener("change", pressSubmit);
negbody.addEventListener("change", pressSubmit);
violence.addEventListener("change", pressSubmit);
mentalhealth.addEventListener("change", pressSubmit);
other.addEventListener("change", pressSubmit);


function pressSubmit() {
    searchForm.submit();
}
