from twisted.web import server, resource
from JpegProducer import JpegProducer
from LoggingUtils import log

class MJpegResource(resource.Resource):
    def __init__(self, queues):
        self.queues = queues

    def setupProducer(self, request):
        producer = JpegProducer(request)
        request.notifyFinish().addErrback(self._responseFailed, producer)
        request.registerProducer(producer, True)

        self.queues.append(producer)

    def _responseFailed(self, err, producer):
        log('connection to client lost')
        producer.stopProducing()

    def render_GET(self, request):
        log('getting new client of image stream')
        request.setHeader("content-type", 'multipart/x-mixed-replace; boundary=--spionisto')

        self.setupProducer(request)
        return server.NOT_DONE_YET
