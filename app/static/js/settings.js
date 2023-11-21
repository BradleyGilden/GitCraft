const textarea = document.getElementById('floatingTextarea');
const charCountElement = document.getElementById('charCount');
const hireableCheck = document.getElementById('hireable');
const detailsForm = document.getElementById('gitUserDetails')
const clearBtn = document.getElementById('git-clear');
const toolCard = document.getElementById('tool-card');
const langCard = document.getElementById('lang-card');



const toolsList = ["docker", "VsCode", "Flask", "ExpressJs", "NodeJs", "React", "Vue"]
const langsList = ["JavaScript", "Python", "C", "C++", "C#", "Ruby", "Go", "Rust", "SQL", "Scala"]
for (let tool of toolsList) {
  toolCard.innerHTML += `
  <div class="form-check">
    <input class="form-check-input" type="checkbox" value="" id="${tool}Id">
    <label class="form-check-label" for="${tool}Id">
      ${tool}
    </label>
  </div>
  `;
}

for (let lang of langsList) {
  langCard.innerHTML += `
  <div class="form-check">
    <input class="form-check-input" type="checkbox" value="" id="${lang}Id">
    <label class="form-check-label" for="${lang}Id">
      ${lang}
    </label>
  </div>
  `;
}

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
