const downBtn1 = document.getElementById('download-btn1');

downBtn1.addEventListener('click', async function() {
  const response = await fetch(downBtn1.dataset.download, {
    method: 'GET',
    headers: {'Content-Type': 'application/zip'}
  });
  const blob = await response.blob();
  const link = document.createElement('a');
  link.href = window.URL.createObjectURL(blob);
  link.download = 'downloaded_file.zip'; // Specify the filename
  // Append the link to the document
  document.body.appendChild(link);
  // Trigger a click on the link to start the download
  link.click();
  // Remove the link from the document
  document.body.removeChild(link);
});
