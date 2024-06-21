import base64

from playwright.sync_api import expect

from public import base_unit
import unittest
from config import setting
# from public.log import Log
from page.goto_page import GotoPage
from page.mobile_new_page import MobileNewPage


class MobileOrderTest(base_unit.BaseTest):
    """流動電話服務"""

    def test_01_mobile_new(self):
        """流動電話-新申請"""
        try:
            goto_page = GotoPage(self.page)
            goto_page.goto_mobile_new()
            mobile_new_page = MobileNewPage(self.page)
            mobile_new_page.set_customer_information('233333')
            mobile_new_page.select_service_number()
            mobile_new_page.select_product()
            mobile_new_page.set_sim_card()
            mobile_new_page.set_esim_email('test@test.com')
            mobile_new_page.set_remark('teleonetest')
            mobile_new_page.authorization('csr', 'a123456')
            order_number = mobile_new_page.get_order_number()
            mobile_new_page.submit_order()
            # 輪詢獲取訂單執行結果
            order_result = self.check_order_status(order_number)
            self.assertTrue(order_result)
        except Exception:
            # 失败或异常时截图，生成报告时会获取img变量生成html
            self.img = base64.b64encode(self.page.screenshot()).decode()
            self.fail()

    # def test_02_login(self):
    #     try:
    #         login_page = LoginPage(self.page)
    #         login_page.login(setting.USERNAME, '123')
    #         # self.assertIn('超级管理员', login_page.username_show.inner_text())
    #         expect(login_page.username_show).to_contain_text('超级管理员')
    #     except AssertionError:
    #         self.fail()
    #
    # def test_03_login(self):
    #     try:
    #         login_page = LoginPage(self.page)
    #         login_page.login(setting.USERNAME, setting.PASSWORD)
    #         # self.assertIn('test', login_page.username_show.inner_text())
    #         expect(login_page.username_show).to_contain_text('test')
    #     except AssertionError:
    #         self.fail()


if __name__ == '__main__':
    unittest.main()
