import time
from tkinter import *
from tkinter import font
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


driver = webdriver.Chrome()

# 사이트 접속
driver.get('https://www.cgv.co.kr/')
driver.implicitly_wait(20)

# 검색
driver.find_element(By.XPATH, '//*[@id="header_keyword"]').send_keys("범죄도시2")
driver.find_element(By.XPATH, '//*[@id="header_keyword"]').send_keys(Keys.ENTER)
driver.find_element(By.XPATH, '//*[@id="preOrderMovie_list"]/li/div/div[3]/a[2]').click()

time.sleep(2)
soup = BeautifulSoup(driver.page_source, 'html.parser')
elms = soup.find(class_="content scroll-y")

print(elms.get_text())


# window = Tk()
# window.geometry("600x400")
#
#
# def readText():
#     str = inputbox.get("1.0", "end")
#     print(str)
#
#
# textlabel = Label(window, text="현재 위치하신 곳과 행선지를 입력해주세요")
# textlabel.pack()
# inputbox = Text(window, height=1)
# inputbox.pack()
#
# btn_meat = Radiobutton(window, width=10, height=1, text="육식")
# btn_meat.pack()
# search_btn = Button(window, width=10, height=1, text="검색")
# search_btn.pack()
#
# window.mainloop()
