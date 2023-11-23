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
const toolLib = {
  "VsCode|#0078D4|https://img.shields.io/badge/Visual_Studio_Code-0078D4?style=for-the-badge&logo=visual%20studio%20code&logoColor=white": "Vs Code",
  "Flask|#000000|https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white": "Flask",
  "Nodejs|#43853D|https://img.shields.io/badge/Node.js-43853D?style=for-the-badge&logo=node.js&logoColor=white": "Node.js",
  "React|#61DAFB|https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB": "React",
  "Vuejs|#35495E|https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vue.js&logoColor=4FC08D": "Vue.js",
  "MySQL|#00000F|https://img.shields.io/badge/MySQL-00000F?style=for-the-badge&logo=mysql&logoColor=white":"MySQL",
  "MongoDB|#4EA94B|https://img.shields.io/badge/MongoDB-4EA94B?style=for-the-badge&logo=mongodb&logoColor=white": "MongoDB",
  "Flutter|#02569B|https://img.shields.io/badge/Flutter-02569B?style=for-the-badge&logo=flutter&logoColor=white": "Flutter",
  "Spring|#6DB33F|https://img.shields.io/badge/Spring-6DB33F?style=for-the-badge&logo=spring&logoColor=white": "Spring",
  "Angular|#DD0031|https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white": "Angular"
}
const langLib = {
  "JavaScript|#F7DF1E|https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black": "JavaScript",
  "Python|#14354C|https://img.shields.io/badge/Python-14354C?style=for-the-badge&logo=python&logoColor=white": "Python",
  "C|#00599C|https://img.shields.io/badge/C-00599C?style=for-the-badge&logo=c&logoColor=white": "C",
  "C++|#00599C|https://img.shields.io/badge/C%2B%2B-00599C?style=for-the-badge&logo=c%2B%2B&logoColor=white": "C++",
  "C#|#239120|https://img.shields.io/badge/C%23-239120?style=for-the-badge&logo=c-sharp&logoColor=white": "C#",
  "Java|#ED8B00|https://img.shields.io/badge/Java-ED8B00?style=for-the-badge&logo=openjdk&logoColor=white": "Java",
  "Ruby|#CC342D|https://img.shields.io/badge/Ruby-CC342D?style=for-the-badge&logo=ruby&logoColor=white": "Ruby",
  "Go|#00ADD8|https://img.shields.io/badge/Go-00ADD8?style=for-the-badge&logo=go&logoColor=white": "Go",
  "Rust|#000000|https://img.shields.io/badge/Rust-000000?style=for-the-badge&logo=rust&logoColor=white": "Rust",
  "PHP|#777BB4|https://img.shields.io/badge/PHP-777BB4?style=for-the-badge&logo=php&logoColor=white": "PHP",
  "Scala|#DC322F|https://img.shields.io/badge/Scala-DC322F?style=for-the-badge&logo=scala&logoColor=white": "Scala"
}

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
  const customUpdate = document.querySelector('#custom-update');
  const loadingAnimation = `
  <span class="spinner-border spinner-border-sm" aria-hidden="true"></span>
  <span role="status">Updating...</span>
  `;
  customUpdate.innerHTML = loadingAnimation;
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
  customUpdate.innerHTML = "Update";
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
  const gitUpdate = document.querySelector('#git-update');
  const loadingAnimation = `
  <span class="spinner-border spinner-border-sm" aria-hidden="true"></span>
  <span role="status">Updating...</span>
  `;
  gitUpdate.innerHTML = loadingAnimation;
  const formData = new FormData(detailsForm);
  const response = await fetch(detailsForm.action, {method: 'PATCH', body: formData});
  gitUpdate.innerHTML = "Update";
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
