from twisted.internet import reactor, interfaces
from zope.interface import implementer
from LoggingUtils import log 

@implementer(interfaces.IPushProducer)
class JpegProducer(object):
    def __init__(self, request):
        self.request = request
        self.isPaused = False
        self.isStopped = False
        self.delayedCall = None

    def cancelCall(self):
        if self.delayedCall:
            self.delayedCall.cancel()
            self.delayedCall = None

    def pauseProducing(self):
        self.isPaused = True
        self.cancelCall()

    def resetPausedFlag(self):
        self.isPaused = False
        self.delayedCall = None

    def resumeProducing(self):
        self.cancelCall()
        self.delayedCall = reactor.callLater(1, self.resetPausedFlag)

    def stopProducing(self):
        self.isPaused = True
        self.isStopped = True
        log('producer is requesting to be stopped')
