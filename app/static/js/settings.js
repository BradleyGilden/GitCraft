const textarea = document.getElementById('floatingTextarea');
const charCountElement = document.getElementById('charCount');
const hireableCheck = document.getElementById('hireable');
const detailsForm = document.getElementById('gitUserDetails')
const clearBtn = document.getElementById('git-clear');
const toolCard = document.getElementById('tool-card');
const langCard = document.getElementById('lang-card');
const checkForm = document.getElementById('customize');
const toolsContainer = document.getElementById('tools');
const langsContainer = document.getElementById('languages');
const toolText = document.querySelector('.tool-list-display');
const langText = document.querySelector('.lang-list-display');

let toolList = [];
let langList = [];
const toolLib = ["docker", "VsCode", "Flask", "ExpressJs", "NodeJs", "React", "Vue"]
const langLib = ["JavaScript", "Python", "C", "C++", "C#", "Ruby", "Go", "Rust", "SQL", "Scala"]

// populates the list of tools and frameworks
for (let tool of toolLib) {
  let idVal = tool.toLowerCase()
  toolCard.innerHTML += `
  <div class="form-check">
    <input class="form-check-input" type="checkbox" name="${idVal}" id="${idVal}">
    <label class="form-check-label" for="${idVal}">
      ${tool}
    </label>
  </div>
  `;
}

// populates the list of languages
for (let lang of langLib) {
  let idVal = lang.toLowerCase()
  if (idVal === 'c++') {
    idVal = 'cpp';
  } else if (idVal === 'c#') {
    idVal = 'csharp';
  }
  langCard.innerHTML += `
  <div class="form-check">
    <input class="form-check-input" type="checkbox" name="${idVal}" id="${idVal}">
    <label class="form-check-label" for="${idVal}">
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

// removes count when away from bio input
textarea.addEventListener('blur', function() {
  charCountElement.textContent = 'Bio';
})

// customizes the hireable check button
hireableCheck.addEventListener('change', function() {
  if (hireableCheck.checked && !hireableCheck.classList.contains('bg-warning')) {
    hireableCheck.classList.add('bg-warning');
  } else if (!hireableCheck.checked && hireableCheck.classList.contains('bg-warning')) {
    hireableCheck.classList.remove('bg-warning');
  }
})

// looks for language and tool checks
toolsContainer.addEventListener('change', (event) => {
  if (event.target instanceof HTMLInputElement && event.target.type === 'checkbox') {
    if (event.target.checked) {
      toolList.push(event.target.labels[0].textContent);
    } else {
      toolList = toolList.filter(item => item !== event.target.labels[0].textContent);
    }
  }
  toolText.textContent = toolList.join(", ");
});
langsContainer.addEventListener('change', (event) => {
  if (event.target instanceof HTMLInputElement && event.target.type === 'checkbox') {
    if (event.target.checked) {
      langList.push(event.target.labels[0].textContent);
    } else {
      langList = langList.filter(item => item !== event.target.labels[0].textContent);
    }
  }
  langText.textContent = langList.join(", ");
});

clearBtn.onclick = (() => {
  for (let i = 0; i < detailsForm.elements.length; i++) {
    let element = detailsForm.elements[i];
    // Check if the element is an input or textarea
    if (element.tagName === 'INPUT' || element.tagName === 'TEXTAREA') {
      element.value = '';
    }
  }
});

// submits custom information to mongodb
checkForm.addEventListener('submit', async function(event){
  event.preventDefault();
  // const loadingAnimation = document.querySelector('.signup .loader');
  // loadingAnimation.style.display = 'flex';
  let langPut = {"langs": []}
  let toolPut = {"tools": []}
  const formData = new FormData(checkForm);
  formData.forEach((value, key) => {
    if (document.getElementsByName(key)[0].parentNode.parentNode.id === 'tool-card') {
      toolPut.tools.push(key)
    } else if (document.getElementsByName(key)[0].parentNode.parentNode.id === 'lang-card') {
      langPut.langs.push(key)
    }
  });
  const response = await fetch(checkForm.action,
    {
      method: 'PUT',
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({"langs": langPut.langs, "tools": toolPut.tools})
    }
  );
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

// alters github detail information
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
