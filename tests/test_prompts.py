import pytest
import allure
from pages.chat_page import ChatPage
from playwright.sync_api import expect


@allure.feature("Промпты")
@pytest.mark.critical
class TestPromptsSelection:
    @allure.title("Тест открытия попапа с промптами")
    def test_prompts_popup_opens(self, chat_page: ChatPage):
        """Тест открытия попапа с промптами"""
        chat_page.open_prompts_popup()
        expect(chat_page.prompts_header).to_be_visible()


    @allure.title("Тест закрытия попапа с промптами")
    def test_close_prompts_popup(self, chat_page: ChatPage):
        chat_page.open_prompts_popup()
        chat_page.close_prompts_popup()


    @allure.title("Тест видимости основных категорий промптов")
    def test_prompts_categories_visible(self, chat_page: ChatPage):
        """Тест видимости основных категорий промптов"""
        chat_page.open_prompts_popup()
        
        # Проверяем видимость всех категорий
        for category_locator in chat_page.prompts_categories.values():
            expect(category_locator).to_be_visible()


    @allure.title("Тест сворачивания и разворачивания категорий промптов")
    def test_expand_collapse_prompt_category(self, chat_page: ChatPage):
        """Тест сворачивания и разворачивания категории промптов Custom prompts"""
        chat_page.open_prompts_popup()
        
        # Проверяем, что контейнер изначально скрыт
        expect(chat_page.custom_prompts_container).to_be_hidden()
        
        # Разворачиваем категорию
        chat_page.expand_prompt_category("Custom prompts")
        expect(chat_page.custom_prompts_container).to_be_visible()
        
        # Проверяем наличие ожидаемого промпта
        prompt_text = "Используя техники граничных условий и классов эквивалентности напиши тест-кейсы для тестирования"
        expect(chat_page.custom_prompts_container.locator(f"text={prompt_text}")).to_be_visible()
        
        # Сворачиваем категорию
        chat_page.expand_prompt_category("Custom prompts")
        expect(chat_page.custom_prompts_container).to_be_hidden()


    @allure.title("Тест выбора конкретного промпта из категории Custom prompts")
    def test_select_prompt(self, chat_page: ChatPage):
        """Тест выбора конкретного промпта из категории Custom prompts"""
        chat_page.open_prompts_popup()
        chat_page.expand_prompt_category("Custom prompts")
        
        prompt_text = "Используя техники граничных условий и классов эквивалентности напиши тест-кейсы для тестирования"
        
        # Выбираем промпт через меню
        prompt_item = chat_page.page.locator(f'div.bg-openFolder div.flex:has-text("{prompt_text}")').first
        prompt_item.hover()
        
        chat_page.prompt_menu_button.click()
        chat_page.add_to_input_button.click()
        
        expect(chat_page.message_input).to_have_value(prompt_text)


    @allure.title("Тест создания нового промпта")
    def test_create_new_prompt(self, chat_page: ChatPage):
        """Тест создания нового промпта"""
        chat_page.open_prompts_popup()
        
        expect(chat_page.create_new_prompt_button).to_be_visible()
        chat_page.create_new_prompt("Test prompt", save=False)


    @allure.title("Тест создания нового промпта с параметризацией")
    @pytest.mark.parametrize("action, test_prompt", [
        ("save", "Test prompt for save"),
        ("cancel", "Test prompt for cancel"),
    ])
    def test_create_custom_prompt(self, chat_page: ChatPage, action, test_prompt):
        """Тест создания нового промпта с параметризацией"""
        chat_page.open_prompts_popup()
        
        if action == "cancel":
            chat_page.create_new_prompt(test_prompt, save=False)
            chat_page.expand_prompt_category("Custom prompts")
            expect(chat_page.page.get_by_text(test_prompt)).not_to_be_visible()
        elif action == "save":
            chat_page.create_new_prompt(test_prompt, save=True)
            chat_page.expand_prompt_category("Custom prompts")
            expect(chat_page.page.get_by_text(test_prompt).first).to_be_visible()
            
            # Очистка
            chat_page.delete_prompt(test_prompt)