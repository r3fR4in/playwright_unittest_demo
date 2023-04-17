from page.base_page import Page


class CarrierPage(Page):

    def __init__(self, page):
        super().__init__(page)
        self.search = self.page.get_by_title('Search')

    def click_search(self):
        self.search.click()
