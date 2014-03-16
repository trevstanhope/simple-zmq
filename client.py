import zmq
import json
import datetime, time

ZMQ_CLIENT_ADDR = 'tcp://127.0.0.1:1980'

class Client:

    def __init__(self):
        context = zmq.Context()
        self.connection = context.socket(zmq.REQ)
        self.connection.connect(ZMQ_CLIENT_ADDR)
        
    def talk(self):
    
        ## Send
        request = {
            'type':'request',
            'time' : time.time(),
        }
        packet = json.dumps(request)
        self.connection.send(packet)
        
        ## Get
        packet = self.connection.recv()
        response = json.loads(packet)
        print response
        
if __name__ == '__main__':
    client = Client()
    while True:
        try:
            client.talk()
        except KeyboardInterrupt:
            break
