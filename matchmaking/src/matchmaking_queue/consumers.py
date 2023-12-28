import json

from channels.generic.websocket import AsyncWebsocketConsumer


class QueueConsumer(AsyncWebsocketConsumer):
    queue = []

    async def connect(self):
        await self.accept()
        await self.send(text_data=json.dumps({
            'message': 'connection established',
        }))

    def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)

        print('received message: ', text_data_json);
        await self.send(text_data=json.dumps({
            'message': 'in queue',
        }))
        self.queue.append({
            'user_id': text_data_json.get('user_id'),
            'elo': text_data_json.get('elo'),
        })
        for user in self.queue:
            print(user)
