from playwright.sync_api import Page, expect


class GoogleAuthPage:
    def __init__(self, page: Page):
        self.page = page
        self.email_field = page.get_by_role("textbox", name="Email or phone")
        self.password_field = page.get_by_role("textbox", name="Enter your password")
        self.next_button = page.get_by_role("button", name="Next")

    def enter_credentials(self, email: str, password: str):
        self.email_field.fill(email)
        self.next_button.click()
        self.password_field.fill(password)
        self.next_button.click()
        
    def enter_email(self, email: str):
        self.email_field.fill(email)
        self.next_button.click()
        return self

    def enter_password(self, password: str):
        self.password_field.fill(password)
        self.next_button.click()
        return self

    def wait_for_redirect(self, timeout=30000):
        """Ждет пока popup закроется (авторизация успешна)"""
        # self.page.wait_for_event("close")
        
        """Ожидает завершения авторизации"""
        try:
            # Ждем либо закрытия popup, либо появления главной страницы
            with self.page.expect_event("close", timeout=timeout):
                pass
        except:
            # Если popup не закрылся, проверяем URL основной страницы
            self.page.wait_for_url("https://app.ailawyer.pro/chats/", timeout=timeout)