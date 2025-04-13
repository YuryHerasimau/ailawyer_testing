import os
import pytest
import allure
from playwright.sync_api import expect
from dotenv import load_dotenv
from pages.google_auth_page import GoogleAuthPage
from pages.login_page import LoginPage
from config import Config

load_dotenv(override=True) # Принудительная перезагрузка

@allure.feature("Авторизация")
class TestLogin:
    @pytest.fixture(autouse=True)
    def setup(self, login_page: LoginPage):
        self.login_page = login_page
        self.config = Config
        self.login_page.navigate()

    @allure.title("Тест авторизации через Google")
    @pytest.mark.smoke
    def test_login(self):
        """Тест авторизации через Google"""
        with allure.step("Выполнение авторизации"):
            login_success = self.login_page.login(
                role="Test",
                email=os.getenv("GOOGLE_EMAIL"),
                password=os.getenv("GOOGLE_PASS")
            )

        if not login_success:
            pytest.skip("Требуется верификация по телефону (Google bot protection)")

        with allure.step("Проверка успешной авторизации"):
            expect(self.login_page.page).to_have_url(self.config.CHATS_URL, timeout=30000)


    @allure.title("Тест неверного пароля")
    @pytest.mark.critical
    def test_incorrect_password(self):
        """Тест неверного пароля"""
        with allure.step("1. Запускаем процесс авторизации"):
            self.login_page.navigate()

            with allure.step("1.1. Проверяем переключение ролей"):
                with allure.step("Проверяем переключение на 'legal consumer'"):
                    self.login_page.legal_consumer_radio.click()
                    expect(self.login_page.legal_consumer_radio).to_be_checked()
                
                with allure.step("Проверяем переключение на 'lawyer'"):
                    self.login_page.lawyer_radio.click()
                    expect(self.login_page.lawyer_radio).to_be_checked()
                
                with allure.step("Проверяем переключение на 'law student'"):
                    self.login_page.law_student_radio.click()
                    expect(self.login_page.law_student_radio).to_be_checked()

                with allure.step("Проверяем переключение на 'other'"):
                    self.login_page.other_radio.click()
                    expect(self.login_page.other_radio).to_be_checked()
                
                    with allure.step("Проверяем заполнение поля 'role'"):
                        self.login_page.role_field.fill("Test")
                        expect(self.login_page.role_field).to_have_value("Test")

            self.login_page.login_button.click()
            
            # Ждем открытия popup Google Auth
            with self.login_page.page.expect_popup() as popup_info:
                self.login_page.google_button.click()
            google_page = GoogleAuthPage(popup_info.value)
        
        with allure.step("2. Вводим корректный email"):
            google_page.enter_email(os.getenv("GOOGLE_EMAIL"))
        
        with allure.step("3. Вводим неверный пароль"):
            google_page.enter_password("incorrect_password")
            
            # Явное ожидание ошибки (важно!)
            error_locator = google_page.page.get_by_text(
                "Wrong password. Try again or click Forgot password to reset it.",
                exact=False  # exact=False для частичного совпадения
            )
            
            with allure.step("4. Проверяем отображение сообщения об ошибке"):
                try:
                    error_locator.wait_for(state="visible", timeout=10000)
                    allure.attach(
                        google_page.page.screenshot(),
                        name="password_error",
                        attachment_type=allure.attachment_type.PNG
                    )
                    print("Error message displayed correctly")
                except Exception as e:
                    print(f"Error message not found: {str(e)}")
                    google_page.take_screenshot("password_error_missing")
                    raise AssertionError("Сообщение об ошибке пароля не появилось")
        
        with allure.step("5. Проверяем отсутствие редиректа"):
            assert self.config.CHATS_URL not in google_page.page.url, \
                "Произошел редирект несмотря на неверный пароль"
            print(f"Current URL: {google_page.page.url[:50]}*** (no redirect as expected)")

@allure.feature("Регистрация по email")
class TestEmailRegistration:
    @pytest.fixture(autouse=True)
    def setup(self, login_page: LoginPage):
        """Подготовка страницы регистрации"""
        self.login_page = login_page
        self.login_page.navigate()
        self.login_page.lawyer_radio.click()
        self.login_page.continue_button.click()
        expect(self.login_page.sign_up_title).to_be_visible()

    @allure.title("Позитивные проверки регистрации по email")
    @pytest.mark.parametrize("email", ["test@test.com", "user@example.com"])
    @pytest.mark.smoke
    def test_valid_email_registration(self, email):
        """Тест успешной регистрации по email"""
        with allure.step("Ввод валидного email и отправка формы"):
            expect(self.login_page.email_input).to_be_empty()
            self.login_page.email_input.fill(email)
            expect(self.login_page.email_input).to_have_value(email)
            expect(self.login_page.sign_up_button).to_be_enabled()
            self.login_page.sign_up_button.click()
        
        with allure.step("Проверяем сообщение о подтверждении"):
            expect(self.login_page.success_notification).to_be_visible()
            expect(self.login_page.success_notification).to_contain_text("Check your inbox")
    
    @allure.title("Негативные проверки валидации email")
    @pytest.mark.parametrize(
        "invalid_email", [("   "), ("invalid"), ("test@test.com"), ("user@example.com")]
    )
    @pytest.mark.critical
    def test_invalid_email_registration(self, invalid_email):
        """Тест валидации email"""
        with allure.step("Проверяем, что кнопка заблокирована по умолчанию"):
            expect(self.login_page.sign_up_button).to_be_disabled()

        with allure.step("Ввод невалидного email"):
            self.login_page.email_input.fill(invalid_email)

        with allure.step("Проверка подсветки поля красной рамкой"):
            expect(self.login_page.email_input).to_have_css(
                "border-color",
                "rgb(255, 0, 0)"
            )
        
        with allure.step("Проверяем, что кнопка заблокирована после ввода невалидного email"):
            expect(self.login_page.sign_up_button).to_be_disabled()
