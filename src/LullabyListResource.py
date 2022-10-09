from twisted.web import resource
import glob
import json

class LullabyListResource(resource.Resource):
    def render_GET(self, request):
        request.setHeader("content-type", 'application/json')
        request.setHeader("Access-Control-Allow-Origin", '*')

        files = glob.glob('/mnt/lullaby-songs/*.mp3')

        return json.dumps(files).encode('utf-8')
