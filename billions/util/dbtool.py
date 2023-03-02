
import MySQLdb

con =MySQLdb.connect("localhost","root","billions","billion")

cur = con.cursor()

cur.execute("select * from inews")

sql = "insert into inews (itit,ihtml,wjj,ikey,imiao,biaoq,url,json) " \
      "values (%s,%s,%s,%s,%s,%s,%s,%s)"

str = "'不知道有没有人疑惑过，所谓特斯拉全球“投资者”（investors），具体指的哪些人？ 特斯拉的股东？买了特斯拉汽车的车主？持有特斯拉股票的投资人？ 实际这些都不是，但也可以说他们“都是”。'"
cur.execute(sql,tuple([1,2,3,4,str,6,7,'[]']))


con.commit()

