import os
from pathlib import Path

import MySQLdb

class Dbtool:

      def __init__(self):
            self.con = MySQLdb.connect("localhost", "root", "billions", "billion")
            self.cur = self.con.cursor()

      # 查询url是否重复
      def findUrl(self,table,url):

            sql = "select url from " + table + " where url = '" + url + "'"
            self.cur.execute(sql)
            url  = self.cur.fetchone()
            return url

      def findTitle(self,table,url):
            sql = "select itit from " + table + " where itit = '" + url + "'"
            self.cur.execute(sql)
            itit  = self.cur.fetchone()
            return itit


      # 对实际上没有文件夹的数据库字段进行置空处理
      def cheWjj(self):
            con = MySQLdb.connect("localhost", "root", "billions", "billion")
            cur = con.cursor()
            cur.execute("select wjj,url from inews ")
            i = 0
            for row in cur:

                  path = Path().absolute().parent / 'image' / 'd1ev' / row[0]
                  exit = os.path.exists(path)
                  if not exit:
                        i = i + 1
                        prarm = (row[1],)
                        print(str(path) + ":" + str(exit) + ":" + str(i) + ":" + row[1])
                        cur.execute("update  inews set wjj = '' where url = %s", prarm)
                        con.commit()

      # 对数据库中没有的文件夹，进行清除处理
      def checkWjj(self):

            path = Path().absolute().parent / 'image' / 'd1ev'
            con = MySQLdb.connect("localhost", "root", "billions", "billion")
            cur = con.cursor()
            for item in os.listdir(path):
                  prarm = (item,)
                  cur.execute("select wjj,url from inews where wjj = %s" ,prarm)
                  res = cur.fetchone()
                  if res is None:
                        print(item +" is null")


db = Dbtool()
# print(db.findUrl("inews_xcar","https://info.xcar.com.cn/200804/news_29579_1.html"))
# print(db.findTitle("inews_xcar","经销商“变”用户实践广汽日野品质"))