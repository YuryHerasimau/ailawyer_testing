import pytest
import allure
from pages.chat_page import ChatPage
from playwright.sync_api import expect


@allure.feature("Чат")
class TestChat:
    @pytest.mark.smoke
    def test_initial_ai_greeting(self, chat_page: ChatPage):
        """Тест проверяет начальное приветственное сообщение AI"""
        greeting = chat_page.get_greeting_text()
        
        assert "Hello, Yury 👋" in greeting['header']
        assert "Please select a question" in greeting['first_paragraph']
        assert "already existing chat from history" in greeting['second_paragraph']
        assert greeting['add_button_visible'] is True

    @pytest.mark.smoke
    @pytest.mark.parametrize("test_message", [
        "Hello AI",
        "What can you do?",
        "Explain like I'm five"
    ])
    def test_chat_flow(self, chat_page: ChatPage, test_message):
        """Тест общения с ChatGPT с параметризацией разных сообщений"""
        chat_page.send_message_and_wait_for_response(test_message)
        
        last_response = chat_page.get_last_ai_message()
        assert len(last_response) > 0, "Ответ AI пустой"
        assert len(last_response) > 100, "Ответ AI слишком короткий"
        
        chat_page.make_screenshot()

    @pytest.mark.critical
    def test_message_sequence(self, chat_page: ChatPage):
        """Тест последовательности сообщений"""
        messages = ["Hi", "How are you?", "What's new?"]
        responses = []
        
        for msg in messages:
            chat_page.send_message_and_wait_for_response(msg)
            responses.append(chat_page.get_last_ai_message())
        
        assert len(responses) == len(set(responses)), "Получили одинаковые ответы AI"

    @pytest.mark.critical
    def test_message_history(self, chat_page: ChatPage):
        """Тест истории сообщений"""
        messages = ["First message", "Second message"]
        for msg in messages:
            chat_page.send_message_and_wait_for_response(msg)
        
        assert chat_page.get_last_user_message() == messages[-1]
        assert chat_page.get_last_ai_message() != ""

    @pytest.mark.critical
    def test_regenerate_response(self, chat_page: ChatPage):
        """Тест регенерации ответа"""
        chat_page.send_message_and_wait_for_response("Test regenerate")
        first_response = chat_page.get_last_ai_message()
        
        chat_page.regenerate_response()
        chat_page.wait_for_ai_response()
        
        second_response = chat_page.get_last_ai_message()
        assert first_response != second_response
