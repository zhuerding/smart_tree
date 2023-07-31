import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By

path = 'chromedriver.exe'

url = 'https://dun.163.com/trial/space-inference'
browser = webdriver.Chrome()
browser.get(url)
i = 0
while i <= 20:
    button = browser.find_element(By.XPATH, '//div[@class="yidun_tips"]')
    button.click()
    time.sleep(2)
    refresh = browser.find_element(By.XPATH, '//button[@class="yidun_refresh"]')
    refresh.click()

    button = browser.find_element(By.XPATH, '//div[@class="yidun_tips"]')
    button.click()
    time.sleep(2)
    image = browser.find_element(By.XPATH, '//div[@class="yidun_bgimg"]/img[@class="yidun_bg-img"]')
    urls = image.get_attribute("src")
    words = browser.find_element(By.XPATH, '//div[@class="yidun_tips__content"]/span[@class="yidun_tips__text '
                                           'yidun-fallback__tip"]')
    content = words.text
    print(urls, content)

    r = requests.get(urls)
    img = r.content
    # 写入图片
    with open(f"./output/{i}.jpg", "wb") as f:
        f.write(img)
    content = content + str('\n') + '  ' + f"{i}.jpg"
    with open(f"./output/content.txt", "a") as f:
        f.write(content)
    i = i + 1
# button = browser.find_element(By.XPATH, '//li[@id="notLogin"]/a[@target="_self"]')

# 发送请求并获取响应内容
# r = requests.get(urls)
# content = r.content
# # 写入图片
# with open("NASA.jpg", "wb") as f:
#     f.write(content)
