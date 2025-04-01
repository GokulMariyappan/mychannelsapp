import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

class MyConsumer(WebsocketConsumer):
	def connect(self):
		self.room_group_name = 'messageroom'
		async_to_sync(self.channel_layer.group_add)(self.room_group_name,self.channel_name)
		self.accept()
		self.send(text_data=json.dumps({'message' : 'socket connected to the server!'}))
	 
	def receive(self, text_data):
		recieved_data = json.loads(text_data)
		message = recieved_data['message']
		async_to_sync(self.channel_layer.group_send)(self.room_group_name,{
			'type' : 'chat_message',
			'message' : message
		})
	
	def chat_message(self, event):
		print(event)
		message = event['message']
		self.send(json.dumps({'type' : 'chat', 'message' : message}))