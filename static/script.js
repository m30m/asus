const video = document.getElementById('video');

Promise.all([
  faceapi.nets.tinyFaceDetector.loadFromUri('static/models'),
  faceapi.nets.faceLandmark68Net.loadFromUri('static/models'),
  faceapi.nets.faceRecognitionNet.loadFromUri('static/models'),
  faceapi.nets.faceExpressionNet.loadFromUri('static/models')
]).then(startVideo);

function startVideo() {
  console.log("start video");
  navigator.mediaDevices.getUserMedia({
                video: {
                    advanced: [{
                        facingMode: "user"
                    }]
                },
                "height": {"exact": 480},
                "width": {"exact": 640}
            }).then(function (stream) {
                video.srcObject = stream;
            });
}

socket = io();
socket.on('connect', function () {
  socket.emit('init', { type:'face', state: 0 })
});

video.addEventListener('play', () => {
  const canvas = faceapi.createCanvasFromMedia(video);
  document.body.append(canvas);
  const displaySize = { width: video.width, height: video.height };
  faceapi.matchDimensions(canvas, displaySize);
  setInterval(async () => {
    const detections = await faceapi.detectAllFaces(video, new faceapi.TinyFaceDetectorOptions()).withFaceLandmarks().withFaceExpressions()
    if(detections.length) {
      var happiness = detections[0]['expressions']['happy']
      socket.emit('update_state', {state: happiness})
    }
    const resizedDetections = faceapi.resizeResults(detections, displaySize);
    canvas.getContext('2d').clearRect(0, 0, canvas.width, canvas.height);
    faceapi.draw.drawDetections(canvas, resizedDetections);
    faceapi.draw.drawFaceLandmarks(canvas, resizedDetections);
    faceapi.draw.drawFaceExpressions(canvas, resizedDetections)
  }, 100)
});
