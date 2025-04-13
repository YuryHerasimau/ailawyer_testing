import os
import logging
from playwright.sync_api import Page
from datetime import datetime

logger = logging.getLogger(__name__)


def check_captcha(page: Page):
    """Проверяет наличие CAPTCHA и делает скриншот если найдена"""
    captcha_selectors = [
        "text=CAPTCHA",
        "text=Verify you're not a robot",
        "div.recaptcha",
        "#captcha",
        "iframe[src*='recaptcha']",
        "iframe[src*='recaptcha']",
        "text=This browser or app may not be secure",
        "text=Try using a different browser"
    ]
    
    for selector in captcha_selectors:
        if page.locator(selector).is_visible():
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = f"screenshots/captcha_{timestamp}.png"
            os.makedirs("screenshots", exist_ok=True)
            page.screenshot(path=screenshot_path)
            logger.error(f"CAPTCHA detected! Captcha: {selector}. Screenshot saved to {screenshot_path}")
            raise Exception("CAPTCHA verification required")