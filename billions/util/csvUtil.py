from pathlib import Path

import pandas as pd
import numpy as np


class CsvUtil:

    def __init__(self):

        path = Path().absolute() / 'util' / 'car.csv'
        self.csv_data = pd.read_csv(path)
        self.brand_name_ = self.csv_data.loc[:,["CarBrandName","VendorName"]]
        print(self.brand_name_)


    def findTag(self,htmlCount,tagNum=5):

        name_ = np.array(self.brand_name_).tolist()

        str = htmlCount

        dict = {}
        # 查找文章中出现的次数
        for csv_datum in name_:

            dict[csv_datum[0]]= str.count(csv_datum[0])
            dict[csv_datum[1]]= str.count(csv_datum[1])

        resultDic = sorted(dict.items(),key = lambda x:x[1],reverse=True)

        newDic = {}
        # 排序
        for res in resultDic :
            if(res[1] > 0):
                newDic.update({res[0]:res[1]})
        #只取前三个
        theList = list(newDic)[:tagNum]

        res =""
        for i in theList:
            res += i +","

        res= res.rstrip(",")
        return  res

#  单例模式
CsvUtil = CsvUtil()



