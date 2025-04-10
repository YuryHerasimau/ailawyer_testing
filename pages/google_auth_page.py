import time
import logging
from playwright.sync_api import Page, expect
from conftest import check_captcha
from config import Config


logger = logging.getLogger(__name__)

class GoogleAuthPage:
    def __init__(self, page: Page):
        self.page = page
        self.email_field = page.get_by_role("textbox", name="Email or phone")
        self.password_field = page.get_by_role("textbox", name="Enter your password")
        self.next_button = page.get_by_role("button", name="Next")
        # Верификаця по телефону
        self.verification_required = False
        self.verification_header = page.get_by_text("Verify it's you")


    def enter_email(self, email: str):
        logger.info("Entering email...")
        try:
            check_captcha(self.page) # Проверка CAPTCHA
            self.email_field.fill(email)
            self.next_button.click()
        except Exception as e:
            self.page.screenshot(path="screenshots/google_auth_error.png")
            raise Exception(f"Failed to enter email: {str(e)}")


    def enter_password(self, password: str):
        logger.info("Entering password...")
        try:
            self.password_field.wait_for(state="visible", timeout=30000)
            check_captcha(self.page) # Проверка CAPTCHA
            self.password_field.fill(password)
            self.next_button.click()

            # Проверяем, не появилось ли требование верификации по телефону
            if self.verification_header.is_visible(timeout=5000):
                self.verification_required = True
                self.page.screenshot(path="screenshots/verification_required.png")

        except Exception as e:
            self.page.screenshot(path="screenshots/google_auth_error.png")
            raise Exception(f"Failed to enter password: {str(e)}")


    def wait_for_redirect(self, timeout=90000):
        try:
            with self.page.expect_event("close", timeout=timeout):
                pass
        except:
            self.page.wait_for_url(
                Config.CHATS_URL,
                timeout=timeout,
                wait_until="networkidle"
            )