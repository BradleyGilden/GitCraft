const video = document.getElementById('video');

function startWebCam() {
  navigator.mediaDevices.getUserMedia({
    video: true,
    audio: false
  })
  .then((stream) => {
    video.srcObject = stream;
  })
  .catch((error) => {
    console.log(error);
  })
}

startWebCam();
