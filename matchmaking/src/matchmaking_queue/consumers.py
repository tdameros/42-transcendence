import json
import asyncio

from channels.generic.websocket import AsyncWebsocketConsumer


class QueueConsumer(AsyncWebsocketConsumer):
    queue = []
    clients = set()

    async def connect(self):
        await self.accept()
        await self.send(text_data=json.dumps({
            'message': 'connection established',
        }))
        asyncio.ensure_future(self.matchmaking())

    def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)

        print('message: ', text_data_json)
        await self.send(text_data=json.dumps({
            'message': 'in queue',
        }))
        self.queue.append({
            'user_id': text_data_json.get('user_id'),
            'elo': text_data_json.get('elo'),
        })
        for user in self.queue:
            print(user)

    async def send_match_notification(self, player1, player2):
        await self.send(text_data=json.dumps({
            'message': f'match found: {player1} vs {player2}'
        }))
        print(f'match found: {player1} vs {player2}')

    async def matchmaking(self):
        while True:
            if len(self.queue) >= 2:
                player1 = self.queue.pop()
                player2 = self.queue.pop()
                await self.send_match_notification(player1, player2)
            await asyncio.sleep(2)