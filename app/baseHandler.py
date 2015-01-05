#coding=utf-8#coding=utf-8

import os
from hashlib import md5
import tornado.web
import tornado.websocket
from mako.template import Template
from mako.lookup import TemplateLookup
from libs.utils import *
#from models.models import *
#from libs.memcached import Memcached as mc

def none_to_blank(value):
	if value is None:
		return ""
	return value

def truncatewords(s, num=200, end_text='...'):
	length = int(num)
	if len(s) > length:
		s = s[:length]
		if not s[-1].endswith(end_text):
			s= s+end_text
	return s

#用了HTMLParser，有更简单的方式吗？正则？
def filter_html(html):
    from HTMLParser import HTMLParser
    html = html.strip()
    html = html.strip("\n")
    result = []
    parser = HTMLParser()
    parser.handle_data = result.append
    parser.feed(html)
    parser.close()
    return ''.join(result)

class BaseHandler(tornado.web.RequestHandler):
	"""docstring for BaseHandler"""
	lookup = TemplateLookup(["./templates"], 
		input_encoding = 'utf-8',
		output_encoding = 'utf-8',
		default_filters=["none_to_blank", "unicode"],
		imports=['from apps.basehandler import none_to_blank', 
				'from apps.basehandler import truncatewords',
				'from apps.basehandler import filter_html',
				'from libs.utils import formatdate',
				'from libs.utils import tNow'])

	def render(self, templatename, **args):
		# print 'args:', args
		#t = tNow()
		r = self.lookup.get_template(templatename + '.html')
		content = r.render(**args)
		self.write(content)
		self.flush()

		#print 'render',templatename, tNow() -t

		# if self.request.method == 'GET' and not self.request.path.startswith('/manager'):
		# 	mc.set(self.request.uri, content)
		pass

	def result(self, msg, tourl, issuccessed = True):
		flag = 'success' if issuccessed else 'error'
		return self.render('/manager/result', flag = flag, msg = msg, tourl = tourl)	

	def prepare(self):
		super(BaseHandler, self).prepare()
		# if self.request.method == 'GET' and not self.request.path.startswith('/manager'):
		# 	cache = mc.get(self.request.uri)
		# 	if cache:
		# 		return self.finish(cache)
		pass

	def on_finish(self):
		# if self.request.method == 'POST':
		# 	mc.clear()
		# 	pass
		pass

	# def get_current_user(self):
	# 	name =  self.get_secure_cookie('username')
	# 	pwd  = self.get_secure_cookie('userpw')

	# 	if name and pwd:
	# 		user = ModelSession(User).get_one(username = name, password = pwd)
	# 		return user
	# 	return None

	# def set_current_user(self, user, rememberPwd = False):
	# 	expires_days = 7 if rememberPwd else None
	# 	self.set_secure_cookie('username', user.username, path="/", expires_days = expires_days, httponly = True)
	# 	self.set_secure_cookie('userpw', user.password, path="/", expires_days = expires_days, httponly = True)
	# 	pass

		