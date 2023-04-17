from config import setting
from public.log import Log

# 读取配置文件的URL
login_url = setting.URL
log = Log()


class Page(object):
    """
    基础类，用于页面对象类的继承
    """
    def __init__(self, page, base_url=login_url):
        self.base_url = base_url
        self.page = page

    def goto(self):
        url = self.base_url
        self.page.goto(url)

    # def get_by_placeholder(self, text):
    #     try:
    #         return self.page.get_by_placeholder(text)
    #     except Exception:
    #         log.error("{0}页面中未能找到placeholder为{1}的元素".format(self, text))
    #
    # def locator(self, text):
    #     try:
    #         return self.page.locator(text)
    #     except Exception:
    #         log.error("{0}页面中未能找到{1}的元素".format(self, text))
