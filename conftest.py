import pytest
from playwright.sync_api import sync_playwright, expect
from pages.login_page import LoginPage
from pages.chat_page import ChatPage
from dotenv import load_dotenv
import os

load_dotenv()


@pytest.fixture(scope="session")
def browser():
    """Запуск браузера с параметрами"""
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            headless=False,
            args=["--disable-blink-features=AutomationControlled"]
        )
        yield browser
        browser.close()

@pytest.fixture
def context(browser):
    """Создание контекста с настройками"""
    context = browser.new_context(
        viewport={"width": 1700, "height": 1000},
    )
    yield context
    context.close()

@pytest.fixture
def page(context):
    """Создание новой страницы с таймаутами"""
    page = context.new_page()
    page.set_default_timeout(10000)  # 10 секунд таймаут по умолчанию
    page.set_default_navigation_timeout(20000)
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
    
    google_auth_page = login_page.login(
        role="Test",
        email=os.getenv("GOOGLE_EMAIL"),
        password=os.getenv("GOOGLE_PASS")
    )
    
    expect(page).to_have_url("https://app.ailawyer.pro/chats/", timeout=30000)
    return page

@pytest.fixture
def chat_page(authed_page):
    """Фикстура для работы с чатом"""
    return ChatPage(authed_page)