from time import sleep
# from selenium import webdriver
import unittest, yaml
from config import setting
from public.log import Log
from playwright.sync_api import sync_playwright

log = Log()


class BaseTest(unittest.TestCase):
    """
    自定义BaseTest类
    """

    playwright = None
    browser = None
    context = None
    USERNAME = setting.USERNAME
    PASSWORD = setting.PASSWORD

    @classmethod
    def setUpClass(cls):
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch(
            headless=False,
            args=['--start-maximized']
        )
        # self.browser = self.playwright.chromium.connect('http://localhost:9222')
        cls.context = cls.browser.new_context(
            ignore_https_errors=True,
            no_viewport=True
        )

    def setUp(self):
        # 当用例不通过需要截图时，报告截图方法在tearDown后执行，如果tearDown中关闭了页面将导致报错，所以把页面关闭放到setUp中判断
        if self.context.pages:
            self.context.pages[0].close()
        self.page = self.context.new_page()

    # def tearDown(self):
    #     self.page.close()

    @classmethod
    def tearDownClass(cls):
        # self.page.close()
        cls.context.close()
        cls.browser.close()
        cls.playwright.stop()


