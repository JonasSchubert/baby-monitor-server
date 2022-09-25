const useClimate = (app) => app.get('/api/v1/climate', (_, response) => {
  const cpuTemperature = +require('child_process').execSync('cat /sys/class/thermal/thermal_zone0/temp') / 1000;
  const gpuTemperature = +(/[0-9]{1,4}\.[0-9]{1,4}/.exec(require('child_process').execSync('vcgencmd measure_temp').toString())[0]);

  const sensorClimate = require('child_process').execSync('python climate.py', { cwd: __dirname }).toString();
  const sensorTemperature = +(/Temperature\:\s[0-9]{1,4}\.[0-9]{1,2}/.exec(sensorClimate)[0].replace('Temperature: ', ''));
  const sensorHumidity = +(/Humidity\:\s[0-9]{1,4}\.[0-9]{1,2}/.exec(sensorClimate)[0].replace('Humidity: ', ''));

  response.status(200).send({
    humidity: {
      sensor: sensorHumidity,
      unit: '%'
    },
    temperature: {
      cpu: cpuTemperature,
      gpu: gpuTemperature,
      sensor: sensorTemperature,
      unit: '°C'
    }
  });
});

module.exports = {
  useClimate
};
