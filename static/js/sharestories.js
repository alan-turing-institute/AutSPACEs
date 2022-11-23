const form = document.querySelector('form');
const content = document.getElementById('content');

form.addEventListener('submit',(e) => {
  e.preventDefault();
  checkInput();
})

function checkInput(){
  if (content === ""){
    console.log("empty");
  }
}
