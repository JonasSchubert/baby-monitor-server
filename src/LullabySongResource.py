from twisted.web import server, resource
import json
import vlc

class LullabySongResource(resource.Resource):
    def __init__(self):
        self.mediaplayer = None
        self.mute = False
        self.volume = 30

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

        try:
            configuration = json.loads(request.content.read().decode('utf-8'))
            self.mute = bool(configuration['mute'])
            self.volume = int(configuration['volume'])

            if configuration['track'] != '':
                if self.mediaplayer != None:
                    newMediaplayer = vlc.MediaPlayer(configuration['track'])
                    if self.mediaplayer.get_media().get_mrl() != newMediaplayer.get_media().get_mrl():
                        self.stopSong()
                        self.playSong(configuration)
                    else:
                        self.mediaplayer.audio_set_volume(self.volume)
                        self.mediaplayer.audio_set_mute(self.mute)
                    newMediaplayer.release()
                    newMediaplayer = None
                else:
                    self.playSong(configuration)
            else:
                if self.mediaplayer != None:
                    self.stopSong()

            return json.dumps(self.getStatus()).encode('utf-8')
        except:
            import sys
            _, value, _ = sys.exc_info()
            print('Error opening %s: %s' % (value.filename, value.strerror))
            self.mediaplayer = None
            return json.dumps({ 'mute': False, 'status': 'Error', 'track': '', 'volume': -1 }).encode('utf-8')
    
    def getStatus(self):
        status = ''
        track = ''

        if self.mediaplayer != None:
            status = self.mediaplayer.get_state()
            track = self.mediaplayer.get_media().get_mrl()
        
        return { 'mute': self.mute, 'status': f'{status}', 'track': track, 'volume': self.volume }

    def playSong(self, configuration):
        self.mediaplayer = vlc.MediaPlayer(configuration['track'])
        self.mediaplayer.audio_set_volume(self.volume)
        self.mediaplayer.audio_set_mute(self.mute)
        self.mediaplayer.play()

    def stopSong(self):
        self.mediaplayer.stop()
        self.mediaplayer.release()
        self.mediaplayer = None
