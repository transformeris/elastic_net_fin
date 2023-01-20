from selenium import webdriver
import datetime
import win32com.client
speaker=win32com.client.Dispatch('SAPI.SpVoice')
now_time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')

rush_time='2023-01-08 11:13:00.00000000'
driver = webdriver.Edge()
driver.get("https://www.taobao.com")
driver.find_element("link text",'亲，请登录').click()
driver.get('https://cart.taobao.com/cart.htm')