from twisted.web import server, resource
import json
import vlc

class LullabySongResource(resource.Resource):
    def __init__(self):
        self.mediaplayer = None

    def render_GET(self, request):
        request.setHeader('Content-type', 'application/json')
        request.setHeader('Access-Control-Allow-Origin', '*')
        request.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTION')
        request.setHeader('Access-Control-Allow-Headers', 'Content-type')

        return json.dumps(self.getStatus()).encode('utf-8')

    def render_OPTIONS(self, request):
        request.setHeader('Content-type', 'application/json')
        request.setHeader('Access-Control-Allow-Origin', '*')
        request.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTION')
        request.setHeader('Access-Control-Allow-Headers', 'Content-type')

        request.write('')
        request.finish()

        return server.NOT_DONE_YET

    # Used to start, update or stop a song, as well as to update the volume or mute/unmute
    def render_POST(self, request):
        request.setHeader('Content-type', 'application/json')
        request.setHeader('Access-Control-Allow-Origin', '*')
        request.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTION')
        request.setHeader('Access-Control-Allow-Headers', 'Content-type')

        configuration = json.loads(request.content.read().decode('utf-8'))

        if configuration['track'] != '':
            if self.mediaplayer != None:
                newMediaplayer = vlc.MediaPlayer(configuration['track'])
                if self.mediaplayer.get_media().get_mrl() != newMediaplayer.get_media().get_mrl():
                    self.stopSong()
                    self.playSong(configuration)
                else:
                    self.mediaplayer.audio_set_volume(configuration['volume'])
                    self.mediaplayer.audio_set_mute(configuration['mute'])
                newMediaplayer.release()
                newMediaplayer = None
            else:
                self.playSong(configuration)
        else:
            if self.mediaplayer != None:
                self.stopSong()

        return json.dumps(self.getStatus()).encode('utf-8')
    
    def getStatus(self):
        mute = False
        status = ''
        track = ''
        volume = 30

        if self.mediaplayer != None:
            mute = self.mediaplayer.audio_get_mute()
            status = self.mediaplayer.get_state()
            track = self.mediaplayer.get_media().get_mrl()
            volume = self.mediaplayer.audio_get_volume()
        
        return { 'mute': mute, 'status': f'{status}', 'track': track, 'volume': volume }

    def playSong(self, configuration):
        self.mediaplayer = vlc.MediaPlayer(configuration['track'])
        self.mediaplayer.audio_set_volume(configuration['volume'])
        self.mediaplayer.audio_set_mute(configuration['mute'])
        self.mediaplayer.play()

    def stopSong(self):
        self.mediaplayer.stop()
        self.mediaplayer.release()
        self.mediaplayer = None
