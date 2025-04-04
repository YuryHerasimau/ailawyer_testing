import os
import pytest
from playwright.sync_api import expect
from dotenv import load_dotenv
from pages.login_page import LoginPage

load_dotenv()

@pytest.fixture
def google_credentials():
    return {
        "email": os.getenv("GOOGLE_EMAIL"),
        "password": os.getenv("GOOGLE_PASS")
    }

@pytest.mark.smoke
def test_login(page, google_credentials):
    """Тест авторизации через Google"""
    login_page = LoginPage(page)
    login_page.navigate()

    login_page.login(
        role="Test",
        email=google_credentials["email"],
        password=google_credentials["password"]
    )

    expect(page).to_have_url("https://app.ailawyer.pro/chats/", timeout=30000)
