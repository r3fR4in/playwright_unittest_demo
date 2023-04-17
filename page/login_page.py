from page.base_page import Page


class LoginPage(Page):

    def __init__(self, page):
        super().__init__(page)
        self.username = self.page.get_by_placeholder('User Name')
        self.password = self.page.get_by_placeholder('Password')
        self.login_btn = self.page.locator('button:has-text("Login")')
        self.username_show = self.page.locator('xpath=//html/body/div[1]/header/div/div[2]/button[1]/span[2]/span')

    def login(self, username, password):
        self.goto()
        self.username.fill(username)
        self.password.fill(password)
        self.login_btn.click()
