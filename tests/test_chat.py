import pytest
from playwright.sync_api import expect


class TestChat:
    def test_initial_ai_greeting(self, chat_page):
        """Тест проверяет начальное приветственное сообщение AI"""
        expect(chat_page.page, "Страница не открылась").to_have_url("https://app.ailawyer.pro/chats/")
        greeting = chat_page.get_greeting_text()
        
        assert "Hello, Yury 👋" in greeting['header']
        assert "Please select a question" in greeting['first_paragraph']
        assert "already existing chat from history" in greeting['second_paragraph']
        assert greeting['add_button_visible'] is True

    @pytest.mark.parametrize("test_message", [
        "Hello AI",
        "What can you do?",
        "Explain like I'm five"
    ])
    def test_chat_flow(self, chat_page, test_message):
        """Тест общения с ChatGPT с параметризацией разных сообщений"""
        # Проверка начального состояния
        expect(chat_page.page, "Страница не открылась").to_have_url("https://app.ailawyer.pro/chats/")
        expect(chat_page.message_input, "Поле ввода сообщений не пустое").to_be_empty()
        
        # Отправка сообщения
        chat_page.send_message(test_message)
        
        # Проверка отправленного сообщения
        expect(chat_page.user_messages.last, f"Сообщение '{test_message}' не отправлено").to_contain_text(test_message)
        
        # Ожидание ответа
        chat_page.wait_for_ai_response()

        # Проверка ответа
        last_response = chat_page.get_last_ai_message()
        normalized_response = " ".join(last_response.split())  # Удаляем лишние пробелы

        print(f"\n--- Полный ответ AI ---\n{normalized_response}\n---")

        assert len(normalized_response) > 0, "Ответ AI пустой"
        assert len(normalized_response) > 100, "Ответ AI слишком короткий"  # Проверка длины
        assert any(word in normalized_response.lower() for word in ["step", "advice", "suggest"]), "Ответ должен содержать рекомендации"
        
        # Дополнительные проверки ответа
        expect(chat_page.ai_message_blocks.last, "Ответ AI не отображается").to_be_visible()

        # Скриншот после всех проверок
        chat_page.make_screenshot()

    def test_message_sequence(self, chat_page):
        """Тест последовательности сообщений"""
        messages = ["Hi", "How are you?", "What's new?"]
        responses = []
        
        for msg in messages:
            chat_page.send_message(msg)
            expect(chat_page.user_messages.last, f"Сообщение '{msg}' не отправлено").to_contain_text(msg)
            
            chat_page.wait_for_ai_response()
            response = chat_page.get_last_ai_message()
            assert response, "Ответ AI пустой"
            responses.append(response)
        
        # Проверяем, что получили уникальные ответы
        assert len(responses) == len(set(responses)), "Получили одинаковые ответы AI"

    def test_message_history(self, chat_page):
        """Тест истории сообщений"""
        # Отправляем два сообщения
        messages = ["First message", "Second message"]
        for msg in messages:
            chat_page.send_message(msg)
            chat_page.wait_for_ai_response()
        
        # Проверяем историю
        assert chat_page.get_last_user_message() == messages[-1]
        assert chat_page.get_last_ai_message() != ""

    def test_regenerate_response(self, chat_page):
        """Тест регенерации ответа"""
        chat_page.send_message("Test regenerate")
        first_response = chat_page.get_last_ai_message()
        chat_page.regenerate_response()
        chat_page.wait_for_ai_response()
        second_response = chat_page.get_last_ai_message()
        assert first_response != second_response
