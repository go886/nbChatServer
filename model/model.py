#coding=utf-8

import time
import json
from hashlib import md5
import torndb
from config import theConfig
from libs.utils import *
mdb = torndb.Connection(host = "%s:%s"%(theConfig.db_host,str(theConfig.db_port)),
                        database = theConfig.db_name,
                        user = theConfig.db_user,
                        password = theConfig.db_passwd,
                        max_idle_time = theConfig.db_timeout)
sdb = torndb.Connection(host = "%s:%s"%(theConfig.db_host,str(theConfig.db_port)),
                        database = theConfig.db_name,
                        user = theConfig.db_user,
                        password = theConfig.db_passwd,
                        max_idle_time = theConfig.db_timeout)

def defaultmodel(func):
    def _dec(obj, *args, **kwargs):
        result = func(obj, *args, **kwargs)
        if not result:
            result = obj.model()
        return result
    return _dec

class BaseModel(object):
    """docstring for BaseModel"""

    def __init__(self):
        super(BaseModel, self).__init__()
        pass

    def model(self):
        if theConfig.db_type == 'sqlite':
            fields = sdb.query("PRAGMA table_info(" + self.tablename + ")")
            return dict_to_object(dict([[x.name, ""] for x in fields]))
        elif theConfig.db_type == 'mysql':
            fields = sdb.query("show columns from " + self.tablename)
            return dict_to_object(dict([[x.Field, ""] for x in fields]))
        else:
            pass    

    def get_all(self):
        try:
            return [x for x in sdb.query('select * from ' + self.tablename)]
        except IndexError:
            pass

    def count(self):
        return sdb.query('select count(*)  as total from ' + self.tablename)[0]['total']    

class TableMgr(BaseModel):
    """docstring for TableMgr"""
    def gettableinfo(self):
        sql = "SELECT TABLE_NAME,TABLE_ROWS FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA='%s';" %(theConfig.db_name)
        return mdb.query(sql)

    def deletetable(self, tname):
        sql = 'DROP TABLE %s;'%(tname)
        return mdb.execute(sql)

    def cleartable(self, tname):
        sql = 'delete from %s;' %(tname)
        return mdb.execute(sql)

theTableMgr = TableMgr()
        

class KeyValue(BaseModel):
    """docstring for KeyValue"""
    def __init__(self,tablename = 'tb_keyvalue'):
        super(KeyValue, self).__init__()
        self.tablename = tablename
        sql = """
        CREATE TABLE IF NOT EXISTS `%s` (
            `s_key` varchar(64) NOT NULL,
            `s_value` text,
            UNIQUE KEY `s_key` (`s_key`) USING BTREE
        ) ENGINE=MyISAM DEFAULT CHARSET=utf8 ;
        """%(self.tablename)
        mdb.execute(sql)

    def makekey(self, skey):
        return toUtf8(skey)
        return md5(toUtf8(skey)).hexdigest()

    def get(self, skey):
        key = self.makekey(skey)
        sql = "SELECT * FROM " + self.tablename + " WHERE s_key = %s;"
        results = sdb.get(sql, key)
        if results:
            return results['s_value']

    def get_all_to_dic(self):
        results = self.get_all()
        if results:
            outdict = {}
            for item in results:
                outdict[item['s_key']] = item['s_value']
            return outdict
        pass

    def put(self, skey, svalue):
        self.clear(skey)
        sql = 'INSERT INTO ' + self.tablename +' (s_key, s_value) VALUES(%s, %s);'
        return mdb.execute(sql, self.makekey(skey), toUtf8(svalue))

    def puts(self, **agrs):
        for item in agrs:
            self.clear(item)
            self.put(item, agrs[item])

    def clear(self, skey):
        key = self.makekey(skey)
        sql = 'DELETE FROM '+ self.tablename +' WHERE s_key = %s;'
        return mdb.execute(sql, key)

    def clearall(self):
        sql = 'DELETE FROM %s;'%(self.tablename)
        return mdb.execute(sql)

    def isexist(self, skey):
        if self.get(skey):
            return True
        return False    
        
theCache = KeyValue()

class User(BaseModel):
    """docstring for User"""
    def __init__(self):
        super(User, self).__init__()
        self.tablename = 'tb_user'
        #sql = "CREATE TABLE IF NOT EXISTS 'tb_user' ('id' smallint(6) unsigned NOT NULL AUTO_INCREMENT, 'name' varchar(32) NOT NULL DEFAULT '', 'password' varchar(32) NOT NULL DEFAULT '', PRIMARY KEY ('id') ) ENGINE=MyISAM DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;"
        sql = """
            CREATE TABLE IF NOT EXISTS `tb_user` (
            `user_id` varchar(64) NOT NULL UNIQUE,
            `user_name` varchar(32) NOT NULL,
            `user_pwd` varchar(32) NOT NULL DEFAULT '',
            `user_nick` varchar(32) NOT NULL DEFAULT 'user',
            `user_logo` text,
            PRIMARY KEY (`user_id`)
            ) ENGINE=MyISAM DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;
        """
        mdb.execute(sql)
        if not self.has_user():
            self.add_new_user('admin', 'admin')
            pass
        pass

    @staticmethod
    def user_name_to_id(name):
        return md5(toUtf8(name)).hexdigest()

    def has_user(self):
        return self.count() > 0    

    def get_user(self, name, pw, isencrpty = False):
        if name and pw:
            user = self.get_user_by_name(name)
            if user:
                pwd = pw
                if not isencrpty:
                    pwd = md5(toUtf8(pw)).hexdigest()
                if user.user_name == name and user.user_pwd == pwd:
                    del user['user_pwd']
                    return user
        return None

    def get_user_by_name(self, name):
        try:
            sql = 'SELECT * FROM tb_user WHERE user_id=%s;'
            return sdb.get(sql, User.user_name_to_id(name))
        except IndexError:
            pass
        pass

    def get_user_by_id(self, user_id):
        sql = 'SELECT* FROM tb_user WHERE user_id=%s;'
        return sdb.get(sql, user_id)
        pass

    def add_new_user(self, name = '', pw = ''):
        if name and pw:
            try:
                user_id = User.user_name_to_id(name)
                pwd = md5(toUtf8(pw)).hexdigest()
                sql = 'INSERT INTO tb_user (user_id, user_name, user_pwd) VALUES(%s,%s,%s);'
                return mdb.execute(sql, user_id, name, pwd)
            except IndexError:
                pass
        pass

    def isexist_user(self, name = '', pw = '', isencrpty = False):
        user = self.get_user(name, pw, isencrpty)
        return user

theUser = User()

class Friend(BaseModel):
    """docstring for Friend"""
    def __init__(self):
        super(Friend, self).__init__()
        self.tablename = 'tb_friends'
        sql = """
            CREATE TABLE IF NOT EXISTS `tb_friends` (
            `user_id_a` varchar(64) NOT NULL,
            `user_id_b` varchar(64) NOT NULL,
            CONSTRAINT `tb_friends_ibfk_1` FOREIGN KEY (`user_id_a`) REFERENCES `tb_user` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE,
            CONSTRAINT `tb_friends_ibfk_2` FOREIGN KEY (`user_id_b`) REFERENCES `tb_user` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE
            ) ENGINE=MyISAM DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;
        """
        mdb.execute(sql)
        pass

    def add_friend(self, user_id_a, user_id_b, together = False):
        try:
            sql = 'INSERT INTO ' + self.tablename +' (user_id_a, user_id_b) VALUES(%s, %s);'
            mdb.execute(sql, user_id_a, user_id_b)
            if together:
                mdb.execute(sql, user_id_b, user_id_a)
        except Exception, e:
            pass
        pass
        
    def remove_friend(self, user_id_a, user_id_b, together = False):
        sql = 'DELETE FROM %s '%(self.tablename) + 'WHERE user_id_a=%s and user_id_b = %s;'
        mdb.execute(sql, user_id_a, user_id_b)
        if together:
            mdb.execute(sql, user_id_b, user_id_a)
        pass

    def get_friends(self, user_id):
        try:
            sql = 'SELECT * FROM tb_user WHERE user_id in (SELECT user_id_b as user_id FROM tb_friends WHERE user_id_a = %s);'
            return [x for x in sdb.query(sql, user_id)]
        except IndexError:
            pass

theFriends = Friend()

class Msg(BaseModel):
    """docstring for Msg"""
    def __init__(self):
        super(Msg, self).__init__()
        self.tablename = 'tb_msg'
        sql = """
            CREATE TABLE IF NOT EXISTS `tb_msg` (
            `id` int(11) NOT NULL AUTO_INCREMENT,
            `send_user_id` varchar(64) NOT NULL,
            `receive_user_id` varchar(64) NOT NULL,
            `time` int(24) unsigned NOT NULL DEFAULT '0',
            `msg` text,
            `flag` tinyint(1) NOT NULL DEFAULT '0',
            PRIMARY KEY (`id`)
            ) ENGINE=MyISAM DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;
        """
        mdb.execute(sql)
        pass

    def add_msg(self, send_user_id, receive_user_id, msg):
        sql = 'INSERT INTO tb_msg (send_user_id, receive_user_id, time, msg) VALUES(%s,%s,%s,%s)'
        return mdb.execute(sql, send_user_id, receive_user_id, time.time(), msg)

    def remove_msg(self, msg_id):
        sql = 'DELETE FROM tb_msg WHERE id =%s;'
        return mdb.execute(sql, msg_id)

    def get_msg(self, receive_user_id, flag = 0):
        try:
            sql = 'SELECT * FROM tb_msg WHERE receive_user_id = %s and flag = %s;'
            return [x for x in sdb.query(sql, receive_user_id, flag)]
        except IndexError:
            pass
        pass
      
theMsg = Msg()  
