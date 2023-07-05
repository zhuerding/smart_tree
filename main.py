# selenium 版本基于4.10.0，python版本基于3.9
# pip install selenium
from selenium.webdriver.common.by import By
from selenium import webdriver

print("欢迎使用Auto Smart tree，")
# 加载浏览器驱动，chromedriver的版本一定要与Chrome浏览器一致
path = 'chromedriver.exe'  # chromedriver需位于根目录下
driver = webdriver.Chrome()

# 访问智慧树官网
url = 'https://www.zhihuishu.com/'
driver.get(url)
button = driver.find_element(By.XPATH, '//li[@id="notLogin"]/a[@target="_self"]')
button.click()

input()