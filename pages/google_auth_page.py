import logging
from pages.base_page import BasePage
from playwright.sync_api import Page
from utils.captcha import check_captcha
from config import Config


logger = logging.getLogger(__name__)

class GoogleAuthPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.email_field = page.get_by_role("textbox", name="Email or phone")
        self.password_field = page.get_by_role("textbox", name="Enter your password")
        self.next_button = page.get_by_role("button", name="Next")
        self.verification_required = False

    def enter_email(self, email: str):
        """Ввод email с обработкой капчи"""
        logger.info("Entering email...")
        check_captcha(self.page) # Проверка CAPTCHA
        self.fill(self.email_field, email)
        self.click(self.next_button)
        self.page.wait_for_timeout(2000) # Краткая пауза для анимации


    def enter_password(self, password: str):
        """Ввод пароля с обработкой возможной верификации"""
        logger.info("Entering password...")
        try:
            # self.password_field.wait_for(state="visible", timeout=30000)
            self.wait_for_visible(self.password_field, timeout=30000)
            check_captcha(self.page) # Проверка CAPTCHA
            self.fill(self.password_field, password)
            self.click(self.next_button)

            self.page.wait_for_timeout(3000)

            # Проверяем, не появилось ли требование верификации по телефону
            verification_texts = [
                "Verify it's you",
                "Enter a phone number"
            ]
            for text in verification_texts:
                if self.page.get_by_text(text, exact=False).is_visible():
                    logger.warning("⚠️ Google triggered bot verification (phone number required)")
                    self.verification_required = True
                    self.take_screenshot("google_bot_check_")

        except Exception as e:
            self.take_screenshot("password_entry_failed_")
            raise Exception(f"Password entry failed: {str(e)}")


    def wait_for_redirect(self, timeout=60000):
        """Ожидание редиректа после успешного логина"""
        logger.info("Waiting for redirect...")
        try:
            with self.page.expect_event("close", timeout=timeout):
                pass
        except:
            self.page.wait_for_url(
                Config.CHATS_URL,
                timeout=timeout,
                wait_until="networkidle"
            )