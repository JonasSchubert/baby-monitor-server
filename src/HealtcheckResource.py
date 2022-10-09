from twisted.web import resource
import json

class HealtcheckResource(resource.Resource):
    def render_GET(self, request):
        request.setHeader('Content-type', 'application/json')
        request.setHeader('Access-Control-Allow-Origin', '*')
        request.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTION')
        request.setHeader('Access-Control-Allow-Headers', 'Content-type')

        status = {'status': 'up'}
        return json.dumps(status).encode('utf-8')
