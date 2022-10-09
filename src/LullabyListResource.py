from twisted.web import resource
import glob
import json

class LullabyListResource(resource.Resource):
    def render_GET(self, request):
        request.setHeader('Content-type', 'application/json')
        request.setHeader('Access-Control-Allow-Origin', '*')
        request.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTION')
        request.setHeader('Access-Control-Allow-Headers', 'Content-type')

        files = glob.glob('/mnt/lullaby-songs/*')

        return json.dumps(files).encode('utf-8')
