from twisted.internet import protocol
from datetime import datetime, timedelta
from LoggingUtils import log

MJPEG_SEP = b'--spionisto\r\n'

class JpegStreamReader(protocol.Protocol):
    def __init__(self):
        self.tnow = None

    def connectionMade(self):
        log('MJPEG Image stream received')
        self.data = b''
        self.tnow = datetime.now()
        self.cumDataLen = 0
        self.cumCalls = 0

    def dataReceived(self, data):
        self.data += data

        chunks = self.data.rsplit(MJPEG_SEP, 1)

        dataToSend = ''
        if len(chunks) == 2:
            subchunks = chunks[0].rsplit(MJPEG_SEP, 1)

            lastchunk = subchunks[-1]
            idx = lastchunk.find(b'\xff\xd8\xff')
            self.factory.latestImage = lastchunk[idx:]

            dataToSend = chunks[0] + MJPEG_SEP

        self.data = chunks[-1]

        self.cumDataLen += len(dataToSend)
        self.cumCalls += 1

        for producer in self.factory.queues:
            if (not producer.isPaused):
                producer.request.write(dataToSend)

        if datetime.now() - self.tnow > timedelta(seconds=1):
            # log('Wrote %d bytes in the last second (%d cals)' % (self.cumDataLen, self.cumCalls))
            self.tnow = datetime.now()
            self.cumDataLen = 0
            self.cumCalls = 0
