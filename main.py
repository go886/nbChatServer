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


# from apps.handler import *
# from apps.manager import *
from config import theConfig


define("port", default=8080, help="run on the given port", type=int)

settings = dict(
    debug=theConfig.is_debug,
    static_path=os.path.join(os.path.dirname(__file__), "static"),
    login_url="/admin/login",
    cookie_secret="61oETzKXQAGaYdkL5gEmGeJJFu6754Qnp2XdTP1o/Vo=",
)

urls = [
	# (r'/test', Test),
	# (r'/test/chat', TestChat),
]

if __name__ == '__main__':
	tornado.options.parse_command_line()
	app = tornado.web.Application(urls,**settings)
	app.listen(options.port)
	print 'listen....',options.port
	tornado.ioloop.IOLoop.instance().start()