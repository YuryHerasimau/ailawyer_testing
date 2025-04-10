import os
import logging
import random
import pytest
from playwright.sync_api import sync_playwright, expect, Page
from playwright_stealth import stealth_sync
from pages.login_page import LoginPage
from pages.chat_page import ChatPage
from dotenv import load_dotenv
from datetime import datetime
from config import Config

load_dotenv()

logging.basicConfig(level=logging.INFO)
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


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


@pytest.fixture(autouse=True)
def take_screenshot_on_failure(request, page):
    """Делает скриншот при падении теста"""
    yield
    
    # Проверяем все возможные статусы
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        os.makedirs("screenshots", exist_ok=True)
        test_name = request.node.name.replace("[", "_").replace("]", "_")
        screenshot_path = f"screenshots/failure_{test_name}.png"
        
        try:
            page.screenshot(path=screenshot_path, full_page=True)
            logger.info(f"Screenshot saved to {screenshot_path}")
        except Exception as e:
            logger.error(f"Failed to take screenshot: {e}")


@pytest.fixture(scope="session")
def browser():
    """Запуск браузера с параметрами"""
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled",
            ]
        )
        yield browser
        browser.close()


@pytest.fixture
def context(browser):
    """Создание контекста с настройками"""
    context = browser.new_context(
        viewport={"width": 1280, "height": 720},
    )
    yield context
    context.close()


@pytest.fixture
def page(context):
    """Создание новой страницы"""
    page = context.new_page()
    yield page
    page.close()


@pytest.fixture
def login_page(page):
    """Фикстура для страницы логина"""
    return LoginPage(page)


@pytest.fixture
def authed_page(page):
    login_page = LoginPage(page)
    login_page.navigate()
    
    # Проверка CAPTCHA перед авторизацией
    check_captcha(page)

    google_auth_page = login_page.login(
        role="Test",
        email=os.getenv("GOOGLE_EMAIL"),
        password=os.getenv("GOOGLE_PASS")
    )
    
    expect(page).to_have_url(Config.CHATS_URL, timeout=30000)
    return page

@pytest.fixture
def chat_page(authed_page):
    """Фикстура для работы с чатом"""
    return ChatPage(authed_page)