const express = require('express');
const app = express();
const fs = require('fs');
const path = require('path');

app.get('/', function (req, res) {
  res.sendFile(__dirname + '/index.html');
});

app.get('/video', function (req, res) {
  const range = req.headers.range;
  if (!range) {
    res.status(400).send('Requires Range header');
  }

  const videoPath = path.resolve(__dirname, 'Sinthu 30th Birthday.mp4');
  const videoSize = fs.statSync(videoPath).size;
  const CHUNK_SIZE = 10 ** 6;
  const start = Number(range.replace(/\D/g, ''));
  const end = Math.min(start + CHUNK_SIZE, videoSize - 1);
  const contentLength = end - start + 1;
  const headers = {
    'Content-Range': `bytes ${start}-${end}/${videoSize}`,
    'Accept-Ranges': 'bytes',
    'Content-Length': contentLength,
    'Content-Type': 'video/mp4',
  };

  res.writeHead(206, headers);
  const videoStream = fs.createReadStream(videoPath, { start, end });
  videoStream.pipe(res);
});

app.get('/api/v1/climate', (_, response) => {
  const cpuTemperature = +require('child_process').execSync('cat /sys/class/thermal/thermal_zone0/temp') / 1000;
  const gpuTemperature = +(/[0-9]{1,4}\.[0-9]{1,4}/.exec(require('child_process').execSync('vcgencmd measure_temp').toString())[0]);

  response.status(200).send({
    humidity: {
      sensor: null
    },
    temperature: {
      cpu: cpuTemperature,
      gpu: gpuTemperature,
      sensor: null
    }
  });
});

app.listen(8000, function () {
  console.log('Listening on port 8000!');
});
