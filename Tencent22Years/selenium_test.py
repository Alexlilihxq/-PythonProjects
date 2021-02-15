from selenium import webdriver
import time
print('你好 {0} 自动化测试开始 {1} '.format('嘻嘻', '哈哈'))
driver = webdriver.Chrome(executable_path=r"C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe")
# driver = webdriver.Chrome()
driver.get('https://www.baidu.com')
driver.find_element_by_id('kw').send_keys('pig')
driver.find_element_by_id('su').click()
time.sleep(3)
driver.quit()