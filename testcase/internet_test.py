import base64

from public import base_unit
import unittest
from config import setting
# from public.log import Log
from page.goto_page import GotoPage
from page.mobile_new_page import MobileNewPage


class InternetOrderTest(base_unit.BaseTest):
    """互聯網服務"""

    def test_01_Internet_new(self):
        """互聯網-新申請"""
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

    def test_02_Internet_new(self):
        """互聯網-測試測試"""
        try:
            goto_page = GotoPage(self.page)
            goto_page.goto_mobile_new()
            mobile_new_page = MobileNewPage(self.page)
            mobile_new_page.set_customer_information('233333')
            mobile_new_page.select_service_number()
            # mobile_new_page.set_customer_information('233333')
        except Exception:
            # 失败或异常时截图，生成报告时会获取img变量生成html
            self.img = base64.b64encode(self.page.screenshot()).decode()
            self.fail()


if __name__ == '__main__':
    unittest.main()
