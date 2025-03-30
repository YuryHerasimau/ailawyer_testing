import pytest
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

class TestChatSettings:
    def test_open_chat_settings(self, chat_page):
        """Тест настроек чата"""
        # Тест проверки открытия попапа настроек
        chat_page.chat_settings_button.click()
        assert chat_page.settings_popup.is_visible()
        assert chat_page.complexity_header.is_visible()
        
        # Закрываем попап
        chat_page.chat_title.click()
        chat_page.page.wait_for_timeout(1000)  # Небольшая задержка для анимации
        assert not chat_page.settings_popup.is_visible()

    @pytest.mark.parametrize("complexity, expected_option", COMPLEXITY_OPTIONS)
    def test_change_complexity_settings(self, chat_page, complexity, expected_option):
        """Тест изменения уровня сложности языка"""
        chat_page.configure_chat_settings(complexity=complexity)
        
        # Дополнительная проверка - открываем настройки снова и проверяем выбранный вариант
        chat_page.chat_settings_button.click()
        expect(chat_page.settings_popup).to_be_visible()

        # Проверяем, что выбрана правильная опция
        if complexity == "Professional":
            expect(chat_page.professional_label).to_be_checked()
            expect(chat_page.professional_radio).to_be_checked()
        elif complexity == "Regular":
            expect(chat_page.regular_label).to_be_checked()
            expect(chat_page.regular_radio).to_be_checked()
        elif complexity == "Simple":
            expect(chat_page.simple_label).to_be_checked()
            expect(chat_page.simple_radio).to_be_checked()
        
        # Закрываем попап
        chat_page.chat_title.click()

        # Добавить проверку, что настройки действительно применились,
        # например, отправив сообщение и проверив ответ

    @pytest.mark.parametrize("crazy_mode, expected_action", CRAZY_MODE_OPTIONS)
    def test_toggle_crazy_mode(self, chat_page, crazy_mode, expected_action):
        """Тест включения/выключения Crazy Mode"""
        chat_page.configure_chat_settings(crazy_mode=crazy_mode)
        
        # Дополнительная проверка - открываем настройки снова и проверяем состояние
        chat_page.chat_settings_button.click()
        
        if crazy_mode:
            expect(chat_page.crazy_mode_toggle.locator("input")).to_be_checked()
        else:
            expect(chat_page.crazy_mode_toggle.locator("input")).not_to_be_checked()
        
        # Закрываем попап
        chat_page.chat_title.click()