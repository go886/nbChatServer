#coding=utf-8
from basehandler import *
from libs.utils import *
from message import *

class Test(BaseHandler):
	"""docstring for Test"""
	def get(self):
		self.render('test')
		pass
		

class BaseWebSocket(tornado.websocket.WebSocketHandler):
	"""docstring for BaseWebSocket"""
	def open(self):
		self.user_token = None
		print 'connect...'
		pass

	def islogin(self):
		return self.user_token != None
		pass

	def on_close(self):
		print 'close...'
		#self.write_message('close')
		SessionManager.instance().remove(self.user_token)
		pass
						
	def on_message(self, message):
		print 'msg:', message
		MessageDispatcher.instance().dispatch(self, message)
		pass
