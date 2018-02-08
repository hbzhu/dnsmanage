# -*- coding: utf-8 -*-
"""
__author__ = 'Frank'
__mtime__ = '2018/2/8'
"""
import MySQLdb
import MySQLdb.cursors
from dnsmanage import settings

class database:
    def __init__(self, dbname=None, dbhost=None):
        self._dbhost = settings.db_host
        self._dbname = settings.db_name
        self._dbuser = settings.db_user
        self._dbpassword = settings.db_password
        self._dbcharset = 'utf8mb4'
        self._dbport = int(settings.db_port)
        self._conn = self.connectMySQL()

        if (self._conn):
            self._cursor = self._conn.cursor()

    # 连接
    def connectMySQL(self):
        conn = False
        try:
            conn = MySQLdb.connect(host=self._dbhost,
                                   user=self._dbuser,
                                   passwd=self._dbpassword,
                                   db=self._dbname,
                                   port=self._dbport,
                                   cursorclass=MySQLdb.cursors.DictCursor,
                                   charset=self._dbcharset,
                                   )
        except Exception, data:
            print data
            conn = False
        return conn

    # 查询
    def fetch_all(self, sql):
        res = ''
        if (self._conn):
            try:
                self._cursor.execute(sql)
                res = self._cursor.fetchall()
            except Exception, data:
                res = False
        return res

    # 更新
    def update(self, sql):
        flag = False
        if (self._conn):
            try:
                self._cursor.execute(sql)
                self._conn.commit()
                flag = True
            except Exception, data:
                flag = False


        return flag

    # 关闭连接
    def close(self):
        if (self._conn):
            try:
                if (type(self._cursor) == 'object'):
                    self._cursor.close()
                if (type(self._conn) == 'object'):
                    self._conn.close()
            except Exception, data:
                print data