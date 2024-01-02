import json
import asyncio

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer


class QueueConsumer(AsyncWebsocketConsumer):
    counter = 0
    task_started = False
    queue = []

    async def connect(self):
        await self.accept()
        await self.send(text_data=json.dumps({
            'message': 'connection established',
        }))
        await self.send(text_data=json.dumps({
            'queue': self.queue,
        }))
        print('current queue:')
        for item in self.queue:
            print(item)

    async def disconnect(self, close_code):
        for user in self.queue:
            if user['channel_name'] == self.channel_name:
                self.queue.remove(user)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)

        print('message: ', text_data_json)
        await self.send(text_data=json.dumps({
            'message': 'in queue',
        }))
        self.queue.append({
            'channel_name': self.channel_name,
            'user_id': text_data_json.get('user_id'),
            'elo': text_data_json.get('elo'),
        })
        print(f'task_started: {self.task_started}')
        if len(self.queue) == 1:
            asyncio.ensure_future(self.matchmaking())
            self.task_started = True
        print(f'task_started: {self.task_started}')
        for user in self.queue:
            print(user)

    async def match_found(self, event):
        await self.send(text_data=json.dumps(event['message']))

    async def send_match_notification(self, player1, player2):
        channel_layer = get_channel_layer()
        await channel_layer.send(player1['channel_name'], {
            'type': 'match.found',
            'message': f"match found: {player1['user_id']} vs {player2['user_id']}",
        })
        await channel_layer.send(player2['channel_name'], {
            'type': 'match.found',
            'message': f"match found: {player1['user_id']} vs {player2['user_id']}",
        })
        print(f"match found: {player1['user_id']} vs {player2['user_id']}")

    async def matchmaking(self):
        while len(self.queue) > 0:
            if len(self.queue) >= 2:
                player1 = self.queue.pop()
                player2 = self.queue.pop()
                await self.send_match_notification(player1, player2)
            # print(f'counter: {self.counter}')
            self.counter += 1
            await asyncio.sleep(2)
