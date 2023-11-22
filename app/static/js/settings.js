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
const customClear = document.getElementById('custom-clear');
const sessionValues = sessionTools.concat(sessionLangs);

let toolList = [];
let langList = [];
const toolLib = {"docker": "Docker", "vscode": "Vs Code", "flask": "Flask",
                 "expressjs": "ExpressJs", "nodejs": "NodeJs", "react": "React",
                 "vue": "Vue"}
const langLib = {"javascript": "JavaScript", "python": "Python", "c": "C",
                 "cpp": "C++", "csharp": "C#", "ruby": "Ruby", "go": "Go",
                 "rust": "Rust", "sql": "SQL", "scala": "Scala"}

// populates the list of tools and frameworks
for (let [key, value] of Object.entries(toolLib)) {
  toolCard.innerHTML += `
  <div class="form-check">
    <input class="form-check-input" type="checkbox" name="${key}" id="${key}">
    <label class="form-check-label" for="${key}">
      ${value}
    </label>
  </div>
  `;
}

// populates the list of languages
for (let [key, value] of Object.entries(langLib)) {
  langCard.innerHTML += `
  <div class="form-check">
    <input class="form-check-input" type="checkbox" name="${key}" id="${key}">
    <label class="form-check-label" for="${key}">
      ${value}
    </label>
  </div>
  `;
}

// ensures checks are constant upon reload
for (let key of Object.keys({...toolLib, ...langLib})) {
  if (sessionValues.includes(key)) {
    document.getElementById(key).checked = true;
  } else {
    document.getElementById(key).checked = false;
  }
}

// handles clearing checks for customizations
customClear.onclick = (() => {
  for (let key of Object.keys({...toolLib, ...langLib})) {
    document.getElementById(key).checked = false;
  }
});

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
