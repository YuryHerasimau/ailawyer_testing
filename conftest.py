import pytest
from playwright.sync_api import sync_playwright


@pytest.fixture
def browser():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False, args=["--disable-blink-features=AutomationControlled"])
        context = browser.new_context(viewport={"width": 1700, "height": 1000})
        page = context.new_page()
        yield page
        page.close()
        browser.close()
