import datetime
import json
import asyncio
from time import time

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer

from matchmaking import settings


class QueueConsumer(AsyncWebsocketConsumer):
    queue = []

    async def connect(self):
        await self.accept()
        await self.send(text_data=json.dumps({
            'type': 'message',
            'data': 'connection established',
        }))

    async def disconnect(self, close_code):
        for user in self.queue:
            if user['channel_name'] == self.channel_name:
                self.queue.remove(user)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_type = text_data_json.get('type')

        print('received: ', text_data_json)
        if message_type == 'matchmaking.join':
            await self.matchmaking_join(text_data_json)
        if message_type == 'matchmaking.start':
            await self.matchmaking_start(text_data_json)
        if message_type == 'matchmaking.info':
            await self.matchmaking_info(text_data_json)

    async def match_found(self, event):
        await self.send(text_data=json.dumps(event))

    async def matchmaking_join(self, json_message):
        data = json_message.get('data')
        self.queue.append({
            'user_id': data.get('user_id'),
            'elo': data.get('elo'),
            'channel_name': self.channel_name,
            'timestamp': time(),
        })
        await self.send(text_data=json.dumps({
            'type': 'message',
            'data': 'in queue',
        }))

    async def matchmaking_start(self, json_message):
        asyncio.ensure_future(self.matchmaking())

    async def matchmaking_info(self, json_message):
        await self.send(json.dumps(self.queue))

    @staticmethod
    async def send_match_notification(player1, player2):
        channel_layer = get_channel_layer()
        data = [
            {
                'user_id': player1.get('user_id'),
                'elo': player1.get('elo'),
            },
            {
                'user_id': player2.get('user_id'),
                'elo': player2.get('elo'),
            }
        ]

        await channel_layer.send(player1['channel_name'], {
            'type': 'match.found',
            'data': json.dumps(data),
        })
        await channel_layer.send(player2['channel_name'], {
            'type': 'match.found',
            'data': json.dumps(data),
        })
        print(f'match found: {data}')

    async def matchmaking(self):
        while len(self.queue) > 0:
            for player in self.queue:
                opponent = self.search_opponent(player)
                if opponent is not None:
                    self.queue.remove(player)
                    self.queue.remove(opponent)
                    await self.send_match_notification(player, opponent)
            await asyncio.sleep(2)

    def search_opponent(self, player):
        match_found = False
        elo_threshold = self.get_elo_threshold(player)
        for opponent in self.queue:
            if opponent == player:
                continue
            if self.elo_gap(player, opponent) < elo_threshold:
                if not match_found:
                    closest_opponent = opponent
                    match_found = True
                elif self.elo_gap(player, opponent) < self.elo_gap(player, closest_opponent):
                    closest_opponent = opponent
        return closest_opponent if match_found else None

    @staticmethod
    def get_elo_threshold(player):
        elapsed_time = time() - player.get('timestamp')
        print(f'elapsed: {elapsed_time}')
        queue_time = elapsed_time / settings.QUEUE_MAX_TIME
        print(f'queue_time: {queue_time}')
        queue_time = min(queue_time, 1)
        print(f'queue_time: {queue_time}')
        elo_threshold = settings.ELO_MAX_THRESHOLD * queue_time
        print(f'elo_threshold: {elo_threshold}')

        return elo_threshold

    @staticmethod
    def elo_gap(player1, player2):
        return abs(player1.get('elo') - player2.get('elo'))