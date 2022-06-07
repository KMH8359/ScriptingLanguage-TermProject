import pyautogui
import requests
import csv

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
import re
from datetime import datetime
from tkinter import *
from datetime import datetime
import telegram

current_day = datetime.now().strftime('%Y-%m-%d')

start = "정왕역"
end = "사당역"
driver = webdriver.Chrome("./chromedriver")
driver.get('https://www.weather.go.kr/w/weather/forecast/short-term.do')

driver.implicitly_wait(10)
driver.find_element(By.XPATH, '//*[@id="index-local-search"]/div[1]/div/input').send_keys(start)
time.sleep(2)
driver.find_element(By.XPATH, '//*[@id="index-local-search"]/div[2]/ul/li[1]').click()
time.sleep(5)

soup = BeautifulSoup(driver.page_source, 'html.parser')
elms = soup.find(class_="slide")
for e in elms:
    print(e.get_text())

driver.find_element(By.XPATH, '//*[@id="index-local-search"]/div[1]/div/input').send_keys(end)
time.sleep(2)
driver.find_element(By.XPATH, '//*[@id="index-local-search"]/div[2]/ul/li[1]').click()
time.sleep(5)

soup = BeautifulSoup(driver.page_source, 'html.parser')
elms = soup.find(class_="slide")
for e in elms:
    print(e.get_text())









