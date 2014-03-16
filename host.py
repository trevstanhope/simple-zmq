import zmq
import json
import datetime, time
from pymongo import MongoClient

ZMQ_HOST_ADDR = 'tcp://*:1980'
MONGO_DB = 'test'

class Host:

    def __init__(self):
    
        context = zmq.Context()
        self.connection = context.socket(zmq.REP)
        self.connection.bind(ZMQ_HOST_ADDR)
        
        client = MongoClient()
        self.database = client[MONGO_DB]
        
    def listen(self):
        
        ## collections
        requests_collection = self.database['requests']
        responses_collection = self.database['responses']
        
        ## get 
        packet = self.connection.recv()
        request = json.loads(packet)
        print request
        requests_collection.insert(request)
        
        # send
        response = {
            'type':'response',
            'time': time.time()
        }
        packet = json.dumps(response)
        responses_collection.insert(response)
        self.connection.send(packet)
        

if __name__ == '__main__':
    host = Host()
    while True:
        try:
            host.listen()
        except KeyboardInterrupt:
            break
            
