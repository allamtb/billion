from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

options = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images":2}
options.add_experimental_option("prefs",prefs)

s =Service("chromedriver.exe")
driver = webdriver.Chrome(service=s,chrome_options=options)


#driver.get("https://search.xcar.com.cn/infosearch.php#?page=999&searchValue=%E5%A5%94%E9%A9%B0&limited=100")
driver.get("http://www.baidu.com")


print(driver.page_source)

sleep(30000)





