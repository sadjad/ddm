from twisted.internet import protocol
from twisted.internet import reactor
from twisted.protocols import basic

from server_model import *

import simplejson

def create_error(message):
    response = {}
    response['type'] = "error"
    response['message'] = message
    return simplejson.dumps(response)

def process_command(command):
    response = {}
    
    if 'command' not in command:
        return create_error("Command not found.")
    
    if command['command'] == 'list':
        files = DownloadRequest.select().where(state=0)
        response['request_id'] = command['request_id']
        response['files'] = []
        
        for f in files:
            response['files'].append((f.url, f.size, f.chunks))
            
        return simplejson.dumps(response)
        
    elif command['command'] == 'fileinfo':
        pass
    elif command['command'] == 'getchunk':
        pass
    else:
        return create_error("Unknown command.")

def process_request(req):
    request =simplejson.loads(req);
    response = {}
    
    if 'request_id' not in req:
        response['request_id'] = None
    
    if 'type' not in req:
        return create_error("Invalid request.")
    
    if request['type'] == 'command':
        return process_command(request)
        

class DDMProtocol(basic.LineReceiver):
    def lineReceived(self, data):
        pass
        
class DDMServerFactory(protocol.ServerFactory):
    protocol = DDMProtocol
    
reactor.listenTCP(22999, DDMServerFactory()) #@UndefinedVariable
reactor.run() #@UndefinedVariable