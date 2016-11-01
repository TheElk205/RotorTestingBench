import sys
import random

import numpy as np
from twisted.web.static import File
from twisted.python import log
from twisted.web.server import Site
from twisted.internet import reactor

from autobahn.twisted.websocket import WebSocketServerFactory, \
    WebSocketServerProtocol

from autobahn.twisted.resource import WebSocketResource


class SomeServerProtocol(WebSocketServerProtocol):
    def onOpen(self):
        """
       Connection from client is opened. Fires after opening
       websockets handshake has been completed and we can send
       and receive messages.

       Register client in factory, so that it is able to track it.
       Try to find conversation partner for this client.
       """
        self.factory.register(self)

    def connectionLost(self, reason):
        """
       Client lost connection, either disconnected or some error.
       Remove client from list of tracked connections.
       """
        self.factory.unregister(self)

    def onMessage(self, payload, isBinary):
        self.factory.communicate(self, payload, isBinary)


class DataPointsFactory(WebSocketServerFactory):
    def __init__(self, *args, **kwargs):
        super(DataPointsFactory, self).__init__(*args, **kwargs)
        self.clients = {}

    def register(self, client):
        self.clients[client.peer] = {"object": client, "partner": None}

    def unregister(self, client):
        self.clients.pop(client.peer)

    def communicate(self, client, payload, isBinary):
        client.sendMessage(np.array_str(np.random.rand(1, 20)))

if __name__ == "__main__":
    log.startLogging(sys.stdout)

    # static file server seving index.html as root
    root = File(".")

    factory = DataPointsFactory(u"ws://127.0.0.1:8080")
    factory.protocol = SomeServerProtocol
    resource = WebSocketResource(factory)
    # websockets resource on "/ws" path
    root.putChild(b"ws", resource)

    site = Site(root)
    reactor.listenTCP(8080, site)
    reactor.run()