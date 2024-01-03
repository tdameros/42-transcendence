import datetime
import json
import asyncio
from time import time

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer

from matchmaking import settings


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
            'timestamp': time(),
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

    @staticmethod
    async def send_match_notification(player1, player2):
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
                    match_found = True
                    closest_opponent = opponent
                else:
                    if self.elo_gap(player, opponent) < self.elo_gap(player, closest_opponent):
                        closest_opponent = opponent
        return closest_opponent if match_found else None

    @staticmethod
    def get_elo_threshold(player):
        elapsed_time = time() - player.get('timestamp')
        queue_time = elapsed_time / settings.QUEUE_MAX_TIME
        queue_time = max(queue_time, 1)
        elo_threshold = settings.ELO_MAX_THRESHOLD * queue_time

        return elo_threshold

    @staticmethod
    def elo_gap(player1, player2):
        return abs(player1.get('elo') - player2.get('elo'))