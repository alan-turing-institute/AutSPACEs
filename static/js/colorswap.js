const button = document.getElementsByClassName('colorbutton');

for (i=0; i < button.length; i++) {
  button[i].addEventListener('click',function(){
    var buttonName = this.innerText;
    colorSwap(buttonName);
  });
}
var setTheme = localStorage.getItem('theme');
console.log('theme', setTheme);

if (setTheme == null) {
  colorSwap('Color View');
} else {
  colorSwap(setTheme);
}

function colorSwap(sheet) {
  switch (sheet) {
    case "Color View":
        document.getElementById('mystylesheet').href = "static/css/navigation_light.css";
        localStorage.setItem('theme',sheet);
        break;
    case "Calm View":
        document.getElementById('mystylesheet').href = "static/css/navigation_dark.css";
        localStorage.setItem('theme',sheet);
        break;
    default:
         document.getElementById('mystylesheet').href = "static/css/navigation_light.css";
  }
}


