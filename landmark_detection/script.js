const video = document.getElementById('video');

Promise.all(
  [
    faceapi.nets.tinyFaceDetector.loadFromUri('../models'),
    faceapi.nets.faceLandmark68Net.loadFromUri('../models')
  ]
).then(startWebCam);

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
  });
}

video.addEventListener('play', () => {
  const canvas = faceapi.createCanvasFromMedia(video);
  document.body.append(canvas);

  setInterval(async () => {
    const detections = await faceapi.detectAllFaces(
      video,
      new faceapi.TinyFaceDetectorOptions()).withFaceLandmarks();
  }, 100);
});
