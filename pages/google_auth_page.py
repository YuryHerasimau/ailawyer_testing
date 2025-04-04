from playwright.sync_api import Page, expect


class GoogleAuthPage:
    def __init__(self, page: Page):
        self.page = page
        self.email_field = page.get_by_role("textbox", name="Email or phone")
        self.password_field = page.get_by_role("textbox", name="Enter your password")
        self.next_button = page.get_by_role("button", name="Next")

    def enter_email(self, email: str):
        self.email_field.fill(email)
        self.next_button.click()

    def enter_password(self, password: str):
        self.password_field.fill(password)
        self.next_button.click()

    def wait_for_redirect(self, timeout=30000):
        try:
            with self.page.expect_event("close", timeout=timeout):
                pass
        except:
            self.page.wait_for_url("https://app.ailawyer.pro/chats/", timeout=timeout)