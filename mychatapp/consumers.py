import json
from channels.generic.websocket import WebsocketConsumer 
from asgiref.sync import async_to_sync

class MyConsumer(WebsocketConsumer):
	def connect(self):
		self.room_group_name = 'messageroom'
		async_to_sync(self.channel_layer.group_add)(self.room_group_name,self.channel_name)
		self.accept()
		print(self.channel_name, self.scope['user'])
		self.send(json.dumps({'message' : 'socket connected to the server!', 'channel_name' : self.channel_name}))
	 
	def receive(self, text_data):
		print(self.channel_name , "recieved a message")
		recieved_data = json.loads(text_data)
		message = recieved_data['message']
		async_to_sync(self.channel_layer.group_send)(self.room_group_name,{
			'type' : 'chat_message',
			'message' : message,
			'sender' : self.channel_name,
			'username' : self.scope['user']
		})
	
	def chat_message(self, event):
		message = event['message']
		if(event['sender'] == self.channel_name):
			self.send(json.dumps({'senderr' : 'me','type' : 'chat', 'message' : message, 'channel_name' : self.channel_name}))
			return
		print(self.channel_name, "this dude sent a message")
		
		self.send(json.dumps({'senderr':f'{event['username']}','type' : 'chat', 'message' : message, 'channel_name' : self.channel_name}))