import requests


# ip =requests.get("http://api.dmdaili.com/dmgetip.asp?apikey=c7b12bad&pwd=1077f02e87c5f50756b41cfe50d871b6&getnum=1&httptype=3&geshi=1&fenge=1&fengefu=&Contenttype=1&operate=2&setcity=cq1")
# # iptable= []
# # if ip.text :
# #     iptable.append(ip.text[:ip.text.index(":")] )
# #     iptable.append(ip.text[ip.text.index(":")+1:] )
# #
# #
# #
# # proxies = {
# #     'http': "http://"+ip.text.strip()
# # }

#response = requests.get('https://img1.xcarimg.com/b5/s10612/846_634_20190602234057197007771947228.jpg', proxies=proxies)

count = 1
for i in range(1,10000,1):


    response = requests.get('https://img1.xcarimg.com/b5/s10612/846_634_20190602234057197007771947228.jpg')
    if response.status_code == 200:
        count = count+1
    print("%d 个 %d"%(i,count))

print(count)