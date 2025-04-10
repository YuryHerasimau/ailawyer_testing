import pytest
from playwright.sync_api import Page, expect
from config import Config


class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.other_radio = page.get_by_role("radio", name="Other", exact=True)
        self.role_field = page.get_by_placeholder("Type your role here")
        self.login_button = page.get_by_text("Log in", exact=True)
        self.google_button = page.get_by_role("button").first

    def navigate(self):
        self.page.goto(Config.LOGIN_URL)
        expect(self.page).to_have_url(Config.LOGIN_URL)

    def login(self, role: str, email: str, password: str):
        self.other_radio.click()
        self.role_field.fill(role)
        self.login_button.click()
        
        self.google_button.wait_for(state="visible")
        
        with self.page.expect_popup() as popup_info:
            self.google_button.click()
        
        from pages.google_auth_page import GoogleAuthPage
        google_page = GoogleAuthPage(popup_info.value)
        
        google_page.enter_email(email)
        google_page.enter_password(password)

        # Обрабатываем возможную верификацию
        # Возвращаем статус верификации вместо прямого вызова skip
        if hasattr(google_page, 'verification_required') and google_page.verification_required:
            return False

        google_page.wait_for_redirect()
        
        return self.page