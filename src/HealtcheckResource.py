from twisted.web import resource
import json

class HealtcheckResource(resource.Resource):
    def render_GET(self, request):
        request.setHeader("content-type", 'application/json')
        request.setHeader("Access-Control-Allow-Origin", '*')

        status = {'status': 'up'}
        return json.dumps(status).encode('utf-8')
