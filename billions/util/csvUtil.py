from pathlib import Path

import pandas as pd
import numpy as np
from shutil import which


class CsvUtil:

    def __init__(self):

        path = "F:\\billions\\billions\\util\\car.csv"
        self.csv_data = pd.read_csv(path)
        self.brand_name_ = self.csv_data.loc[:, ["CarBrandName", "VendorName"]]
        print(self.brand_name_)

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


#  单例模式
CsvUtil = CsvUtil()

print(CsvUtil.findTag("长安"))
