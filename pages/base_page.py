import logging
from typing import Optional
from playwright.sync_api import Page, Locator, expect

logger = logging.getLogger(__name__)

class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.default_timeout = 10000 

    # Навигация
    def navigate_to(self, url: str, timeout: Optional[int] = None):
        """Переход по URL с проверкой"""
        timeout = timeout or self.default_timeout
        self.page.goto(url)
        expect(self.page).to_have_url(url, timeout=timeout)
        logger.info(f"Navigated to URL: {url}")

    def get_url(self):
        """Получение текущего URL"""
        return self.page.url

    # Базовые взаимодействия
    def click(self, locator: Locator, timeout: Optional[int] = None):
        """Клик с ожиданием и обработкой ошибок"""
        timeout = timeout or self.default_timeout
        try:
            locator.wait_for(state="visible", timeout=timeout)
            locator.click()
            logger.debug(f"Clicked on element: {locator}")
        except Exception as e:
            self._handle_error(f"Failed to click on element: {locator}", e)

    def fill(self, locator: Locator, text: str):
        """Заполнение поля с ожиданием"""
        timeout = self.default_timeout
        try:
            locator.wait_for(state="visible", timeout=timeout)
            locator.fill(text)
            logger.debug(f"Filled field {locator} with text: {text}")
        except Exception as e:
            self._handle_error(f"Failed to fill field {locator} with text: {text}", e)

    def get_text(self, locator: Locator, timeout: Optional[int] = None):
        """Получение текста элемента"""
        timeout = timeout or self.default_timeout
        try:
            locator.wait_for(state="visible", timeout=timeout)
            return locator.text_content().strip()
        except Exception as e:
            self._handle_error(f"Failed to get text from element: {locator}", e)
            return ""

    # Ожидания
    def wait_for_visible(self, locator: Locator, timeout: Optional[int] = None):
        """Явное ожидание видимости элемента"""
        timeout = timeout or self.default_timeout
        locator.wait_for(state="visible", timeout=timeout)

    def wait_for_hidden(self, locator: Locator, timeout: Optional[int] = None):
        """Явное ожидание скрытия элемента"""
        timeout = timeout or self.default_timeout
        locator.wait_for(state="hidden", timeout=timeout)

    # Проверки
    def should_have_text(self, locator: Locator, text: str, timeout: Optional[int] = None):
        """Проверка наличия текста в элементе"""
        timeout = timeout or self.default_timeout
        expect(locator).to_have_text(text, timeout=timeout)

    def should_be_empty(self, locator: Locator, timeout: Optional[int] = None):
        """Проверка пустоты элемента"""
        timeout = timeout or self.default_timeout
        expect(locator).to_be_empty(timeout=timeout)

    def should_be_visible(self, locator: Locator, timeout: Optional[int] = None):
        """Проверка видимости элемента"""
        timeout = timeout or self.default_timeout
        expect(locator).to_be_visible(timeout=timeout)
    
    def should_not_be_visible(self, locator: Locator, timeout: Optional[int] = None):
        """Проверка скрытия элемента"""
        timeout = timeout or self.default_timeout
        expect(locator).not_to_be_visible(timeout=timeout)

    # Обработка ошибок
    def _handle_error(self, message: str, exception: Exception):
        """Обработка ошибок со скриншотом"""
        logger.error(message)
        self.take_screenshot("error_")
        raise type(exception)(f"{message}. Original error: {str(exception)}")

    def take_screenshot(self, prefix: str = ""):
        """Скриншот с timestamp"""
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = f"screenshots/{prefix}{timestamp}.png"
        self.page.screenshot(path=path, full_page=True)
        logger.info(f"Screenshot saved to: {path}")
    