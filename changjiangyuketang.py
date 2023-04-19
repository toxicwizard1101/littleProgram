import os
import re
import threading
import time
import tkinter
import tkinter.messagebox
from tkinter import ttk

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
    # print(e1.get())
    # class_start = '//*[@id="pane-student"]/div[2]/div/div['
    # class_end = ']/div/div[1]/div/div[1]/div[1]/h1'
    # 打开浏览器
    global wd
    wd = webdriver.Chrome()
    wd.get('https://changjiang.yuketang.cn/v2/web/index')
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
            # print(classtext)
            i += 1
        except:
            break
    # print(classtext)
    # 设置下拉栏内容
    cmb['value'] = classtext


def openClass():
    # print(cmb.get())
    global flag
    for text in classtext:
        if text == cmb.get():
            # print(classtext.index(cmb.get()))
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
    print(111)
    time.sleep(0.5)
    while 1:
        try:
            buttons = wd.find_elements(By.XPATH, '//span[text()="未开始"]')
            # print(buttons)
            # buttons[1].click()
            # for i in range(1, len(buttons)+1):
            # print(len(buttons))
            buttons[0].click()
            # time.sleep(2)
            # try:
            #     test = wd.find_element(By.XPATH, '//*[@id="app"]/div[2]/div/div[2]/div[1]/div/p').text
            #     if test == "期末考试":
            #         flag = False
            #         break
            #     break
            # except:
            #     print("error")
            # if not flag:
            #     flag = True
            #     wd.back()
            #     continue
            time.sleep(0.5)
            while 1:
                try:
                    time.sleep(5)
                    detail = wd.find_element(By.XPATH, '//span[contains(text(),"详情")]')
                    detail.click()
                    time.sleep(8)
                    complete = wd.find_element(By.XPATH, '//li[contains(text(),"是否完成")]').text
                    print(complete)
                    icon = wd.find_element(By.XPATH,
                                           '//*[@id="app"]/div[2]/div/div[2]/div[2]/div/div/div[1]/button/i')
                    icon.click()
                    if complete == "是否完成：已完成":
                        print("completed")
                        break
                except:
                    continue
            wd.back()
            wd.back()
            time.sleep(0.5)
            class_click = wd.find_element(By.XPATH, class_start + str(classtext.index(cmb.get()) + 1) + class_end)
            class_click.click()
            time.sleep(1)
            while 1:
                try:
                    # 两种模糊搜索方式 //<tag>[contains(text(),"xxx")]或者//<tag>[text()="xxx"]
                    button = wd.find_element(By.XPATH, '//span[contains(text(),"展开")]')
                    button.click()
                    break
                except:
                    continue
            continue
        except:
            continue


classtext = []
class_start = '//*[@id="pane-student"]/div[2]/div/div['
class_end = ']/div/div[1]/div/div[1]/div[1]/h1'
top = tkinter.Tk()
top.minsize(580, 400)
tkinter.Label(top, text='选择课程').grid(row=0, column=1, sticky='w')
cmb = ttk.Combobox(top)
cmb.grid(row=0, column=2, columnspan=2, sticky='w')
cmb.configure(state="readonly")
# cmb.current(0)
# e1 = tkinter.Entry(top)
# e1.grid(row=0, column=1, sticky='w')
tkinter.Button(top, text='手动打开网页', command=lambda: thread_it(openWeb)).grid(row=0, column=5, sticky='w')
thread_it(openWeb)
tkinter.Button(top, text='选择该课程', command=lambda: thread_it(openClass)).grid(row=0, column=4, sticky='w')
top.mainloop()
