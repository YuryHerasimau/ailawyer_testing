import os
import time
from playwright.sync_api import sync_playwright, expect
from dotenv import load_dotenv

load_dotenv()

GOOGLE_EMAIL = os.getenv("GOOGLE_EMAIL")
GOOGLE_PASS = os.getenv("GOOGLE_PASS")


def test_ailawyer_auth():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, args=["--disable-blink-features=AutomationControlled"])
        context = browser.new_context()
        page = context.new_page()

        page.goto("https://app.ailawyer.pro/")
        page.get_by_role("radio", name="I'm a legal consumer").click()
        page.get_by_role("button", name="Choose and continue").click()

        with page.expect_popup() as page1_info:
            page.get_by_role("button").first.click()

        page1 = page1_info.value

        page1.get_by_role("textbox", name="Email or phone").fill(GOOGLE_EMAIL)
        page1.get_by_role("textbox", name="Email or phone").click()
        page1.get_by_role("button", name="Next").click()

        page1.get_by_role("textbox", name="Enter your password").fill(GOOGLE_PASS)
        page1.get_by_role("textbox", name="Enter your password").click()
        page1.get_by_role("button", name="Next").click()

        # Ожидание перехода на страницу чатов
        expect(page).to_have_url("https://app.ailawyer.pro/chats/", timeout=30000)

        # Проверка наличия надписи "New chat" в хедере
        expect(page.get_by_role("heading", name="New Chat")).to_be_visible()

        # Проверка наличия кнопки с надписью "New chat" в сайдбаре
        expect(page.get_by_role("button", name="New Chat")).to_be_visible()

        time.sleep(10)

        context.close()
        browser.close()

        print("Тест прошел успешно")
