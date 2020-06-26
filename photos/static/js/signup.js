var password = document.getElementById("password")
var confirm_password = document.getElementById("confirm_password")
var unmatched_password = document.getElementById("unmatched_password")
var submit_button = document.getElementById("submit_button")

function validatePassword(){
  if(password.value != confirm_password.value) {
    confirm_password.setCustomValidity("Passwords Don't Match")
    unmatched_password.style.display = "block"
    submit_button.disabled = true
  } else {
    confirm_password.setCustomValidity('')
    unmatched_password.style.display = "none"
    submit_button.disabled = false
  }
}

password.onchange = validatePassword
confirm_password.onkeyup = validatePassword