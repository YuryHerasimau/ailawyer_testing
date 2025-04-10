import pytest
import allure
from pages.chat_page import ChatPage
from playwright.sync_api import expect


# Параметры для теста сложности языка
COMPLEXITY_OPTIONS = [
    ("Professional", "professional"),
    ("Regular", "regular"),
    ("Simple", "simple")
]

# Параметры для теста Crazy Mode
CRAZY_MODE_OPTIONS = [
    (True, "enable"),
    (False, "disable")
]

@allure.feature("Настройки чата")
@pytest.mark.critical
class TestChatSettings:
    def test_open_chat_settings(self, chat_page: ChatPage):
        """Тест открытия и закрытия настроек чата"""
        chat_page.open_chat_settings()
        chat_page.close_chat_settings()

    @pytest.mark.parametrize("complexity, _", COMPLEXITY_OPTIONS)
    def test_change_complexity_settings(self, chat_page: ChatPage, complexity, _):
        """Тест изменения уровня сложности языка"""
        chat_page.configure_chat_settings(complexity=complexity)
        
        # Проверяем, что настройки сохранились
        chat_page.open_chat_settings()
        
        if complexity == "Professional":
            expect(chat_page.professional_radio).to_be_checked()
        elif complexity == "Regular":
            expect(chat_page.regular_radio).to_be_checked()
        elif complexity == "Simple":
            expect(chat_page.simple_radio).to_be_checked()
        
        chat_page.close_chat_settings()

        # Добавить проверку, что настройки действительно применились,
        # например, отправив сообщение и проверив ответ

    @pytest.mark.parametrize("crazy_mode, _", CRAZY_MODE_OPTIONS)
    def test_toggle_crazy_mode(self, chat_page: ChatPage, crazy_mode, _):
        """Тест включения/выключения Crazy Mode"""
        chat_page.configure_chat_settings(crazy_mode=crazy_mode)
        
        # Проверяем состояние переключателя
        chat_page.open_chat_settings()
        
        if crazy_mode:
            expect(chat_page.crazy_mode_toggle.locator("input")).to_be_checked()
        else:
            expect(chat_page.crazy_mode_toggle.locator("input")).not_to_be_checked()
        
        chat_page.close_chat_settings()