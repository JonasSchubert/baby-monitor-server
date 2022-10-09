#!/usr/bin/env python

from twisted.internet import reactor, protocol, defer, endpoints
import twisted.internet.error
from twisted.web import server
from twisted.web.resource import Resource
from twisted.web.server import Site

import subprocess

from ProcessProtocolUtils import spawnNonDaemonProcess
from LoggingUtils import log, setupLogging, LoggingProtocol
from JpegStreamReader import JpegStreamReader
from ClimateResource import ClimateResource
from HealtcheckResource import HealtcheckResource
from LatestImageResource import LatestImageResource
from LullabyListResource import LullabyListResource
from LullabySongResource import LullabySongResource
from MJpegResource import MJpegResource

def async_sleep(seconds):
    d = defer.Deferred()
    reactor.callLater(seconds, d.callback, seconds)
    return d

def startAudio():

    def startVlcAudio():
        spawnNonDaemonProcess(reactor, LoggingProtocol('vlc-audio'), '/bin/sh', ['sh', 'vlc-audio.sh'])
        log('Started vlc audio')

    reactor.callLater(2, startVlcAudio)

def audioAvailable():
    out = subprocess.check_output(['arecord', '-l'])
    return (b'USB Audio' in out)

def startAudioIfAvailable():
    if audioAvailable():
        startAudio()
    else:
        log('Audio not detected. Starting in silent mode')

class BabyMonitorApp:
    def __init__(self):
        queues = []

        self.reactor = reactor

        factory = protocol.Factory()
        factory.protocol = JpegStreamReader
        factory.queues = queues
        factory.latestImage = None
        reactor.listenTCP(9999, factory)
        log('Started listening for MJPEG stream')

        root = Resource()
        root.putChild(b'healthcheck', HealtcheckResource())
        root.putChild(b'climate', ClimateResource())
        root.putChild(b'stream.mjpeg', MJpegResource(queues))
        root.putChild(b'latest.jpeg', LatestImageResource(factory))
        root.putChild(b'lullaby-list', LullabyListResource())
        root.putChild(b'lullaby-song', LullabySongResource())

        site = Site(root)

        PORT = 8080
        BACKUP_PORT = 8081

        try:
            endpoint = endpoints.TCP4ServerEndpoint(reactor, PORT)
            endpoint.listen(site)
            log('Started webserver at port %d' % PORT)
        except twisted.internet.error.CannotListenError:
            endpoint = endpoints.TCP4ServerEndpoint(reactor, BACKUP_PORT)
            endpoint.listen(site)
            log('Started webserver at port %d' % BACKUP_PORT)

        startAudioIfAvailable()
        spawnNonDaemonProcess(reactor, LoggingProtocol('gstream-video'), '/bin/sh', ['sh', 'gstream_video.sh', '/dev/video0'])
        reactor.run()

if __name__ == "__main__":
    import logging
    setupLogging()
    log('Starting main method of baby monitor')
    try:
        app = BabyMonitorApp()
    except:
        import sys
        _, value, _ = sys.exc_info()
        print('Error opening %s: %s' % (value.filename, value.strerror))
        logging.exception("main() threw exception")
