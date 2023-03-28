import re

import pandas as pd
import numpy as np

from billions.util.RichSelenium import baidubaikeFix
from billions.util.htmlUtil import getChineseWord


class CsvUtil:

    def __init__(self):

        path = "F:\\billions\\billions\\util\\car.csv"
        self.csv_data = pd.read_csv(path)
        self.brand_name_ = self.csv_data.loc[:, ["CarBrandName", "VendorName"]]
        self.VendorName = self.csv_data.loc[:, ["VendorName"]]

        print(self.brand_name_)

    def getVenderByCar(self,key):

        vender = self.brand_name_.loc[self.brand_name_['CarBrandName'] == key]
        x =np.array(vender).tolist()
        if x:
            return x[0][1]
        else:
            return None


    def getCarList(self):

        brand_name_ = self.csv_data.loc[:, ["CarBrandName"]]
        VendorName = self.csv_data.loc[:, ["VendorName"]]

        brand_list = np.array(brand_name_).tolist()  # type: list
        vendor_list = np.array(VendorName).tolist()

        resultList = []

        for brand in brand_list:
            resultList.append(brand[0])

        for vendor in vendor_list:
            resultList.append(vendor[0])

        return resultList

    def findTag(self, htmlCount, tagNum=5):

        name_ = np.array(self.brand_name_).tolist()

        str = htmlCount

        dict = {}
        # 查找文章中出现的次数
        for csv_datum in name_:
            dict[csv_datum[0]] = str.count(csv_datum[0])
            dict[csv_datum[1]] = str.count(csv_datum[1])

        resultDic = sorted(dict.items(), key=lambda x: x[1], reverse=True)

        newDic = {}
        # 排序
        for res in resultDic:
            if (res[1] > 0):
                newDic.update({res[0]: res[1]})
        # 只取前三个
        theList = list(newDic)[:tagNum]

        res = ""
        for i in theList:
            res += i + ","

        res = res.rstrip(",")
        return res


    def getCar(self):

        return  np.array(self.brand_name_).tolist()
    def getVender(self):
        vender = self.VendorName.drop_duplicates()
        return  np.array(vender).tolist()

    def fixCsvCarName(self):
        car = []
        with open("F:/baikeError.log", 'r', encoding='utf-8') as file:
            lines = file.readlines()
            for line in lines:
                if 'Spider error processing <GET' in line:
                    sch = re.search("<GET (.*?)>", line)
                    html = sch.group(1)
                    if 'item/' in html:
                        res = re.search("item/(.*?)[\?|target]", line).group(1)
                        word = getChineseWord(res)
                    else:
                        res = re.search("word=(.*?)&", line).group(1)
                        word = getChineseWord(res)
                    # 通过selenium调用百度百科的自动提示补全搜索关键字
                    word = baidubaikeFix(word)
                    if word is None:
                        continue
                    url = "https://baike.baidu.com/item/" + word

                    if word in self.getVender():
                        car.append((word, '', '', url))
                    else:
                        vendor = self.getVenderByCar(word)
                        car.append((word, '', vendor, url))
                    print(word)
                    print(car)
        return car


#  单例模式
CsvUtil = CsvUtil()
#
# print(CsvUtil.getCarList().index('极狐 阿尔法T'))
# # #print(CsvUtil.getCarList())
# CsvUtil.getCar()
# print(CsvUtil.getVender())
#
# print(CsvUtil.getVenderByCar("桑塔纳"))
