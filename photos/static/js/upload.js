

var preview = document.querySelector("#preview")
var form = document.querySelector("form#img")
form.addEventListener("onchange", function(){
    preview.src=window.URL.createObjectURL(this.files[0])
})