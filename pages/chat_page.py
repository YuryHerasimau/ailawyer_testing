import time
from typing import Any, Dict, List
from pages.base_page import BasePage
from playwright.sync_api import Page, expect


class ChatPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self._init_locators()

    def _init_locators(self):
        """Инициализация всех локаторов"""
        self._init_welcome_locators()
        self._init_input_locators()
        self._init_message_locators()
        self._init_additional_elements_locators()
        self._init_prompts_popup_locators()
        self._init_pin_chat_locators()
        self._init_chat_settings_locators()

    def _init_welcome_locators(self):
        """Локаторы для приветственного сообщения"""
        self.greeting_block = self.page.locator('div.bg-aiMessage').first
        self.greeting_header = self.greeting_block.locator('h2')
        self.greeting_paragraphs = self.greeting_block.locator('p')
        self.add_button = self.greeting_block.locator('button:has-text("Add")')

    def _init_input_locators(self):
        """Локаторы для поля ввода"""
        self.message_input = self.page.get_by_placeholder("Type your message here")
        self.send_button = self.message_input.locator('xpath=./following-sibling::button[1]')
        self.chat_title = self.page.locator('h1.text-xl')

    def _init_message_locators(self):
        """Локаторы для сообщений"""
        self.ai_message_blocks = self.page.locator('div.bg-aiMessage:has(p)')  # Блоки сообщений AI
        self.user_messages = self.page.locator('div.myMessage p')

    def _init_additional_elements_locators(self):
        """Локаторы для дополнительных элементов"""
        self.internet_button = self.page.locator('//div[contains(@class, "bg-aiMessage")]//span[contains(text(), "Internet")]')
        self.prompts_button = self.page.locator('//div[contains(@class, "group") and contains(text(), "Prompts")]')
        self.regenerate_button = self.page.locator('xpath=//button[.//p[contains(text(), "Regenerate Response")]]')

    def _init_prompts_popup_locators(self):
        """Локаторы для попапа с промптами"""
        self.prompts_popup = self.page.locator('text=Prompts Base')
        self.prompts_header = self.page.locator('text=Choose the prompt that suits you best')
        self.prompts_close_button = self.page.locator('div[class*="bg-white"] header button')
        self.create_new_prompt_button = self.page.get_by_text("Create new prompt", exact=True)
        
        # Категории промптов
        self._init_prompts_categories()
        
        # Custom prompts
        self.custom_prompts_category_button = self.page.locator('button:has-text("Custom prompts")')
        self.custom_prompts_container = self.custom_prompts_category_button.locator('xpath=./following-sibling::div[contains(@class, "bg-openFolder")][1]')
        
        # Форма создания промпта
        self.create_prompt_form_title = self.page.get_by_text("Create your own quick access prompt")
        self.prompt_input_field = self.page.get_by_placeholder("Your prompt")
        self.cancel_prompt_button = self.page.get_by_text("Cancel", exact=True)
        self.save_prompt_button = self.page.get_by_text("Save", exact=True)
        
        # Меню промпта
        self.prompt_menu_button = self.page.locator('button:has(> svg)').first
        self.add_to_input_button = self.page.locator('button:has-text("Add to input field")')
        self.delete_prompt_button = self.page.locator('button:has-text("Delete prompt")')
        self.delete_prompt_confirm = self.page.get_by_text("Delete", exact=True).first

    def _init_prompts_categories(self):
        """Инициализация локаторов для категорий промптов"""
        self.prompts_categories = {
            "custom_prompts": self.page.locator('text=Custom prompts'),
            "legal_consumers": self.page.locator('text=Prompts for Legal Consumers'),
            "legal_research": self.page.locator('text=Prompts for Legal Research'),
            "drafting_legal_documents": self.page.locator('text=Prompts for Drafting Legal Documents'),
            "family_lawyers": self.page.locator('text=Prompts for Family Lawyers'),
            "personal_injury_lawyers": self.page.locator('text=Prompts for Personal Injury Lawyers'),
            "employment_labor_lawyers": self.page.locator('text=Prompts for Employment and Labor Lawyers'),
            "immigration_lawyers": self.page.locator('text=Prompts for Immigration Lawyers'),
            "business_lawyers": self.page.locator('text=Prompts for Business Lawyers'),
            "tax_lawyers": self.page.locator('text=Prompts for Tax Lawyers'),
            "real_estate_lawyers": self.page.locator('text=Prompts for Real Estate Lawyers'),
            "ip_lawyers": self.page.locator('text=Prompts for Intellectual Property (IP) Lawyers'),
            "criminal_defense_lawyers": self.page.locator('text=Prompts for Criminal Defense Lawyers')
        }

    def _init_pin_chat_locators(self):
        """Локаторы для закрепления чата"""
        self.pin_button = self.page.locator('button:has(.icon[style*="pin-dark.svg"])')

    def _init_chat_settings_locators(self):
        """Локаторы для настройки чата"""
        self.chat_settings_button = self.page.locator('button:has(svg path[d*="M9.594 3.94c"])')
        self.settings_popup = self.page.locator('div[class*="bg-white shadow-shadow"]:has(header h3)')
        self.complexity_header = self.settings_popup.locator('header h3:has-text("Language complexity")')
        
        # Радиокнопки
        self.professional_label = self.settings_popup.locator('label:has-text("Professional")')
        self.regular_label = self.settings_popup.locator('label:has-text("Regular")')
        self.simple_label = self.settings_popup.locator('label:has-text("Simple")')
        self.professional_radio = self.settings_popup.locator('input[name="Professional"]')
        self.regular_radio = self.settings_popup.locator('input[name="Regular"]')
        self.simple_radio = self.settings_popup.locator('input[name="Simple"]')
        
        # Crazy Mode
        self.crazy_mode_toggle = self.settings_popup.locator('div:has-text("Crazy Mode") >> label')

    # Методы для работы с промптами
    def open_prompts_popup(self):
        """Открывает попап с промптами"""
        self.click(self.prompts_button)
        self.wait_for_visible(self.prompts_popup)

    def close_prompts_popup(self):
        """Закрывает попап с промптами"""
        self.click(self.prompts_close_button)
        self.wait_for_hidden(self.prompts_popup)

    def expand_prompt_category(self, category_name):
        """Разворачивает категорию промптов"""
        normalized_name = category_name.lower().replace(" ", "_")
        category_locator = self.prompts_categories.get(normalized_name)
        if category_locator:
            self.click(category_locator)
        else:
            raise ValueError(f"Категория '{category_name}' не найдена")

    def select_prompt_by_text(self, prompt_text):
        """Выбирает промпт по тексту"""
        prompt_item = self.page.locator(f'div.bg-openFolder div.flex:has-text("{prompt_text}")').first
        self.wait_for_visible(prompt_item)
        self.click(prompt_item)

    def create_new_prompt(self, prompt_text, save=True):
        """Создает новый промпт"""
        self.click(self.create_new_prompt_button)
        self.should_be_visible(self.create_prompt_form_title)
        
        self.fill(self.prompt_input_field, prompt_text)
        self.should_have_text(self.prompt_input_field, prompt_text)
        
        if save:
            self.click(self.save_prompt_button)
        else:
            self.click(self.cancel_prompt_button)        
        self.wait_for_hidden(self.create_prompt_form_title)

    def delete_prompt(self, prompt_text):
        """Удаляет промпт"""
        prompt_item = self.page.locator(f'div.bg-openFolder div.flex:has-text("{prompt_text}")').first
        prompt_item.hover()
        
        self.click(self.prompt_menu_button)
        self.click(self.delete_prompt_button)
        
        self.should_be_visible(self.page.locator('text=Delete prompt?'))
        self.click(self.delete_prompt_confirm)
        self.wait_for_hidden(prompt_item)

    # Остальные методы класса остаются без изменений
    def get_greeting_text(self) -> Dict[str, Any]:
        """Возвращает все части приветственного сообщения в виде словаря"""
        return {
            'header': self.get_text(self.greeting_header),
            # 'first_paragraph': self.get_text(self.greeting_paragraphs.nth(0)),
            # 'second_paragraph': self.get_text(self.greeting_paragraphs.nth(1)),
            'paragraphs': [self.get_text(p) for p in self.greeting_paragraphs.all()],
            'add_button_visible': self.add_button.is_visible()
        }

    def send_message(self, text: str, wait_for_input_empty=True):
        """Отправляет сообщение в чат"""

        self.fill(self.message_input, text)
        self.should_have_text(self.message_input, text) # Проверка что текст введен
        self.click(self.send_button)

        if wait_for_input_empty:
            self.should_be_empty(self.message_input) # Поле очистилось после отправки

    def get_last_ai_message(self, timeout=30000) -> str:
        """Возвращает текст последнего сообщения от AI"""
        last_message_block = self.ai_message_blocks.last
        self.wait_for_visible(last_message_block, timeout=timeout)

        # Объединяем текст всех параграфов в блоке
        paragraphs = last_message_block.locator('p')
        self.wait_for_visible(paragraphs.first, timeout=timeout)

        return " ".join([p.text_content() for p in paragraphs.all() if p.text_content().strip()])

    def get_last_user_message(self) -> str:
        """Возвращает текст последнего сообщения пользователя"""
        return self.get_text(self.user_messages.last)

    def regenerate_response(self):
        """Регенерирует последний ответ"""
        self.click(self.regenerate_button)

    def wait_for_ai_response(self, timeout=30000):
        """Ждет ПОЛНОГО ответа AI (со стабилизацией текста)"""
        last_block = self.ai_message_blocks.last
        
        # Ждем появления блока
        self.wait_for_visible(last_block, timeout=timeout)
        
        # Ждем стабилизации текста (3 проверки подряд с интервалом 1 сек)
        stable_text = ""
        stable_count = 0
        start_time = time.time()
        
        while stable_count < 3 and (time.time() - start_time) < timeout:
            current_text = self.get_text(last_block)
            if current_text == stable_text:
                stable_count += 1
            else:
                stable_text = current_text
                stable_count = 0
            time.sleep(1)
        
        if stable_count < 3:
            raise TimeoutError("AI response did not stabilize")

    def configure_chat_settings(self, complexity="Professional", crazy_mode=False):
        """Настраивает параметры чата"""
        self.click(self.chat_settings_button)
        self.wait_for_visible(self.settings_popup)

        # Ждём появления всех лейблов
        self.wait_for_visible(self.professional_label)
        self.wait_for_visible(self.regular_label)
        self.wait_for_visible(self.simple_label)

        # Выбираем уровень сложности языка AI (кликаем на label)
        if complexity == "Professional":
            self.click(self.professional_label)
        elif complexity == "Regular":
            self.click(self.regular_label)
        elif complexity == "Simple":
            self.click(self.simple_label)
        
        # Если Crazy Mode не активирован, то активируем
        current_state = self.crazy_mode_toggle.locator('input').is_checked()
        if crazy_mode != current_state:
            self.click(self.crazy_mode_toggle)
        
        # Закрываем попап (клик вне попапа)
        self.click(self.chat_title)
        self.wait_for_hidden(self.settings_popup)

    def open_chat_settings(self):
        """Открывает настройки чата"""
        self.click(self.chat_settings_button)
        self.wait_for_visible(self.settings_popup)
    
    def close_chat_settings(self):
        """Закрывает настройки чата"""
        self.click(self.chat_title)
        self.wait_for_hidden(self.settings_popup)
    
    def send_message_and_wait_for_response(self, text: str):
        """Отправляет сообщение и ждет ответа"""
        self.send_message(text)
        self.wait_for_ai_response()
