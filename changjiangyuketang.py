import os
import re
import threading
import time
import tkinter
import tkinter.messagebox
from tkinter import ttk
from selenium.webdriver.chrome.options import Options
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By


# 线程函数，防止图形化界面卡死
def thread_it(func, *args):
    # 函数打包进线程
    t = threading.Thread(target=func, args=args)
    t.setDaemon(True)
    t.start()
    # t.join()


def openWeb():
    global wd
    # classtext = []
    if cmb.get() == '':
        print('empty')
    else:
        cmb.delete()
    wd = webdriver.Chrome()
    wd.get('https://changjiang.yuketang.cn/v2/web/index')
    wd.maximize_window()
    # 进入“我听的课”页面
    while 1:
        try:
            time.sleep(0.5)
            class_click = wd.find_element(By.XPATH, '//*[@id="tab-student"]')
            class_click.click()
            break
        except:
            continue
    time.sleep(1)
    i = 1
    # 记录所有课程
    while 1:
        try:
            classtext.append(wd.find_element(By.XPATH, class_start + f"{i}" + class_end).text)
            i += 1
        except:
            break
    # 设置下拉栏内容
    cmb['value'] = classtext


def openClass():
    global flag
    for text in classtext:
        if text == cmb.get():
            # 进入选定的课程主页
            while 1:
                try:
                    class_click = wd.find_element(By.XPATH,
                                                  class_start + str(classtext.index(cmb.get()) + 1) + class_end)
                    class_click.click()
                    break
                except:
                    continue
    while 1:
        try:
            # 两种模糊搜索方式 //<tag>[contains(text(),"xxx")]或者//<tag>[text()="xxx"]
            button = wd.find_element(By.XPATH, '//span[contains(text(),"展开")]')
            button.click()
            break
        except:
            continue
    time.sleep(0.5)
    ing = 0
    while 1:
        try:
            time.sleep(1)
            buttons = wd.find_elements(By.XPATH, '//span[text()="进行中"]')
            print('剩余进行中视频', len(buttons))
            buttons[ing].click()
            time.sleep(0.5)
            while 1:
                try:
                    detail = wd.find_element(By.XPATH, '//span[contains(text(),"详情")]')
                    detail.click()
                    time.sleep(8)
                    complete = wd.find_element(By.XPATH, '//li[contains(text(),"是否完成")]').text
                    print(complete)
                    icon = wd.find_element(By.XPATH,
                                           '//*[@id="app"]/div[2]/div/div[2]/div[2]/div/div/div[1]/button/i')
                    icon.click()
                    time.sleep(10)
                    if complete == "是否完成：已完成":
                        print("completed")
                        break
                except:
                    ing += 1
                    break
            wd.back()
            wd.back()
            time.sleep(1)
            class_click = wd.find_element(By.XPATH, class_start + str(classtext.index(cmb.get()) + 1) + class_end)
            class_click.click()
            time.sleep(1)
            button = wd.find_element(By.XPATH, '//span[contains(text(),"展开")]')
            button.click()
            continue
        except:
            print('进行中视频已看完')
            break
    time.sleep(0.5)
    i = 0
    while 1:
        try:
            time.sleep(1)
            buttons = wd.find_elements(By.XPATH, '//span[text()="未开始"]')
            print(len(buttons))
            # for i in range(0, len(buttons) + 1):
            print('剩余视频数量:', len(buttons))
            buttons[i].click()
            time.sleep(0.5)
            flag = False
            while 1:
                try:
                    detail = wd.find_element(By.XPATH, '//span[contains(text(),"详情")]')
                    detail.click()
                    time.sleep(8)
                    complete = wd.find_element(By.XPATH, '//li[contains(text(),"是否完成")]').text
                    print(complete)
                    icon = wd.find_element(By.XPATH,
                                           '//*[@id="app"]/div[2]/div/div[2]/div[2]/div/div/div[1]/button/i')
                    icon.click()
                    time.sleep(10)
                    if complete == "是否完成：已完成":
                        print("completed")
                        break
                except:
                    # 这边抛出异常的情况是进入期末考试,或者进入作业页面
                    i += 1
                    flag = True
                    break
            if flag:
                wd.back()
                wd.back()
                class_click1 = wd.find_element(By.XPATH,
                                               class_start + str(classtext.index(cmb.get()) + 1) + class_end)
                class_click1.click()
                time.sleep(1)
                while 1:
                    try:
                        button = wd.find_element(By.XPATH, '//span[contains(text(),"展开")]')
                        button.click()
                        break
                    except:
                        continue
                continue
            wd.back()
            wd.back()
            time.sleep(0.5)
            try:
                wd.find_element(By.XPATH, class_start + str(classtext.index(cmb.get()) + 1) + class_end)
            except:
                wd.back()
            class_click = wd.find_element(By.XPATH, class_start + str(classtext.index(cmb.get()) + 1) + class_end)
            class_click.click()
            time.sleep(1)
            button = wd.find_element(By.XPATH, '//span[contains(text(),"展开")]')
            button.click()
            continue
        except:
            wd.quit()
            print("出错了")
            break


classtext = []
class_start = '//*[@id="pane-student"]/div[2]/div/div['
class_end = ']/div/div[1]/div/div[1]/div[1]/h1'
top = tkinter.Tk()
top.minsize(580, 400)
tkinter.Label(top, text='选择课程').grid(row=0, column=1, sticky='w')
cmb = ttk.Combobox(top)
cmb.grid(row=0, column=2, columnspan=2, sticky='w')
cmb.configure(state="readonly")
tkinter.Button(top, text='手动打开网页', command=lambda: thread_it(openWeb)).grid(row=0, column=5, sticky='w')
thread_it(openWeb)
tkinter.Button(top, text='选择该课程', command=lambda: thread_it(openClass)).grid(row=0, column=4, sticky='w')
top.mainloop()
