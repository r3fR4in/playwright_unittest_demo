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
        self.page = self.context.new_page()

    def tearDown(self):
        self.page.close()

    @classmethod
    def tearDownClass(cls):
        # self.page.close()
        cls.context.close()
        cls.browser.close()
        cls.playwright.stop()


