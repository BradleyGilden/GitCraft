const logoutButton = document.querySelector('#logout-btn');
const refreshButton = document.querySelector('#refresh-btn');
const tokenDisplay = document.querySelector('#token-display');

document.addEventListener('DOMContentLoaded', () => {
  let def = true;
  let links = document.querySelectorAll('.custom-nav-toggle');
  for (let link of links) {
    if (link.href === window.location.href) {
      link.classList.add('active');
      def = false
    } else {
      link.classList.remove('active');
    }
  }
  // default option if no page is visited
  if (def) {
    links[0].classList.add('active');
  }
})

logoutButton.onclick = (()=>{
  Swal.fire({
    backdrop: false,
    title: "Are you sure you want to logout?",
    confirmButtonColor: "#00c50a",
    showCancelButton: true,
    confirmButtonText: "Logout",
  }).then((result) => {
    if (result.isConfirmed) {
      return fetch(logoutButton.dataset.logout, {
        method: 'POST',
      })
      .then(response => {
        if (response.status < 400) {
          window.location.href = response.url;
        } else {
          console.error('Logout failed:', response.statusText);
        }
      })
      .catch(error => {
        console.error('Error during logout:', error);
      });
    }
  });
});

refreshButton.addEventListener('click', async() => {
  const loadingAnimation = `
  <span class="spinner-border spinner-border-sm" aria-hidden="true"></span>
  <span role="status">Refreshing...</span>
  `;
  refreshButton.innerHTML = loadingAnimation;
  const response = await fetch(refreshButton.dataset.refresh, {
    method: 'GET',
  });
  refreshButton.innerHTML = "Refresh";
  if (response.status < 400) {
    location.reload(true);
  } else {
    Swal.fire({
      title: "Updated!",
      icon: "error",
      text: "failed to reload data"
    });
  }
});

tokenDisplay.addEventListener('mouseenter', () => {
  tokenDisplay.parentNode.classList.remove('ms-5');
  tokenDisplay.style.fontSize = "0.7rem";
  tokenDisplay.textContent = tokenDisplay.dataset.tokenshow;
});
tokenDisplay.addEventListener('mouseleave', () => {
  tokenDisplay.parentNode.classList.add('ms-5');
  tokenDisplay.style.fontSize = "1rem";
  tokenDisplay.textContent = "***********";
});
