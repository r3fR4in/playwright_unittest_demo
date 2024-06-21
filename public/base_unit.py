import time
from time import sleep
# from selenium import webdriver
import unittest, yaml
from config import setting
# from public.log import Log
from playwright.sync_api import sync_playwright
from page.login_page import LoginPage
import requests
import json
# requests移除告警
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# log = Log()


class BaseTest(unittest.TestCase):
    """
    自定义BaseTest类
    """

    # page = None
    # playwright = None
    # browser = None
    # context = None
    USERNAME = setting.USERNAME
    PASSWORD = setting.PASSWORD

    # @classmethod
    # def setUpClass(cls):
    #     cls.playwright = sync_playwright().start()
    #     cls.browser = cls.playwright.chromium.launch(
    #         args=['--start-maximized'],
    #         headless=False  # 无头浏览器
    #     )
    #     # self.browser = self.playwright.chromium.connect('http://localhost:9222')
    #     cls.context = cls.browser.new_context(
    #         ignore_https_errors=True,
    #         no_viewport=True
    #     )
    #     cls.page = cls.context.new_page()
    #     login_page = LoginPage(cls.page)
    #     login_page.login(setting.USERNAME, setting.PASSWORD)

    def setUp(self):
        # 当用例不通过需要截图时，报告截图方法在tearDown后执行，如果tearDown中关闭了页面将导致报错，所以把页面关闭放到setUp中判断
        # if self.context.pages:
        #     self.context.pages[0].close()
        # 当存在page时，刷新一下
        # if self.context.pages:
        #     self.page.reload()

        # playwright放在setupclass和teardownclass时无法使用多线程，应该同一变量被多个线程公用导致teardownclass时无法切换线程
        # 放到setup和teardown中牺牲单个suite的执行速度以换取多线程处理
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(
            args=['--start-maximized'],
            headless=False  # 无头浏览器
        )
        # self.browser = self.playwright.chromium.connect('http://localhost:9222')
        self.context = self.browser.new_context(
            ignore_https_errors=True,
            no_viewport=True
        )
        self.page = self.context.new_page()
        login_page = LoginPage(self.page)
        login_page.login(setting.USERNAME, setting.PASSWORD)

    def tearDown(self):
        self.page.close()
        self.context.close()
        self.browser.close()
        self.playwright.stop()

    # @classmethod
    # def tearDownClass(cls):
    #     cls.page.close()
    #     cls.context.close()
    #     cls.browser.close()
    #     cls.playwright.stop()

    """檢查訂單狀態"""
    def check_order_status(self, order_number):
        # 獲取當前登錄token
        session_storage = json.loads(self.page.evaluate("() => JSON.stringify(sessionStorage)"))
        token = session_storage['token']
        url = 'https://172.30.22.169/api/cso-server/queryOrdersNew'
        header = {
            "Content-Type": "application/json;charset=UTF-8",
            "Authorization": token
        }
        body = {
            "pageNum": 1,
            "pageSize": 10,
            "orderStatus": "-1,0,1,2,3,5,6,7,8,10",
            "serviceType": "",
            "serviceActions": "",
            "shopCodes": "",
            "orderNumber": order_number,
            "customerName": "",
            "serviceNumber": "",
            "lastHandlerName": "",
            "onlyShowMySuspendOrder": False,
            "isShowSuspendOrderToday": False,
            "accountNumber": "",
            "identityNumber": "",
            "contactTelephone": "",
            "onlyShowMyCompletedOrder": False,
            "isShowCompletedOrderToday": False,
            "fuzzySearchFlag": False,
            "finishedDateStart": "",
            "finishedDateEnd": ""
        }
        # 輪詢10分鐘調接口查詢訂單狀態，已完成返true，超過10分鐘沒有完成則false
        # 輪詢時間(秒)
        polling_duration = 10 * 60  # 10分鐘
        start_time = time.time()
        while True:
            current_time = time.time()
            elapsed_time = current_time - start_time
            if elapsed_time >= polling_duration:
                return False
            else:
                re = requests.request('get', url, headers=header, params=body, verify=False)
                result = re.json()
                if result['data']['list'][0]['orderStatus'] == 6:
                    return True
            sleep(15)

