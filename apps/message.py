#coding=utf-8
import sys
import struct
import json
from model.model import *
import time

class SessionManager(object):
	"""docstring for SessionManager"""

	@classmethod
	def instance(cls):
		if not hasattr(cls, '_instance'):
			cls._instance = cls()
		return cls._instance

	def __init__(self):
		#super(SessionManager, self).__init__()
		self.sessions = dict()
	
	def add(self, session, key):
		print 'add key:', key
		oldsession = self.sessions.get(key)
		if oldsession and oldsession != session:
			oldsession.close()
		self.sessions[key] = session
		pass

	def remove(self, *keys):
		for key in keys:
			session = self.sessions.get(key)
			if session:
				session.close()
				del self.sessions[key]
		pass

	def find(self, *keys):
		result = []
		for key in keys:
			session = self.sessions.get(key)
			if session:
				result.append(session)
		return result

	def get(self, key):
		return self.sessions.get(key)
		pass

	def send_msg(self, sender, msg, *receiver):
		if len(receiver):
			sessions = self.find(*receiver)
			for s in xrange(1,10):
				pass
			pass
		pass

class MessageDispatcher(object):
	"""docstring for MessageDispatcher"""
	@classmethod
	def instance(cls):
		if not hasattr(cls, '_instance'):
			cls._instance = cls()
		return cls._instance

	def __init__(self):
		super(MessageDispatcher, self).__init__()
		self.handlers = {}
		pass

	def add(self, msghandler):
		self.handlers[msghandler.cmd] = msghandler
		pass

	def dispatch(self, sesstion, message):
		try:
			infos = json.loads(message)
			cmd = infos.get('cmd')
			if cmd and cmd in self.handlers:
				msg = self.handlers[cmd]
				msg.handler(sesstion, **infos)
				pass
		except Exception, e:
			raise e
			print e	
		pass

def toJson(cmd, **kwags):
	kwags['cmd'] = cmd
	return json.dumps(kwags)
	pass

class Message(object):
	"""docstring for Message"""
	def __init__(self,cmd = None, **kwagrs):
		super(Message, self).__init__()
		self.cmd = cmd
		self.data = kwagrs
		pass

	def islogin(self):
		return False

	def get(self, key):
		return self.data[key] if key in self.data else None

	def __repr__(self):
		return '%s(%r,%r)'%(
			self.__class__.__name__,
			self.cmd,
			self.data)
		pass

	def toJson(self):
		if hasattr(self, 'outjson'):
			return getattr(self, 'outjson')
		outjson = toJson(self.cmd, **self.data)
		setattr(self, 'outjson', outjson)
		return outjson

	def handler(self, session, **infos):
		print 'handler...'
		if self.islogin() or session.islogin():
			self.on_handler(session, **infos)
		pass

	def on_handler(self, session, **infos):
		pass

	def send_msg(self, *receiver, **kwagrs):
		msg = toJson(self.cmd, **kwagrs)
		for s in receiver:
			session = s if not isinstance(s, basestring) else SessionManager.instance().get(s)
			try:
				session.write_message(msg)
				print 'send_msg:', msg
			except Exception, e:
				print 'send msg error:', e
				self.on_send_failed(s, msg, **kwagrs)
			pass
		pass

	def on_send_failed(self, _receiver, _msg, **kwagrs):
		pass

def safeUser(*userlist):
	for user in userlist:
		del user['user_pwd']
		del user['user_name']
		user['online'] = 1 if SessionManager.instance().find(user['user_id']) else 0
		pass
	pass
class LoginMessage(Message):
	"""docstring for LoginMessage"""
	def islogin(self):
		return True

	def on_handler(self, session, user_name, user_pwd, **infos):
		userinfo = theUser.get_user(user_name, user_pwd)
		if userinfo:
			session.user_token = userinfo.user_id
			SessionManager.instance().add(session, session.user_token)
			self.send_msg(session, userinfo = userinfo)
		else:
			self.send_msg(session, error = 'not found')
		pass

class FriendMessage(Message):
	"""docstring for Friend"""
	def on_handler(self, session, op, user_id, **infos):
		if op == 'add':
			user_info = theUser.get_user_by_id(user_id)
			if user_info:
				theFriends.add_friend(session.user_token, user_info.user_id)
				self.send_msg(session, op = op, friend_info = user_info)
			else:
				self.send_msg(session, op = op, error = 'user not found')
			pass
		elif op == 'remove':
			theFriends.remove_friend(session.user_token, user_id)
			self.send_msg(session, op = op)
		pass
		
		
class FriendQueryMessage(Message):
	"""docstring for FriendListMessage"""
	def on_handler(self, session, key, value, **infos):
		pass
	
class ChatMessage(Message):
	"""docstring for ChatMessage"""
	def on_handler(self, session, receiver_user_id, msg = None, **infos):
		self.send_msg(receiver_user_id, msg = msg, send_user_id = session.user_token)
		pass

	def on_send_failed(self, _receiver, _msg, msg, send_user_id):
		theMsg.add_msg(send_user_id, _receiver, msg)
		pass

# class MessageBin(object):
# 	"""docstring for Message"""
# 	def __init__(self, cmd = 0, **kwagrs):
# 		super(Message, self).__init__()
# 		self.cmd = cmd
# 		self.data = json.dumps(kwagrs) if kwagrs else None
# 		pass

# 	def __repr__(self):
# 		return '%s(%r,%r)'%(
# 			self.__class__.__name__,
# 			self.cmd,
# 			self.data)
# 		pass

# 	def pack(self):
# 		if self.data:
# 			datalen = len(self.data)
# 			packlen = 8 + datalen
# 			return struct.pack('ii%ds'%(datalen), packlen, self.cmd, self.data)
		
# 		packlen = 8
# 		return struct.pack('ii', packlen, self.cmd)

# 	@staticmethod
# 	def unpacker(data):
# 		if not data:
# 			return None

# 		fmt = 'ii'
# 		size = struct.calcsize(fmt)
# 		packlen, cmd = struct.unpack(fmt, data[:size])
# 		if len(data) == packlen:
# 			msg = Message(cmd)
# 			msg.data = json.loads(data[size:])
# 			return msg
# 			pass
# 		return None

# if __name__ == '__main__':
# 	msg =  Message(0).pack()
# 	print 'msg:', msg, len(msg)
# 	packet = Message.unpacker(msg)
# 	print 'p:', packet


mgr = MessageDispatcher.instance()
mgr.add(LoginMessage(3))
mgr.add(ChatMessage(4))

if __name__ == '__main__':
	#{"cmd": 3, "user_name":"admin" , "user_pwd": "admin"}
	#{"cmd": 4, "msg":"hello","receiver_user_id": "21232f297a57a5a743894a0e4a801fc3"}
	msg = LoginMessage(3,song = {'song_id':343243}, error = 'a').toJson()
	print msg
	mgr.dispatch(None, msg)

