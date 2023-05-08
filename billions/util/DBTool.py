import os
import shutil
from pathlib import Path
from loguru import logger
import MySQLdb
import re
from tqdm import tqdm

logger.add(f"./log/dbtool.log", level="ERROR", rotation="100MB", encoding="utf-8", enqueue=True,
           retention="10 days")
class Dbtool:

    def __init__(self):
        self.con = MySQLdb.connect("localhost", "root", "billions", "billion")
        self.cur = self.con.cursor()

    # 查询url是否重复
    def findUrl(self, table, url):

        sql = "select url from " + table + " where url = '" + url + "'"
        self.cur.execute(sql)
        url = self.cur.fetchone()
        return url

    def findTitle(self, table, url):
        sql = "select itit from " + table + " where itit = '" + url + "'"
        self.cur.execute(sql)
        itit = self.cur.fetchone()
        return itit


    # 对数据库中没有的文件夹，进行清除处理
    def checkWjjFile(self,table,wjjpath,delete=False):
        count = 0
        path = Path().absolute().parent / 'image' / wjjpath
        con = MySQLdb.connect("localhost", "root", "billions", "billion")
        cur = con.cursor()
        databasesieze = tqdm(os.listdir(path))
        for item in databasesieze:
            databasesieze.set_description(wjjpath+"文件扫描进度")
            prarm = (item,)
            cur.execute("select wjj,url from "+table+" where wjj = %s", prarm)
            res = cur.fetchone()
            if res is None:
                logger.error(item + " 没有在数据库中存在！")
                count = count+1
                if delete:
                    shutil.rmtree(path/item)
        print(f"存在{count}条文件夹在数据库中不存在")


    # handling 为9位数 900001111
    #   第一位为占位符
    #   第二位表示 翻译为英文
    #   第三位表示 翻译为中文
    #   第四位表示 文章已清理
    #   第五位表示 WJJ已清理
    def checkPage(self,table,wjjPath):

        con = MySQLdb.connect("localhost", "root", "billions", "billion")

        cur = con.cursor()
        finish = False
        cur.execute(
            "select count(url) from " + table + " where handling is null or  substr(handling,8,1)= 0 ")
        res = cur.fetchone()
        pbar = tqdm(total=res[0])
        pbar.set_description("数据库的文件夹处理进度")
        while not finish:
            res = cur.execute(
                "select itit,url,ihtml,wjj,handling from "+table+" where handling is null or  substr(handling,7,1)= 0 limit 100 for update")
            if res == 0 :
                finish = True
            pbar.update(res)
            for row in cur :
                tit = row[0]
                url = row[1]
                html = row[2]
                wjj = row[3]
                handling = row[4]
                #  如果这条数据没有wjj信息的的话，文章中也不应该有img。 确定文章中有没有img，如果有img，那么删除该文章
                if not wjj:
                    if "<img" in html:
                        prarm = (url,)
                        logger.error(wjj + "信息不存在, 但是居然在html正文中存在img :" + tit)
                        cur.execute("delete  baike_baidu_new  where url = %s", prarm)
                        con.commit()
                else:
                    # 如果这条数据有wjj信息，可磁盘实际没有该wjj的文件夹，那么删除该文章。
                    path = Path().absolute().parent / 'image' / wjjPath / wjj
                    exit = os.path.exists(path)
                    if not exit:
                        prarm = (url,)
                        logger.error(wjj + "在磁盘上不存在，数据库中又存在该wjj的信息 :" + tit)
                        cur.execute("delete  "+table+"  where url = %s", prarm)
                        con.commit()
                    # 如果这条数据有wjj信息，磁盘实际也有该wjj的文件夹，现在需要检查文章中的img在wjj中实际存在不，如果不存在，需要删除html中的img
                    if exit:
                        needUpdateDB = False
                        #<img alt ="奥迪,大众,奔驰,世纪,现代" src="/eeimg/{HostI}/img/20230315224520305158/6.jpg "/>
                        result =re.findall(r'(\d+.jpg)',html)
                        for res in result:
                            # 看文件夹中存在该图片不，如果不存在，删除文章中的该img
                            if res not in os.listdir(path):
                                html = re.sub("<img(.*?)/>", "", html)
                                needUpdateDB = True
                        if needUpdateDB:
                            logger.error("文章中存在img标签，没有成功下载到文件夹的情况" + tit)
                            prarm = (html,url)
                            cur.execute("update  "+table+" set ihtml = %s where url = %s", prarm)
                            con.commit()
                if handling is None or len(str(handling)) < 9 :
                    handling =  "900000000"
                prarm = (url,)
                strs = list(str(handling))
                strs[6] = "1"
                handling = "".join(strs)
                cur.execute("update  "+table+" set handling = "+handling+" where url = %s", prarm)
                con.commit()

    def moveTable(self):
        from loguru import logger
        logger.add(f"dbmove.log", level="INFO", rotation="100MB", encoding="utf-8", enqueue=True, retention="10 days")
        con = MySQLdb.connect("localhost", "root", "billions", "billion")

        accdbId = 1
        cur = con.cursor()
        path = r"F:\billionsData\kong.com_list_"+ str(accdbId)+".accdb"
        accdb = Accdb(path)

        tables = ["inews_xcar","inews_huanqiu","inews_hexun","inews_gasgoo","inews_d1ev","inews_autotimes","inews_autohome","inews"]
        itemCount = 1

        for table in tables:
            print(table)
            cur.execute(
                "select sname,lei11,lei22,itit,ihtml,rq,px,wjj,wjj,lai,h1,ikey,imiao,biaoq,xian,ihtml_zh from " + table)
            fetchall = cur.fetchall()
            pbar = tqdm(total= cur.rowcount)
            for i,res in enumerate(fetchall):
                itemCount = itemCount+1
                if itemCount % 60000 == 0:
                    try:
                        accdb.close()
                        accdbId = accdbId+1
                        cur = con.cursor()
                        path = r"F:\billionsData\kong.com_list_" + str(accdbId) + ".accdb"
                        accdb = Accdb(path)
                    except:
                        pass
                sname = res[0]
                lei11 = res[1]
                lei22 = res[2]
                itit  = res[3]
                ihtml = res[4]
                rq = res[5]
                px = res[6]
                itme = res[7]
                wjj = res[8]
                lai = res[9]
                h1 = res[10]
                ikey = res[11]
                imiao = res[12]
                biaoq = res[13]
                xian = res[14]
                ihtml_zh = res[15]


                if ihtml_zh is None:
                    ihtml_zh = ihtml
                if itit is None or ihtml_zh is None or ikey is None or imiao is None or biaoq is None:
                    continue

                ihtml_zh = ihtml_zh.replace("'", "''")
                imiao = imiao.replace("'", "''")
                itit = itit.replace("'", "''")
                qry_select =""
                try:
                    qry_select = "insert into inews (itit,ihtml,wjj,ikey,imiao,biaoq) values ('%s','%s','%s','%s','%s','%s')"%(itit,ihtml_zh,wjj,ikey,imiao,biaoq)
                    accdb.execute(qry_select)
                    accdb.commit()
                    pbar.update(1)
                except Exception  as ex:
                    print(qry_select)
                    print(ex)
        accdb.close()

    def lei(self):
        pass
        path = r"F:\billionsData\kong.com.accdb"
        accdb = Accdb(path)

        carList = CsvUtil.getCar()
        for car in carList:
            qry_select = "insert into lei (lei11,yiid) values ('%s','%s')" % (car[0],1)
            accdb.execute(qry_select)
            accdb.commit()

        venderList =CsvUtil.getVender()
        for vender in venderList:
            qry_select = "insert into lei (lei11,yiid) values ('%s','%s')" % (vender[0],0)
            accdb.execute(qry_select)
            accdb.commit()

db = Dbtool()
db.checkWjjFile("inews_hexun", "hexun")
# db.checkPage("baike_baidu_new", "baike")
