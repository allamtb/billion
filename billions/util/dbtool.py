import os
from pathlib import Path

import MySQLdb

# 对实际上没有文件夹的数据库字段进行置空处理
def cheWjj():
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
def checkWjj():

      path = Path().absolute().parent / 'image' / 'd1ev'
      con = MySQLdb.connect("localhost", "root", "billions", "billion")
      cur = con.cursor()
      for item in os.listdir(path):
            prarm = (item,)
            cur.execute("select wjj,url from inews where wjj = %s" ,prarm)
            res = cur.fetchone()
            if res is None:
                  print(item +" is null")



checkWjj()