import json

from channels.generic.websocket import WebsocketConsumer

class QueueConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

        self.send(text_data=json.dumps({
            'message': 'hey'
        }))

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)

        print(text_data_json)
        self.send(text_data=json.dumps(text_data_json))
