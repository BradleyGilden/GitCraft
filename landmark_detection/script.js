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
  faceapi.matchDimensions(canvas, {height: video.height, width: video.width})

  setInterval(async () => {
    const detections = await faceapi.detectAllFaces(
      video,
      new faceapi.TinyFaceDetectorOptions()).withFaceLandmarks();

      const resizedDetections = faceapi.resizeResults(detections, {
        width: video.width,
        height: video.height
      })
      canvas.getContext("2d").clearRect(0, 0, canvas.width, canvas.height);
      faceapi.draw.drawDetections(canvas, resizedDetections);
      faceapi.draw.drawFaceLandmarks(canvas, resizedDetections);
  }, 100);
});
