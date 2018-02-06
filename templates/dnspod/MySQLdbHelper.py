
#encoding:utf-8
#name:MySQLdbHelper.py
'''
使用方法：1.在主程序中先实例化DB Mysql数据库操作类。
      2.使用方法:db=database()  db.fetch_all("sql")
'''
import MySQLdb
import MySQLdb.cursors
import mod_config
import mod_logger

#读取配置文件
DB = "database"    #数据库配置
LOGPATH = mod_config.getConfig('path', 'logpath') + 'database.log'
DBNAME = mod_config.getConfig(DB, 'dbname')
DBHOST = mod_config.getConfig(DB, 'dbhost')
DBUSER = mod_config.getConfig(DB, 'dbuser')
DBPWD = mod_config.getConfig(DB, 'dbpassword')
DBCHARSET = mod_config.getConfig(DB, 'dbcharset')
DBPORT = mod_config.getConfig(DB, "dbport")

logger = mod_logger.logger(LOGPATH)

#数据库操作类
class database:
    def __init__(self, dbname=None, dbhost=None):
        self._logger = logger
        #这里的None相当于其它语言的NULL
        if dbname is None:
            self._dbname = DBNAME
        else:
            self._dbname = dbname
        if dbhost is None:
            self._dbhost = DBHOST
        else:
            self._dbhost = dbhost
            
        self._dbuser = DBUSER
        self._dbpassword = DBPWD
        self._dbcharset = DBCHARSET
        self._dbport = int(DBPORT)
        self._conn = self.connectMySQL()
        
        if(self._conn):
            self._cursor = self._conn.cursor()

    #连接
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
        except Exception,data:
            self._logger.error("connect database failed, %s" % data)
            conn = False
        return conn

    #查询
    def fetch_all(self, sql):
        res = ''
        if(self._conn):
            try:
                self._cursor.execute(sql)
                res = self._cursor.fetchall()
            except Exception, data:
                res = False
                self._logger.warn("query database exception, %s" % data)
        return res

    #更新
    def update(self, sql):
        flag = False
        if(self._conn):
            try:
                self._cursor.execute(sql)
                self._conn.commit()
                flag = True
            except Exception, data:
                flag = False
                self._logger.warn("update database exception, %s" % data)

        return flag

    #关闭连接
    def close(self):
        if(self._conn):
            try:
                if(type(self._cursor)=='object'):
                    self._cursor.close()
                if(type(self._conn)=='object'):
                    self._conn.close()
            except Exception, data:
                self._logger.warn("close database exception, %s,%s,%s" % (data, type(self._cursor), type(self._conn)))