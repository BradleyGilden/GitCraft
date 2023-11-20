const textarea = document.getElementById('floatingTextarea');
const charCountElement = document.getElementById('charCount');
const hireableCheck = document.getElementById('hireable');
const detailsForm = document.getElementById('gitUserDetails')
const clearBtn = document.getElementById('git-clear');

// Add event listener for the 'input' event
textarea.addEventListener('input', function() {
  const charCount = textarea.value.length;
  if (charCount > 160) {
    textarea.classList.add('is-invalid');
  } else if (charCount <= 160 && textarea.classList.contains('is-invalid')) {
    textarea.classList.remove('is-invalid');
  }
  charCountElement.innerHTML = 'Bio ' + charCount + '/160';
});

textarea.addEventListener('blur', function() {
  charCountElement.textContent = 'Bio';
})

hireableCheck.addEventListener('change', function() {
  if (hireableCheck.checked && !hireableCheck.classList.contains('bg-warning')) {
    hireableCheck.classList.add('bg-warning');
  } else if (!hireableCheck.checked && hireableCheck.classList.contains('bg-warning')) {
    hireableCheck.classList.remove('bg-warning');
  }
})

clearBtn.onclick = (() => {
  for (let i = 0; i < detailsForm.elements.length; i++) {
    let element = detailsForm.elements[i];
    // Check if the element is an input or textarea
    if (element.tagName === 'INPUT' || element.tagName === 'TEXTAREA') {
      element.value = '';
    }
  }
});

detailsForm.addEventListener('submit', async function(event){
  event.preventDefault();
  // const loadingAnimation = document.querySelector('.signup .loader');
  // loadingAnimation.style.display = 'flex';
  const formData = new FormData(detailsForm);
  const response = await fetch(detailsForm.action, {method: 'PATCH', body: formData});
  // loadingAnimation.style.display = 'none';
  if (response.ok) {
    Swal.fire({
      title: "Updated!",
      icon: "success"
    });
  } else {
    const jsonResponse = await response.json()
    Swal.fire({
      icon: "error",
      title: "Oops...",
      text: jsonResponse.message
    });
  }
});
