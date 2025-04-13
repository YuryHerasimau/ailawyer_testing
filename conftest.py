import os
import logging
import pytest
from playwright.sync_api import sync_playwright, expect
from pages.login_page import LoginPage
from pages.chat_page import ChatPage
from utils.captcha import check_captcha
from dotenv import load_dotenv
from config import Config

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
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
            logger.error(f"Failed to take screenshot: {str(e)}")


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
    
    # # Проверка CAPTCHA перед авторизацией
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