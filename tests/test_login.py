import os
import time
from pages.login_page import LoginPage
from playwright.sync_api import expect
from dotenv import load_dotenv

load_dotenv()
GOOGLE_EMAIL = os.getenv("GOOGLE_EMAIL")
GOOGLE_PASS = os.getenv("GOOGLE_PASS")


def test_login(page):
    login_page = LoginPage(page)
    login_page.navigate()

    # Выполняем вход
    login_page.login("Test", GOOGLE_EMAIL, GOOGLE_PASS)

    # Проверяем редирект на страницу чатов
    expect(page).to_have_url("https://app.ailawyer.pro/chats/", timeout=30000)

    # Проверяем наличие элементов на странице чатов
    expect(
        page.get_by_role("heading", name="New Chat"),
        "Надпись 'New Chat' не отображается в хедере страницы",
    ).to_contain_text("New Chat")

    expect(page.get_by_role("heading", name="New Chat")).to_be_visible()

    time.sleep(3)
