#coding=utf-8
from basehandler import *

class Login(BaseHandler):
	"""docstring for Login"""
	def get(self):
		self.redirect('/manager/index') if self.get_current_user() else self.render('/manager/login')
		pass

	def post(self):
		try:
			name = self.get_argument("name")
			password = self.get_argument("pwd")
			rememberPassword = self.get_argument('remember-me', False)

			user = ModelSession(User).get_one(username = name, password = md5(toUtf8(password)).hexdigest())
			if user:
				self.set_current_user(user, rememberPwd = bool(rememberPassword))
				self.redirect('/manager/index')
				return
		except Exception, e:
			pass
		self.get()
		pass


class Index(BaseHandler):
	"""docstring for Index"""
		
