from playwright.sync_api import expect

from public import base_unit
import unittest
from config import setting
from public.log import Log
from page.login_page import LoginPage
from page.carrier_page import CarrierPage


class LoginTest(base_unit.BaseTest):

    def test_01_login(self):
        try:
            login_page = LoginPage(self.page)
            login_page.login(setting.USERNAME, setting.PASSWORD)
            # self.assertIn('超级管理员', login_page.username_show.inner_text())
            expect(login_page.username_show).to_contain_text('超级管理员')
            carrier_page = CarrierPage(self.page)
            carrier_page.click_search()
        except AssertionError:
            self.fail()

    def test_02_login(self):
        try:
            login_page = LoginPage(self.page)
            login_page.login(setting.USERNAME, '123')
            # self.assertIn('超级管理员', login_page.username_show.inner_text())
            expect(login_page.username_show).to_contain_text('超级管理员')
        except AssertionError:
            self.fail()

    def test_03_login(self):
        try:
            login_page = LoginPage(self.page)
            login_page.login(setting.USERNAME, setting.PASSWORD)
            # self.assertIn('test', login_page.username_show.inner_text())
            expect(login_page.username_show).to_contain_text('test')
        except AssertionError:
            self.fail()


if __name__ == '__main__':
    unittest.main()
