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
from multiprocessing import Pool

routes = []
roads = []
token = '5421970300:AAGHJ8Yf0NmQ2CxH24DuKegDzvSk247JgWk'
sender_id = 5389446647


def select_pattern(event=None):
    pattern = ''
    for i in listbox.curselection():
        pattern = listbox.get(i)
        pattern = pattern.replace("번째 경로", "")
    path_text_box.delete("1.0", END)
    for text in roads[int(pattern) - 1]:
        path_text_box.insert(END, text)


def send():
    bot = telegram.Bot(token)
    pattern = ''
    try:
        for i in listbox.curselection():
            pattern = listbox.get(i)
            pattern = pattern.replace("번째 경로", "")
        text = roads[int(pattern) - 1]
        bot.sendMessage(chat_id=sender_id, text=text)
    except:
        pass


def search():

    roads.clear()
    path_text_box.delete("1.0", END)
    weather_text_box.delete("1.0", END)
    start_point = start_point_box.get("1.0", "end")
    destination_point = destination_point_box.get("1.0", "end")
    search_weather(start_point, destination_point)

    driver = webdriver.Chrome("./chromedriver")
    driver.get(full_url)
    driver.implicitly_wait(5)
    driver.find_element(By.XPATH, '//*[@id="directionStart0"]').send_keys(start_point)
    time.sleep(0.3)
    driver.find_element(By.XPATH, '//*[@id="directionStart0"]').send_keys(Keys.ENTER)
    time.sleep(0.3)
    driver.find_element(By.XPATH, '//*[@id="directionGoal1"]').send_keys(destination_point)
    time.sleep(0.3)
    driver.find_element(By.XPATH, '//*[@id="directionGoal1"]').send_keys(Keys.ENTER)
    time.sleep(0.3)
    driver.find_element(By.XPATH,
                        '//*[@id="container"]/shrinkable-layout/div/directions-layout/directions-result/div['
                        '1]/div/directions-search/div[2]/button[2]').click()
    time.sleep(1)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    elms = soup.find_all(class_='search_result transit ng-star-inserted')
    if elms is None:
        driver.quit()
        error_label.config(text="검색 실패")

    for e in elms:
        if e.get_text() != "":
            routes.append(e.get_text())

    listbox.delete(0, END)
    time.sleep(2)
    for i in range(len(elms) + 1):
        listbox.insert(END, f'{i + 1}번째 경로')

    current = datetime.now().strftime('%Y-%m-%d, %H:%M 기준')
    current_day = datetime.now().strftime('%Y-%m-%d')
    print(current_day)
    time_label.config(text=current)
    time.sleep(2)
    for i in range(len(elms) + 1):
        driver.find_element(By.XPATH,
                            f'//*[@id="container"]/shrinkable-layout/div/directions-layout/directions-result/div['
                            f'1]/directions-summary-list/directions-hover-scroll/div/ul/li[{i + 1}]/directions-summary-item'
                            f'-pubtransit/div[2]/div/button').click()

        time.sleep(3)
        raw = driver.page_source
        soup = BeautifulSoup(raw, 'html.parser')
        minute_elms = soup.find_all(class_='icon_transport_text')
        text_elms = soup.find_all(class_='path_name_text')

        text = ''
        text += '출발 시각: ' + soup.find(class_='departureTime').get_text() + '\n\n'
        for minute_elm, text_elm in zip(minute_elms, text_elms):
            text += text_elm.get_text() + ' ' + minute_elm.get_text() + '\n'
        text += '\n도착 시각: ' + soup.find(class_='arrivalTime').get_text()
        text = re.sub("이동수단", "도보", text)
        roads.append(text)

    driver.quit()


def search_weather(begin, end):
    driver = webdriver.Chrome("./chromedriver")
    driver.set_window_size(2000,2000)
    driver.get(weather_url)

    driver.implicitly_wait(10)

    driver.find_element(By.XPATH, '//*[@id="index-local-search"]/div[1]/div/input').send_keys(begin)
    time.sleep(2)
    driver.find_element(By.XPATH, '//*[@id="index-local-search"]/div[2]/ul/li[1]').click()
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    elms = soup.find(class_="slide")
    weather_text_box.insert(END, f'{begin} 날씨\n' + elms.get_text() + '\n\n')

    driver.find_element(By.XPATH, '//*[@id="index-local-search"]/div[1]/div/input').send_keys(end)
    time.sleep(2)
    driver.find_element(By.XPATH, '//*[@id="index-local-search"]/div[2]/ul/li[1]').click()
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    elms = soup.find(class_="slide")
    weather_text_box.insert(END, f'{end} 날씨\n' + elms.get_text() + '\n\n')


full_url = "https://map.naver.com/v5/directions/"
weather_url = "https://www.weather.go.kr/w/weather/forecast/short-term.do#"

window = Tk()

start_label = Label(window, text="출발지", width=10)
start_label.grid(column=0, row=0)

destination_label = Label(window, text="목적지", width=10)
destination_label.grid(column=2, row=0)

start_point_box = Text(window, width=20, height=3)
start_point_box.grid(column=0, row=1)
destination_point_box = Text(window, width=20, height=3)
destination_point_box.grid(column=2, row=1)

search_btn = Button(window, width=10, text="검색", command=search)
search_btn.grid(column=1, row=1)

send_btn = Button(window, width=10, height=2, text="텔레그램으로\n 보내기", command=send)
send_btn.grid(column=2, row=2)

listbox = Listbox(window, selectmode='single', width=20, height=20)
listbox.grid(column=1, row=2, columnspan=1)
listbox.bind('<<ListboxSelect>>', select_pattern)

path_text_box = Text(window, font='Aria')
path_text_box.grid(column=3, row=0, rowspan=3)

weather_text_box = Text(window, font='Aria')
weather_text_box.grid(column=4, row=0, rowspan=3)

current_time = datetime.now().strftime('%Y-%m-%d, %H:%M')
current_day = datetime.now().strftime('%Y-%m-%d')
time_label = Label(window, text=current_time, width=20)
time_label.grid(column=0, row=2)

error_label = Label(window, text=None, width=20)
error_label.grid(column=2, row=3)

window.mainloop()

print('start crawling : %s' % full_url)
