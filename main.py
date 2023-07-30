# selenium 版本基于4.10.0，python版本基于3.9
# pip install selenium
import time

from selenium.webdriver.common.by import By
from selenium import webdriver
import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import utils.segmentation_jieba
import utils.detect
import utils.det_main
import utils.classify_color
#
# # Clear函数，用于清理内存
# def clear():
#     try:
#         os.system('taskkill /im chromedriver.exe /F')
#         os.system('taskkill /im chrome.exe /F')
#     except:
#         pass
#     else:
#         print('已清理进程')
#
#
# # Driver函数，用于加载chromedriver驱动
# def driver(path1):
#     # 加载浏览器驱动，chromedriver的版本一定要与Chrome浏览器一致
#     browser1 = webdriver.Chrome()
#     browser1.get(str(path1))
#     return browser1
#
#
# # 自检函数
# def check(user):
#     if user == 1:
#         # 检测user_list.xlsx是否存在
#         if os.path.exists("user_list.xlsx"):
#             pass
#         else:
#             df = pd.DataFrame({"user_name": [], "password":[]})
#             # 使用to_excel()方法将DataFrame保存为example.xlsx文件，index=False表示不需要将DataFrame的索引列保存到文件中
#             df.to_excel("user_list.xlsx", index=False)
#         # 检测user文件夹是否存在
#         if os.path.exists("./user"):
#             pass
#         else:
#             os.mkdir("./user")
#         print("文件自检完成")
#     else:
#         if os.path.exists(f"./user/{user['username']}"):
#             if os.path.exists(f"./user/{user['username']}/{user['username']}.txt"):
#                 pass
#             else:
#                 with open(f"./user/{user['username']}/{user['username']}.txt", "w") as file:
#                     # 向文件中写入一行字符串
#                     file.write(f"user_name:{user['username']}\n================================================")
#                     file.close()
#         else:
#             os.mkdir(f"./user/{user['username']}/")
#             # 使用with语句打开或创建一个名为test.txt的文件，使用"w"模式，表示写入模式
#             with open(f"./user/{user['username']}/{user['username']}.txt", "w") as file:
#                 # 向文件中写入一行字符串
#                 file.write(f"user_name:{user['username']}\n================================================")
#                 file.close()
#
#
# # Data函数，用于加载用户信息
# def data():
#     df = pd.read_excel("user_list.xlsx")
#     # 读取"user_name"列
#     user_lst = df["user_name"]
#     # 读取"password"列
#     psws = df["password"]
#     # 封装用户信息
#     user_data = (user_lst, psws)
#     return user_data
#
#
# # browser_login函数，用于网页登录
# def login(browser_login, user_data):
#     # 进入登录界面
#     button = browser_login.find_element(By.XPATH, '//li[@id="notLogin"]/a[@target="_self"]')
#     button.click()
#     # 获取用户名与密码输入框
#     user_name = browser_login.find_element(By.ID, 'lUsername')
#     psw = browser_login.find_element(By.ID, 'lPassword')
#     log_in = browser_login.find_element(By.XPATH, '//span[@class="wall-sub-btn"]')
#     # 输入用户信息
#     user_name.send_keys(int(user_data['username']))
#     psw.send_keys(user_data['password'])
#     # 登录
#     log_in.click()
#     time.sleep(10)
#     return browser_login
#
#
# # 滑块验证码破解
# class CrackSlider():
#     def __init__(self):
#         pass
#
#
# if __name__ == '__main__':
#     print("欢迎使用Auto Smart tree，作者：zhuerding")
#     print('清理进程')
#     clear()
#     print("相关文件自检中")
#     a = 1
#     check(a)
#     # 加载驱动地址
#     path = 'chromedriver.exe'  # chromedriver需位于根目录下
#     # 加载智慧树官网
#     url = 'https://www.zhihuishu.com/'
#     browser = driver(url)
#     # 加载用户表
#     data_lst = data()
#     i = 0
#     while i < len(data_lst[0]):
#         # 获取单个用户信息
#         print("\n")
#         print(f"现在开始{data_lst[0][i]}用户的登录")
#         user = {'username': data_lst[0][i], 'password': data_lst[1][i]}
#         check(user)
#         print(user)
#         # 访问登录界面
#         browser = login(browser, user)
#         print(6)
#         time.sleep(5)
#         i = i + 1
#     #
#     input()
# 测试
content = '请点击小写n朝向一样的大写K'
print("收到数据，识别开始")
image_path = r'./img/20.jpg'
# 对文本进行分词
noun = utils.segmentation_jieba.segmentation(content[3:])
# 获取页面中内容
data = utils.detect.detect(image_path)
# 获取元件颜色
color = utils.classify_color.detect(image_path)
# 对其进行二次iou去重
dat = utils.det_main.de_weight(data)
col = utils.det_main.de_weight(color)
# 将朝向和颜色标签汇总
all_data = utils.det_main.select(dat, col)
for i in all_data:
    if i["color"] == 'color':
        print("\033[31m" + "部分颜色识别失败，可能影响识别效果" + '\033[0;0m')
        break
answer = utils.det_main.information(all_data, noun)
if type(answer) == type("a"):
    print(answer)
else:
    print(len(dat))
    lst = answer["crop"].tolist()
    crop = ((lst[2] - lst[0])/2, (lst[3] - lst[1])/2)
    print('输入的问题是:', "\033[34m" + content + '\033[0;0m')
    print("您需要的答案中心坐标为", "\033[32m" + "x:%f, y:%f" % tuple(crop) + '\033[0;0m')