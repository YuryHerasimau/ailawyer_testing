import os
import time
from playwright.sync_api import expect
from dotenv import load_dotenv

load_dotenv()

GOOGLE_EMAIL = os.getenv("GOOGLE_EMAIL")
GOOGLE_PASS = os.getenv("GOOGLE_PASS")


def test_login(browser):
    page = browser

    # Шаг 1 - Открыть страницу
    page.goto("https://app.ailawyer.pro/")

    # Шаг 2 - Проверить, что открыт корректный url
    expect(page).to_have_url("https://app.ailawyer.pro/login/")

    # Шаг 3 - Выбрать вариант "Other" и заполнить поле "Type your role here"
    page.get_by_role("radio", name="Other", exact=True).click()
    page.get_by_placeholder("Type your role here").fill("Test")
    page.get_by_text("Log in", exact=True).click()

    # Шаг 4 - Выбрать вариант "Google" и заполнить поля авторизации
    with page.expect_popup() as page1_info:
        page.get_by_role("button").first.click()

    page1 = page1_info.value
    page1.get_by_role("textbox", name="Email or phone").fill(GOOGLE_EMAIL)
    page1.get_by_role("button", name="Next").click()
    page1.get_by_role("textbox", name="Enter your password").fill(GOOGLE_PASS)
    page1.get_by_role("button", name="Next").click()

    # Шаг 5 - Проверить, что открыт корректный url
    expect(page).to_have_url("https://app.ailawyer.pro/chats/", timeout=30000)

    # Шаг 6 - Проверить наличие надписи "New chat" в хедере
    expect(
        page.get_by_role("heading", name="New Chat"),
        "Надпись 'New Chat' не отображается в хедере страницы"
    ).to_contain_text("New Chat")

    time.sleep(3)
