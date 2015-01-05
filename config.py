#coding=utf-8

import os
from libs.utils import dict_to_object

__author__ = 'go886<lege2005@qq.com>'
__version__ = '0.0.1beta'
__license__ = 'MIT'


config = {
	'version': __version__,
	'is_debug': False,
	'is_cache': False,
	'cache_time': 60*60*7,
	'data_dir': 'data',
	'upload_dir': 'static/images/',
	'db_type': 'mysql',
	'db_name': 'go886',
	'db_host': 'localhost',
	'db_port': 3306,
	'db_timeout': 60*60*7,
	'db_user': 'root',
	'db_passwd': '8822497',
	'db_prefix': 'go886_',
	'runtime' : 'LOCAL',
	'setting': {} 
}

if 'SERVER_SOFTWARE' in os.environ:
	if os.environ['SERVER_SOFTWARE'] == 'direwolf/1.0':
		import sae.const
		config['runtime'] = 'SAE'
		config['db_type'] = 'mysql'
		config['db_host'] = sae.const.MYSQL_HOST
		config['db_host_s'] = sae.const.MYSQL_HOST_S
		config['db_port'] = int(sae.const.MYSQL_PORT)
		config['db_user'] = sae.const.MYSQL_USER
		config['db_passwd'] = sae.const.MYSQL_PASS
		config['db_name'] = sae.const.MYSQL_DB
		config['db_timeout'] = 10
	elif os.environ['SERVER_SOFTWARE'] == 'bae/1.0':
		from bae.core import const
		config['runtime'] = 'BAE'
		config['db_type'] = 'mysql'
		config['db_host'] = const.MYSQL_HOST
		config['db_port'] = int(const.MYSQL_PORT)
		config['db_user'] = const.MYSQL_USER
		config['db_passwd'] = const.MYSQL_PASS
		config['db_name'] = 'ABCDEDF'
		config['AK'] = 'xxxx'
		config['SK'] = 'xxxx'
	else:
	    config['runtime'] = 'LOCAL'
	    pass
	pass 	

theConfig = dict_to_object(config)
print theConfig['db_type']
print theConfig['runtime']