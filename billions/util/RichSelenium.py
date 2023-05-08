import random
import re
import time
import MySQLdb
import pyperclip
from fake_useragent import UserAgent
from threading import Thread
from loguru import logger
from scrapy import Selector
from selenium import webdriver
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.wpewebkit.service import Service
from selenium.webdriver.support.wait import  WebDriverWait
import selenium.webdriver.support.expected_conditions as  EC
from selenium.webdriver.chrome.options import Options as ChromeOption


def baidubaike(key):
    ua = UserAgent()
    ChromeOptions = ChromeOption()
    ChromeOptions.add_argument("--enable-javascript")
    ChromeOptions.add_argument('user-agent=' + ua.chrome)
    ChromeOptions.add_argument('javascript.enabled')
    # options.add_argument('--headless')
    # s = Service("F:\chromedriver.exe")
    driver = webdriver.Chrome(options=ChromeOptions)
    # driver = webdriver.Firefox()
    driver.get("https://baike.baidu.com/item/%E5%90%88%E5%88%9B%E6%B1%BD%E8%BD%A6?fromModule=lemma_search-box")
    logger.add(f"./log/baikeNew.log", level="ERROR", rotation="100MB", encoding="utf-8", enqueue=True,
               retention="10 days")
    elementInput = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.ID, 'query')))
    elementInput.send_keys(key)
    elementSearch = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.ID, 'search')))
    elementSearch.click()
    try:
        eleCorrect = WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='spell-correct']")))
        if eleCorrect:

            html = eleCorrect.get_attribute("outerHTML")
            res = re.search('href="(.*?)">', html)
            if res and res.group(1):
                link = "https://baike.baidu.com" + res.group(1)
                logger.error(key+"无法检索到, 修为为 is Crorrect to " + link)
                return link
    except:
        print("no need check spell")

    #  先要判断是否存在
    try:
        elementCollaps = WebDriverWait(driver, 0.5).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'toggle')]")))
        elementCollaps.click()
    except:
        print("no need toggle check element ")

    try:
        elementList = WebDriverWait(driver, 0.5).until(EC.presence_of_element_located((By.XPATH, '//div[contains(@class,"polysemant-list")]')))
        items = elementList.find_elements(By.CLASS_NAME,"item")
        for item in items:
            if "车" in item.text:
                html = item.get_attribute("outerHTML")
                res =re.search('href="(.*?)">',html)
                if res and res.group(1):
                    link = "https://baike.baidu.com" + res.group(1)
                    logger.info(key + "is Relating to " + link)
                    return link
    except:
        print("only one element")

    logger.info(key + "is Relating to " + driver.current_url)

    try:
        elementClear = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//em[@class='cmn-icon cmn-icons cmn-icons_clear input-clear J-input-clear']")))
        elementClear.click()
    except:
        # for i in range(20):
        #     elementSearch.sendKeys(Keys.BACK_SPACE)
        logger.error(driver.current_url + "need check,cann't click clear" )
        elementInput.clear()
        print("cann't click ")

    return driver.current_url

def baidubaikeFix(key):
    ua = UserAgent()
    ChromeOptions = ChromeOption()
    ChromeOptions.add_argument("--enable-javascript")
    ChromeOptions.add_argument('user-agent=' + ua.chrome)
    ChromeOptions.add_argument('javascript.enabled')
    # options.add_argument('--headless')
    # s = Service("F:\chromedriver.exe")
    driver = webdriver.Chrome(options=ChromeOptions)
    driver.get("https://baike.baidu.com/item/%E5%90%88%E5%88%9B%E6%B1%BD%E8%BD%A6?fromModule=lemma_search-box")
    elementInput = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.ID, 'query')))
    elementInput.clear()
    elementInput.send_keys(key)
    chains = ActionChains(driver)
    chains.move_to_element(elementInput).double_click().click_and_hold().pause(3)
    elements = driver.find_element(By.XPATH, '//ul[@id="suggestion"]')
    chains.perform()
    html= elements.get_attribute("outerHTML")

    divs = Selector(text=html).xpath("//div[@class='sug-lemma_item-content']").getall()
    for div in divs:
        if "车" in div or  "公司" in div or "集团" or "品牌" in div:
            res = re.search('title">(.*?)</div>',div)
            return res.group(1)

    try:
        elementClear = WebDriverWait(driver, 5).until(EC.presence_of_element_located(
            (By.XPATH, "//em[@class='cmn-icon cmn-icons cmn-icons_clear input-clear J-input-clear']")))
        elementClear.click()
    except:
        # for i in range(20):
        #     elementSearch.sendKeys(Keys.BACK_SPACE)
        logger.error(driver.current_url + "need check,cann't click clear")
        elementInput.clear()
        print("cann't click ")

    logger.error(key + "  cann't find " + html)
    return None



def baidufanyi():
        ua = UserAgent()
        options = webdriver.ChromeOptions()
        options.add_argument("--enable-javascript")
        options.add_argument('user-agent=' + ua.chrome)
        options.add_argument('javascript.enabled')
        # options.add_argument('--headless')
        driver = webdriver.Chrome(chrome_options=options)

        element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'app-guide-close')))
        element.click()
        elementInput = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'baidu_translate_input')))

        elementInput.send_keys("please translate IT")
        driver.execute_script("window.scrollTo(0,0)", "")
        delay = 1
        ranDelay = random.uniform(0.5 * delay, 1.5 * delay)
        time.sleep(ranDelay)

        out = driver.find_element(By.XPATH, '//div[@class="trans-right"]')
        # outElement = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CLASS_NAME, 'ordinary-output source-output')))
        x = out.text.replace("\n笔记\n双语对照", "")
        delay = 2
        ranDelay = random.uniform(0.8 * delay, 1.5 * delay)
        time.sleep(ranDelay)
        print(x)
        WebDriverWait(driver,5).until(EC.presence_of_element_located((By.CLASS_NAME, 'textarea-clear-btn'))).click()


def bing():
    options = webdriver.ChromeOptions()
    # prefs = {"profile.managed_default_content_settings.images":2}
    # options.add_experimental_option("prefs",prefs)
    options.add_argument("--enable-javascript")
    # options.add_argument('user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"')
    options.add_argument('javascript.enabled')
    # options.add_argument('--headless')
    # s = Service("F:\chromedriver.exe")
    driver = webdriver.Chrome(chrome_options=options)
    driver.get("https://cn.bing.com/search?q=%E7%BF%BB%E8%AF%91")
    elementInput = driver.find_element(By.ID, 'tta_input_ta')
    elementInput.send_keys('please tanslate it , GTP3')
    svg = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'tta_output_url')))
    time.sleep(2)
    ActionChains(driver).double_click(svg).pause(0.2).context_click(svg).perform()
    # print(elementOutput.text)
    time.sleep(20)
# bing()

def youdao():

    import undetected_chromedriver as uc
    driver = uc.Chrome(headless=True)
    driver.get("https://fanyi.youdao.com/index.html#")
    # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//img[@class="close"]'))).click()

    con = MySQLdb.connect("localhost", "root", "billions", "billion")
    cur = con.cursor()
    sql = "select ihtml from inews_autotimes limit 100"
    cur.execute(sql)
    fetchall = cur.fetchmany(100)

    for f in fetchall:
        elementInput = driver.find_element(By.ID, 'js_fanyi_input')
        i_ = str(f)
        pyperclip.copy(i_)
        elementInput.send_keys(Keys.CONTROL, 'v')
        time.sleep(3)
        # print(driver.page_source)
        result = Selector(text=driver.page_source).xpath("//p[@data-section]//text()").getall()
        print("".join(result))
        clickbutton =WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//a[@class="clearBtn icon_clear"]')))
        driver.execute_script("arguments[0].click();", clickbutton)
# youdao()
# # ok
def sogou():

    import undetected_chromedriver as uc
    driver = uc.Chrome()
    driver.get("https://fanyi.sogou.com/")
    con = MySQLdb.connect("localhost", "root", "billions", "billion")
    cur = con.cursor()
    sql = "select ihtml from inews_autotimes limit 100"
    cur.execute(sql)
    fetchall = cur.fetchmany(100)

    for f in fetchall:

        elementInput = driver.find_element(By.ID, 'trans-input')

        i_ = str(f)
        pyperclip.copy(i_)
        elementInput.send_keys(Keys.CONTROL, 'v')

        time.sleep(2)
        result = Selector(text=driver.page_source).xpath("//span[@class='trans-sentence']//text()").getall()
        # chains = ActionChains(driver)
        # chains.move_to_element(elementInput).double_click().click_and_hold().pause(5)
        # elementOutput = driver.find_element(By.XPATH, '//div[@class=output]')
        # chains.perform()
        print(i_)
        print("".join(result))
        WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH, '//span[@class="btn-clear"]'))).click()
        time.sleep(2)
# sogou()

def getHeaders():
    import undetected_chromedriver as uc
    driver = uc.Chrome()
    options = webdriver.ChromeOptions()
    # prefs = {"profile.managed_default_content_settings.images":2}
    # options.add_experimental_option("prefs",prefs)

    driver.get('https://bot.sannysoft.com/')  # my own test test site with max anti-bot protection
    time.sleep(100)

getHeaders()
#  OK
def googleFanyi():
    con = MySQLdb.connect("localhost", "root", "billions", "billion")
    cur = con.cursor()
    sql = "select ihtml from inews_autotimes limit 10"
    cur.execute(sql)

    options = webdriver.ChromeOptions()
    # prefs = {"profile.managed_default_content_settings.images":2}
    # options.add_experimental_option("prefs",prefs)
    options.add_argument("--enable-javascript")
    ua = UserAgent()
    options.add_argument('user-agent=' + ua.random)
    options.add_argument('javascript.enabled')
    # options.add_argument('--headless')
    # s = Service("F:\chromedriver.exe")
    driver = webdriver.Chrome( chrome_options=options)
    driver.get("https://www.google.com.hk/search?q=%E7%BF%BB%E8%AF%91")

    fetchall = cur.fetchmany(10000)
    time.sleep(10)
    WebDriverWait(driver, 5). \
        until(EC.visibility_of_element_located((By.XPATH, '//span[@title="对调源和目标语言"]'))) \
        .click()

    for i in fetchall:
        elementInput = driver.find_element(By.ID, 'tw-source-text-ta')

        print(str(i))
        i_ = str(i)[:380]
        pyperclip.copy(i_)
        elementInput.send_keys(Keys.CONTROL, 'v')
        delay = 1
        ranDelay = random.uniform(0.5 * delay, 1.5 * delay)
        time.sleep(ranDelay)

        elementOutput = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'tw-target-text')))
        delay = 2
        ranDelay = random.uniform(0.5 * delay, 1.5 * delay)
        time.sleep(ranDelay)
        print(elementOutput.text)

        WebDriverWait(driver, 5). \
            until(EC.visibility_of_element_located((By.XPATH, '//span[@title="清除原文文字"]'))) \
            .click()

def googleTranslate():
    options = webdriver.ChromeOptions()
    # prefs = {"profile.managed_default_content_settings.images":2}
    # options.add_experimental_option("prefs",prefs)
    options.add_argument("--enable-javascript")
    ua = UserAgent()
    options.add_argument('user-agent=' + ua.random)
    options.add_argument('javascript.enabled')
    # options.add_argument('--headless')
    # s = Service("F:\chromedriver.exe")
    driver = webdriver.Chrome(chrome_options=options)
    driver.get('https://translate.google.com/?hl=zh-CN')
    elementInput = WebDriverWait(driver, 5). \
        until(EC.visibility_of_element_located((By.XPATH, '//textarea[@class="er8xn"]')))
    elementInput.send_keys("please Translate it ,GPT3")
    driver.implicitly_wait(3)
    elementOutPut = WebDriverWait(driver, 5). \
        until(EC.visibility_of_element_located((By.XPATH, '//span[@class="ryNqvb"]')))
    print(elementOutPut.text)

    result = Selector(text=driver.page_source).xpath('//span[@class="ryNqvb"]//text()').getall()

    print(result)
# \div[contains(@class,'toggle')

    try:
        WebDriverWait(driver, 5). \
            until(EC.visibility_of_element_located((By.XPATH, '//button[contains(@class="VfPpkd-Bz112c-LgbsSe VfPpkd-Bz112c-LgbsSe-OWXEXe-e5LLRc-SxQuSe")]'))) \
            .click()
    except:
        driver.refresh()

    time.sleep(10)
# googleTranslate()



# urls ={1,3,2,4}
#
# with open('quotes-1.html', 'r',encoding='utf-8') as f:
#     html = f.read()
#     html=re.sub(r'原文链接','原地址',html)
#     html=re.sub(r'<p>.*?原文.*?</p>','',html)
#     print(html)
#
#     getall = Selector(text=group).xpath("//img/@src").getall()
#
#     for get in getall:
#         url = re.search(r'"(.*?)"', get)
#         print(url.group(1).rstrip('\\'))

#
# if os.path.getsize('urls.txt') > 0:
#     with open('urls.txt', 'rb') as f:
#         urls = pickle.load(f)



import undetected_chromedriver as uc
driver = uc.Chrome()
driver.get('https://www.odaily.news/post/5186831')  # my own test test site with max anti-bot protection
html = driver.page_source
html=re.sub(r'<p>.*?原文.*?</p>','',html)
html=re.sub(r'</h','/r/n/r/n/r/n/r/n</h',html)
html=re.sub(r'":"','',html)
res = re.search(r'content(.*?)",',html)


group = res.group(1)
if res and group:
    print(group)
    # result.extend(result1)
    # print(result)


