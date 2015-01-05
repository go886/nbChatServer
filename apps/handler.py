#coding=utf-8
from basehandler import *

class BaseWebSocket(tornado.websocket.WebSocketHandler):
	"""docstring for BaseWebSocket"""
	def open(self):
		print 'connect...'
		self.write_message('a')
		pass

	def on_close(self):
		print 'close...'
		#self.write_message('close')
		pass
						
	def on_message(self, msg):
		print 'msg:', msg
		self.write_message(msg)
		pass


class Test(BaseHandler):
	"""docstring for Test"""
	def get(self):
		self.render('test')
		pass