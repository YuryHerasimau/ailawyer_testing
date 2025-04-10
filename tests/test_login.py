import os
import pytest
import allure
from playwright.sync_api import expect
from dotenv import load_dotenv
from pages.login_page import LoginPage
from config import Config

load_dotenv(override=True) # Принудительная перезагрузка

@pytest.fixture
def google_credentials():
    return {
        "email": os.getenv("GOOGLE_EMAIL"),
        "password": os.getenv("GOOGLE_PASS"),
        "phone": os.getenv("GOOGLE_PHONE")
    }


@allure.feature("Авторизация")
@allure.title("Тест авторизации через Google")
@pytest.mark.smoke
def test_login(page, google_credentials):
    """Тест авторизации через Google"""
    login_page = LoginPage(page)
    login_page.navigate()

    with allure.step("Выполнение авторизации"):
        # Маскируем чувствительные данные в отчете
        with allure.step(f"Авторизация пользователя {google_credentials['email'][:3]}***"):
            login_success = login_page.login(
                role="Test",
                email=google_credentials["email"],
                password=google_credentials["password"]
            )

    if not login_success:
        pytest.skip("Требуется верификация по телефону")

    with allure.step("Проверка успешной авторизации"):
        expect(page).to_have_url(Config.CHATS_URL, timeout=30000)