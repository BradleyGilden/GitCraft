const downBtn1 = document.getElementById('download-btn1');
const downBtn2 = document.getElementById('download-btn2');
const select = document.getElementById('dev-type');
const viewLink = document.getElementById('view-param');

// Add an event listener to the select element
select.addEventListener('change', function() {
    // Get the selected value
    let selectedValue = select.value;

    // Update the href attribute of the link with the selected value
    viewLink.href = viewLink.dataset.select + selectedValue;
});

downBtn1.addEventListener('click', async function() {
  const loadingAnimation = `
  <span class="spinner-border spinner-border-sm" aria-hidden="true"></span>
  <span role="status">Downloading...</span>
  `;
  downBtn1.innerHTML = loadingAnimation;
  const response = await fetch(downBtn1.dataset.download, {
    method: 'GET',
    headers: {'Content-Type': 'application/zip'}
  });
  const blob = await response.blob();
  downBtn1.innerHTML = "Download";
  const link = document.createElement('a');
  link.href = window.URL.createObjectURL(blob);
  link.download = 'portfolio.zip'; // Specify the filename
  // Append the link to the document
  document.body.appendChild(link);
  // Trigger a click on the link to start the download
  link.click();
  // Remove the link from the document
  document.body.removeChild(link);
});

downBtn2.addEventListener('click', async function() {
  const queryString = new URLSearchParams({param1: select.value}).toString();
  const loadingAnimation = `
  <span class="spinner-border spinner-border-sm" aria-hidden="true"></span>
  <span role="status">Downloading...</span>
  `;
  downBtn2.innerHTML = loadingAnimation;
  const response = await fetch(`${downBtn2.dataset.download}?${queryString}`, {
    method: 'GET',
    headers: {'Content-Type': 'application/zip'}
  });
  const blob = await response.blob();
  downBtn2.innerHTML = "Download";
  const link = document.createElement('a');
  link.href = window.URL.createObjectURL(blob);
  link.download = 'portfolio_scrollable.zip'; // Specify the filename
  // Append the link to the document
  document.body.appendChild(link);
  // Trigger a click on the link to start the download
  link.click();
  // Remove the link from the document
  document.body.removeChild(link);
});
