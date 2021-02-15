import time
import unittest
from selenium import webdriver
from unittest import TestCase
from selenium.webdriver.common.by import By
from Page.baidu_page import BaiduPage


class TestBaiDuSearch(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.driver = webdriver.Chrome()
        cls.base_url = 'https://baidu.com'

    @unittest.skip("直接跳过测试")
    def test_search_case1(self):
        print("unittest.skip()")

    @unittest.skipIf(True, "条件为真跳过测试")
    def test_search_case2(self):
        print("条件为真跳过测试")

    @unittest.skipUnless(False, "条件为真执行测试")
    def test_search_case3(self):
        print("条件为真执行测试")

    @unittest.expectedFailure
    def test_search_case4(self):
        print("不管结果，都标记为失败，但不会抛出异常")
        self.assertEqual(1, 1)

    def test_search_case5(self):
        search_key = 'selenium'
        page_baidu = BaiduPage(self.driver)
        page_baidu.get(self.base_url)
        page_baidu.search_input = search_key
        page_baidu.search_enter.click()
        time.sleep(3)
        self.assertEqual(search_key + '_百度搜索', self.driver.title)

    def test_search_case6(self):
        search_key = 'python'
        page_baidu = BaiduPage(self.driver)
        page_baidu.get(self.base_url)
        page_baidu.search_input = search_key
        page_baidu.search_enter.click()
        time.sleep(3)
        self.assertEqual(search_key + '_百度搜索', self.driver.title)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.driver.quit()


# class TestBaiDu