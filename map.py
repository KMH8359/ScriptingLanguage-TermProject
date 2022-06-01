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

routes = []
roads = []
token = '5421970300:AAGHJ8Yf0NmQ2CxH24DuKegDzvSk247JgWk'
sender_id = 5389446647


def select_pattern(event=None):
    pattern = ''
    for i in listbox.curselection():
        pattern = listbox.get(i)
        pattern = pattern.replace("번째 경로", "")
    textbox.delete("1.0", END)
    for text in roads[int(pattern) - 1]:
        textbox.insert(END, text)


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
    start_point = start_point_box.get("1.0", "end")
    destination_point = destination_point_box.get("1.0", "end")

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
    for e in elms:
        if e.get_text() != "":
            routes.append(e.get_text())

    listbox.delete(0, END)
    time.sleep(2)
    for i in range(len(elms) + 1):
        # try:
        #     optimal = driver.find_element(By.XPATH,
        #                                   f'//*[@id="container"]/shrinkable-layout/div/directions-layout/directions'
        #                                   f'-result/div[1]/directions-summary-list/directions-hover-scroll/div/ul/li['
        #                                   f'{i + 1}]/directions-summary-item-pubtransit/div[1]/em')
        #     listbox.insert(END, f'{i + 1}번째 경로 -- {optimal.text}')
        # except:
        listbox.insert(END, f'{i + 1}번째 경로')

    current = datetime.now().strftime('%Y-%m-%d, %H:%M 기준')
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

        # elms = soup.find(class_='list_path')
        # text = elms.get_text()
        # text = re.sub("파노라마 보기", "\n", text)
        # text = re.sub("상세정보 거리뷰", "", text)
        # text = re.sub("시간표", "", text)
        # text = re.sub("빠른환승 *\d-*\d", "", text)
        # text = re.sub("빠른하차 *\d-*\d", "", text)
        # text = re.sub("\d\d\d\d\d", "", text)
        # text = re.sub("이동수단", "", text)
        text = ''
        text += '출발 시각: ' + soup.find(class_='departureTime').get_text() + '\n\n'
        for minute_elm, text_elm in zip(minute_elms, text_elms):
            text += text_elm.get_text() + ' ' + minute_elm.get_text() + '\n'
        text += '\n도착 시각: ' + soup.find(class_='arrivalTime').get_text()
        text = re.sub("이동수단", "도보", text)
        roads.append(text)
        # elms = soup.find_all(class_='path_name')
        # for e in elms:
        #     roads.append(e.get_text())

    # bt = driver.find_element(By.XPATH,
    #                          '//*[@id="container"]/shrinkable-layout/div/directions-layout/directions-result/div['
    #                          '2]/directions-details-result/directions-details-summary-pubtransit/div/em')
    # textbox.insert(END, f"{bt.text} 경로 " + "\n")
    # # 걸리는 시간 출력
    # bt = driver.find_element(By.CLASS_NAME, 'summary_duration')
    # textbox.insert(END, f"걸리는 시간:{bt.text}\n")
    # textbox.insert(END,
    #                driver.find_element(By.CLASS_NAME, 'summary_time').text + '\n' + driver.find_element(By.CLASS_NAME,
    #                                                                                                     'summary_info_detail').text + '\n')
    # names = driver.find_elements(By.CLASS_NAME, "path_name_text")
    # elms = driver.find_elements(By.CLASS_NAME, "list_path")

    # print(len(driver.find_element(By.CLASS_NAME, "list_path")))

    # for i in range(1, 50):
    #     name = driver.find_elements(By.XPATH,
    #                                 f'//*[@id="container"]/shrinkable-layout/div/directions-layout/directions-result/div[2]/directions-details-result/directions-hover-scroll/div/div[1]/div/div/ul/li[{i}]')
    #     if name:
    #         for txt in name:
    #             textbox.insert(END, txt.text)
    #     else:
    #         break


full_url = "https://map.naver.com/v5/directions/"

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

textbox = Text(window, font='Aria')
textbox.grid(column=3, row=0, rowspan=3)

current_time = datetime.now().strftime('%Y-%m-%d, %H:%M')
time_label = Label(window, text=current_time, width=20)
time_label.grid(column=0, row=2)

window.mainloop()

# start_place = input("출발지를 입력하시오: ")
# destination = input("목적지를 입력하시오: ")
# print("출발지: %s" % start_place)
# print("목적지: %s" % destination)
# full_url = "https://m.map.naver.com/search2/search.naver?query=%s" % search_key
# full_url = f"http://map.naver.com/index.nhn?slng=127&slat=37.5&stext={start_place}&elng=127.5&elat=37.4&pathType=0&showMap=true&etext={destination}&menu=route"


print('start crawling : %s' % full_url)
'''
response = requests.get(full_url)
#print(response.text)
bs = BeautifulSoup(response.text, 'html.parser')
f = open('result.txt','w')
f.write(response.text)
f.close()
'''

# for name in names:
#   print(name.text)

# print(driver.find_element(By.CLASS_NAME, 'summary_time').text)

# times, length = score_result.split("추천", 1)
#
# times = times.split(">", 2)
# times = times[2]
# times = times.split("<", 1)
# times = times[0]
#
# length = length.split(">", 4)
# length = length[4]
# length = length.split("<", 1)
# length = length[0]
# # print("거리 : " + length + "   /   소요예상시간 : " + times)
# times_ff = times
# driver.close()
#
# now_hour = datetime.today().strftime("%H")
# now_min = datetime.today().strftime("%M")
#
# now_time = int(now_hour) * 60 + int(now_min)
# if '시간' in times:
#     times = times.split("시간", 1)
#     times_hour = times[0]
#     times_hour = times_hour.replace("시간", "")
#     times_min = times[1]
#     times_min = times_min.replace(" ", "")
#     times_min = times_min.replace("분", "")
# else:
#     times = times.replace(" ", "")
#     times_min = times.replace("분", "")
#     times_hour = '0'
#
# times_hour = str(times_hour)
# times_min = str(times_min)
#
# times_f = int(times_hour) * 60 + int(times_min)
#
# time_sum = times_f + now_time
# d
# time_f_hour = int(time_sum / 60)
# time_f_min = time_sum % 60
#
# if time_f_hour >= 24:
#     time_f_hour = time_f_hour - 24
#
# print("거리 : " + length + "   /   예상소요시간 : " + times_ff + "   /   현재출발시 예상도착시간 : " + str(time_f_hour) + "시 " + str(
#     time_f_min) + "분")

# 크롭 웹페이지를 닫음
