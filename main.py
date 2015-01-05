#coding=utf-8

import os
import sys
reload(sys)  
sys.setdefaultencoding('utf8')
try:
	import tornado.wsgi
	import tornado.ioloop
	import tornado.web
	import tornado.options
	from tornado.options import define,options
except Exception, e:
	print e

