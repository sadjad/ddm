from twisted.internet import protocol, reactor
from twisted.protocols import basic

import simplejson

class DDMProtocol(basic.LineReceiver):
    def lineReceived(self, data):
        pass
        
class DDMServerFactory(protocol.ServerFactory):
    protocol = DDMProtocol
    
reactor.listenTCP(22999, DDMServerFactory())
reactor.run()