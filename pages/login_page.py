from pages.base_page import BasePage
from playwright.sync_api import Page
from pages.google_auth_page import GoogleAuthPage
from config import Config


class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self._init_locators()

    def _init_locators(self):
        # выбор роли
        self.legal_consumer_radio = self.page.get_by_role("radio", name="I'm a legal consumer", exact=True)
        self.lawyer_radio = self.page.get_by_role("radio", name="I'm a lawyer", exact=True)
        self.law_student_radio = self.page.get_by_role("radio", name="I'm a law student", exact=True)
        self.other_radio = self.page.get_by_role("radio", name="Other", exact=True)
        self.role_field = self.page.get_by_placeholder("Type your role here")

        # регистрация
        self.continue_button = self.page.get_by_role("button", name="Choose and continue")
        self.sign_up_title = self.page.get_by_role("heading", name="Sign up")
        self.email_input = self.page.get_by_placeholder("Email")
        self.sign_up_button = self.page.get_by_role("button", name="Sign up")
        self.success_notification = self.page.get_by_text("Check your inbox", exact=False)

        # логин
        self.login_button = self.page.get_by_text("Log in", exact=True)
        self.google_button = self.page.get_by_role("button").first

    def navigate(self):
        """Переход на страницу логина"""
        self.navigate_to(Config.LOGIN_URL)

    def login(self, role: str, email: str, password: str):
        """
        Полный процесс логина через Google
        """
        try:
            self.navigate()

            self.click(self.other_radio)
            self.fill(self.role_field, role)
            self.click(self.login_button)
            
            # self.wait_for(self.google_button, "visible")
            self.wait_for_visible(self.google_button)
            with self.page.expect_popup() as popup_info:
                self.click(self.google_button)
            
            google_page = GoogleAuthPage(popup_info.value)
            google_page.enter_email(email)
            google_page.enter_password(password)

            # Обрабатываем возможную верификацию
            if google_page.verification_required:
                return False

            google_page.wait_for_redirect()
            return self.page
        
        except Exception as e:
            self.take_screenshot("login_failed_")
            return False