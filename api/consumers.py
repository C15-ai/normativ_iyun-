import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):

    def connect(self):
        self.room_group_name = "chat"

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "send_message",
                "message": data["message"]
            }
        )

    def send_message(self, event):
        self.send(text_data=json.dumps({
            "message": event["message"]
        }))