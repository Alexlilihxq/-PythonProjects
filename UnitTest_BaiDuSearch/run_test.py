import unittest
import yagmail
from HTMLTestRunner import HTMLTestRunner
import os
import time
from selenium import webdriver


# def send_mail_to_sweetie():
#     yag = yagmail.SMTP(user='newcode_hxq@163.com',
#                        password='LXLOBNPNTJMQFZZK',
#                        host='smtp.163.com')
#     subject = "来自帅气小哥的吃饭邀请"
#     content = "我的小宝贝，咱们去吃饭吧 ❤ 么么"
#     yag.send('huangrm98@163.com', subject, content)
#     print('Your Email has send out')


def send_mail(report):
    yag = yagmail.SMTP(user='newcode_hxq@163.com',
                       password='LXLOBNPNTJMQFZZK',
                       host='smtp.163.com')
    subject = "主题：自动化测试报告"
    content = "请查看附件"
    yag.send('1097170742@qq.com', subject, content, report)
    print('Your Email has send out')


if __name__ == '__main__':
    # send_mail_to_sweetie()
    # 定义测试用例的目录为当前目录下的test_case目录
    test_dir = './test_case'
    suit = unittest.defaultTestLoader.discover(test_dir, pattern='test*.py')

    # 获取当前时间
    now_time = time.strftime("%Y-%m-%d")

    # 测试报告保存地址及命名
    html_report_name = './test_report/'+'Result_' + now_time + '.html'

    # 生成 HTML 格式的测试报告
    fp = open(html_report_name, 'wb')
    runner = HTMLTestRunner(stream=fp, title='百度搜索测试报告', description='运行环境：Window 10 ， Chrome')
    runner.run(suit)
    fp.close()

    # 发送测试报告至邮箱
    send_mail(html_report_name)

    # 查看HTML测试报告
    path = os.path.abspath(html_report_name)
    driver = webdriver.Chrome()
    time.sleep(1)
    driver.get(path)
    time.sleep(10)
    driver.quit()
