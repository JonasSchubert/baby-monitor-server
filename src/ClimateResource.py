from twisted.web import resource
import json
import subprocess
from GroveTemperatureHumiditySensorSHT3x import GroveTemperatureHumiditySensorSHT3x

class ClimateResource(resource.Resource):
    def render_GET(self, request):
        request.setHeader('Content-type', 'application/json')
        request.setHeader('Access-Control-Allow-Origin', '*')
        request.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTION')
        request.setHeader('Access-Control-Allow-Headers', 'Content-type')

        sensor = GroveTemperatureHumiditySensorSHT3x()
        temperature, humidity = sensor.read()

        cpuTemperatureOut = subprocess.Popen(["cat", "/sys/class/thermal/thermal_zone0/temp"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        cpuTemperature = int(cpuTemperatureOut.stdout.read().decode("utf-8")) / 1000

        gpuTemperatureOut = subprocess.Popen(["vcgencmd", "measure_temp"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        gpuTemperature = float(gpuTemperatureOut.stdout.read().decode('utf-8').split("=")[1].split("'")[0])

        status = {'humidity': { 'sensor': humidity, 'unit': '%' }, 'temperature': { 'cpu': cpuTemperature, 'gpu': gpuTemperature, 'sensor': temperature, 'unit': '°C' } }
        return json.dumps(status).encode('utf-8')
