const loginText = document.querySelector(".title-text .login");
const loginForm = document.querySelector("form.login");
const signupForm = document.querySelector('form.signup');
const loginBtn = document.querySelector("label.login");
const signupBtn = document.querySelector("label.signup");
const signupLink = document.querySelector("form .signup-link a");
signupBtn.onclick = (()=>{
  loginForm.style.marginLeft = "-50%";
  loginText.style.marginLeft = "-50%";
});
loginBtn.onclick = (()=>{
  loginForm.style.marginLeft = "0%";
  loginText.style.marginLeft = "0%";
});
signupLink.onclick = (()=>{
  signupBtn.click();
  return false;
});

loginForm.addEventListener('submit', async function(event){
  event.preventDefault();
  const loadingAnimation = document.querySelector('.loader');
  loadingAnimation.style.display = "flex";
  const formData = new FormData(loginForm);
  console.log(formData.get("username"));
  const response = await fetch(loginForm.action, {method: 'POST', body: formData});
  loadingAnimation.style.display = "none";
  if (response.ok) {
    alert("login successful");
  } else {
    alert("Invalid credentials");
  }
});
