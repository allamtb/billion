import random
import time

import MySQLdb
import pyperclip
from selenium import webdriver
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent





def baidufanyi():
   options = webdriver.ChromeOptions()
   # prefs = {"profile.managed_default_content_settings.images":2}
   # options.add_experimental_option("prefs",prefs)
   options.add_argument("--enable-javascript")
   # options.add_argument('user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"')
   options.add_argument('javascript.enabled')
   # options.add_argument('--headless')
   s = Service("F:\chromedriver.exe")
   driver = webdriver.Chrome(service=s, chrome_options=options)
   driver.get("https://fanyi.baidu.com/?aldtype=16047#zh/en/")
   # element = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID, 'baidu_translate_input'))
   #                                          )
   # # element.send_keys("English is good place")
   #
   con = MySQLdb.connect("localhost", "root", "billions", "billion")
   cur = con.cursor()
   element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'app-guide-close')))
   element.click()
   elementInput = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'baidu_translate_input')))
   sql = "select ihtml from inews_autotimes"
   cur.execute(sql)
   fetchall = cur.fetchmany(1000)
   for i in fetchall:
      print(str(i))
      pyperclip.copy(str(i))
      elementInput.send_keys(Keys.CONTROL, 'v')
      delay = 1
      ranDelay = random.uniform(0.5 * delay, 1.5 * delay)
      time.sleep(ranDelay)

      out = driver.find_element(By.XPATH, '//div[@class="trans-right"]')
      # outElement = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CLASS_NAME, 'ordinary-output source-output')))
      x = out.text.replace("\n笔记\n双语对照", "")
      ranDelay = random.uniform(0.5 * delay, 1.5 * delay)
      time.sleep(ranDelay)
      print(x)
      driver.find_element(By.CLASS_NAME, 'textarea-clear-btn').click()


def bing():
   options = webdriver.ChromeOptions()
   # prefs = {"profile.managed_default_content_settings.images":2}
   # options.add_experimental_option("prefs",prefs)
   options.add_argument("--enable-javascript")
   # options.add_argument('user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"')
   options.add_argument('javascript.enabled')
   # options.add_argument('--headless')
   s = Service("F:\chromedriver.exe")
   driver = webdriver.Chrome(service=s, chrome_options=options)
   driver.get("https://cn.bing.com/search?q=%E7%BF%BB%E8%AF%91")
   elementInput = driver.find_element(By.ID, 'tta_input_ta')
   elementInput.send_keys('please tanslate it , GTP3')
   elementOutput = driver.find_element(By.ID, 'tta_output_ta')
   svg = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'tta_output_url')))
   time.sleep(2)
   ActionChains(driver).double_click(svg).pause(0.2).context_click(svg).perform()
   print(elementOutput.text)
   time.sleep(20)


def googleFanyi():
   con = MySQLdb.connect("localhost", "root", "billions", "billion")
   cur = con.cursor()
   sql = "select ihtml from inews_autotimes"
   cur.execute(sql)

   options = webdriver.ChromeOptions()
   # prefs = {"profile.managed_default_content_settings.images":2}
   # options.add_experimental_option("prefs",prefs)
   options.add_argument("--enable-javascript")
   ua = UserAgent()
   options.add_argument('user-agent='+ua.random)
   options.add_argument('javascript.enabled')
   # options.add_argument('--headless')
   s = Service("F:\chromedriver.exe")
   driver = webdriver.Chrome(service=s, chrome_options=options)
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

      WebDriverWait(driver,5).\
         until(EC.visibility_of_element_located((By.XPATH, '//span[@title="清除原文文字"]')))\
         .click()




googleFanyi()




