import time
from playwright.sync_api import Page, expect


class ChatPage:
    def __init__(self, page: Page):
        self.page = page

        # Локаторы для приветственного сообщения
        self.greeting_block = page.locator('div.bg-aiMessage').first
        self.greeting_header = self.greeting_block.locator('h2')
        self.greeting_paragraphs = self.greeting_block.locator('p')
        self.add_button = self.greeting_block.locator('button:has-text("Add")')

        # Локаторы для поля ввода
        self.message_input = page.get_by_placeholder("Type your message here")
        self.send_button = self.message_input.locator('xpath=./following-sibling::button[1]')
        self.chat_title = page.locator('h1.text-xl')

        # Локаторы для сообщений
        self.ai_message_blocks = page.locator('div.bg-aiMessage:has(p)') # Блоки сообщений AI
        self.user_messages = page.locator('div.myMessage p')

        # Локаторы для дополнительных элементов
        self.internet_button = page.locator('//div[contains(@class, "bg-aiMessage")]//span[contains(text(), "Internet")]')
        self.prompts_button = page.locator('//div[contains(@class, "group") and contains(text(), "Prompts")]')
        self.regenerate_button = page.locator('xpath=//button[.//p[contains(text(), "Regenerate Response")]]')

        # Локаторы для попапа с промптами
        self.prompts_popup = page.locator('text=Prompts Base')
        self.prompts_header = page.locator('text=Choose the prompt that suits you best')
        self.prompts_close_button = page.locator('div[class*="bg-white"] header button')
        self.prompts_categories_custom_prompts = page.locator('text=Custom prompts')
        self.prompts_categories_prompts_for_legal_consumers  = page.locator('text=Prompts for Legal Consumers')
        self.prompts_categories_prompts_for_legal_research = page.locator('text=Prompts for Legal Research')
        self.prompts_categories_prompts_for_drafting_legal_documents = page.locator('text=Prompts for Drafting Legal Documents')
        self.prompts_categories_prompts_for_family_lawyers = page.locator('text=Prompts for Family Lawyers')
        self.prompts_categories_prompts_for_personal_injury_lawyers = page.locator('text=Prompts for Personal Injury Lawyers')
        self.prompts_categories_prompts_for_employment_and_labor_lawyers = page.locator('text=Prompts for Employment and Labor Lawyers')
        self.prompts_categories_prompts_for_immigration_lawyers = page.locator('text=Prompts for Immigration Lawyers')
        self.prompts_categories_prompts_for_business_lawyers = page.locator('text=Prompts for Business Lawyers')
        self.prompts_categories_prompts_for_tax_lawyers = page.locator('text=Prompts for Tax Lawyers')
        self.prompts_categories_prompts_for_real_estate_lawyers = page.locator('text=Prompts for Real Estate Lawyers')
        self.prompts_categories_prompts_for_intellectual_property_ip_lawyers = page.locator('text=Prompts for Intellectual Property (IP) Lawyers')
        self.prompts_categories_prompts_for_criminal_defense_lawyers = page.locator('text=Prompts for Criminal Defense Lawyers')

        # Локаторы для закрепления чата
        self.pin_button = page.locator('button:has(.icon[style*="pin-dark.svg"])')

        # Локаторы для настройки чата
        self.chat_settings_button = page.locator('button:has(svg path[d*="M9.594 3.94c"])')
        self.settings_popup = page.locator('div[class*="bg-white shadow-shadow"]:has(header h3)')
        self.complexity_header = self.settings_popup.locator('header h3:has-text("Language complexity")')

        # Локаторы для радиокнопок
        self.professional_label = self.settings_popup.locator('label:has-text("Professional")')
        self.regular_label = self.settings_popup.locator('label:has-text("Regular")')
        self.simple_label = self.settings_popup.locator('label:has-text("Simple")')
        self.professional_radio = self.settings_popup.locator('input[name="Professional"]')
        self.regular_radio = self.settings_popup.locator('input[name="Regular"]')
        self.simple_radio = self.settings_popup.locator('input[name="Simple"]')

        # Локатор для Crazy Mode (кликаем на весь переключатель)
        self.crazy_mode_toggle = self.settings_popup.locator('div:has-text("Crazy Mode") >> label')
    
    def get_greeting_text(self) -> dict:
        """Возвращает все части приветственного сообщения в виде словаря"""
        return {
            'header': self.greeting_header.text_content(),
            'first_paragraph': self.greeting_paragraphs.nth(0).text_content(),
            'second_paragraph': self.greeting_paragraphs.nth(1).text_content(),
            'add_button_visible': self.add_button.is_visible()
        }

    def send_message(self, text: str, wait_for_input_empty=True):
        """Отправляет сообщение в чат"""
        self.message_input.fill(text)
        expect(self.message_input).to_have_value(text)  # Проверка что текст введен
        self.send_button.click()

        if wait_for_input_empty:
            expect(self.message_input).to_be_empty() # Поле очистилось после отправки

    def get_last_ai_message(self, timeout=30000) -> str:
        """Возвращает текст последнего сообщения от AI"""
        last_message_block = self.ai_message_blocks.last
        expect(last_message_block).to_be_visible(timeout=timeout)

        # Объединяем текст всех параграфов в блоке
        paragraphs = last_message_block.locator('p')
        expect(paragraphs.first).to_be_visible(timeout=timeout)

        return " ".join([p.text_content() for p in paragraphs.all() if p.text_content().strip()])

    def get_last_user_message(self) -> str:
        """Возвращает текст последнего сообщения пользователя"""
        return self.user_messages.last.text_content()

    def select_prompt(self, index: int):
        """Выбирает prompt по индексу"""
        self.prompts_button.nth(index).click()

    def regenerate_response(self):
        """Регенерирует последний ответ"""
        self.regenerate_button.click()

    def wait_for_ai_response(self, timeout=30000):
        """Ждет ПОЛНОГО ответа AI (со стабилизацией текста)"""
        last_block = self.ai_message_blocks.last
        
        # Ждем появления блока
        expect(last_block).to_be_visible(timeout=timeout)
        
        # Ждем стабилизации текста (3 проверки подряд с интервалом 1 сек)
        stable_text = ""
        stable_count = 0
        start_time = time.time()
        
        while stable_count < 3 and (time.time() - start_time) < timeout:
            current_text = last_block.text_content()
            if current_text == stable_text:
                stable_count += 1
            else:
                stable_text = current_text
                stable_count = 0
            time.sleep(1)
        
        if stable_count < 3:
            raise TimeoutError("AI response did not stabilize")

    def make_screenshot(self, name="screenshot"):
        """Делает скриншот с timestamp"""
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.page.screenshot(path=f"screenshots/{name}_{timestamp}.png")

    def configure_chat_settings(self, complexity="Professional", crazy_mode=False):
        """Настраивает параметры чата"""
        self.chat_settings_button.click()
        expect(self.settings_popup).to_be_visible()

        # Ждём появления всех лейблов
        expect(self.professional_label).to_be_visible()
        expect(self.regular_label).to_be_visible()
        expect(self.simple_label).to_be_visible()

        # Выбираем уровень сложности языка AI (кликаем на label)
        if complexity == "Professional":
            self.professional_label.click()
        elif complexity == "Regular":
            self.regular_label.click()
        elif complexity == "Simple":
            self.simple_label.click()
        
        # Если Crazy Mode не активирован, то активируем
        current_state = self.crazy_mode_toggle.locator('input').is_checked()
        if crazy_mode != current_state:
            self.crazy_mode_toggle.click()
        
        # Закрываем попап (клик вне попапа)
        self.chat_title.click()
        expect(self.settings_popup).not_to_be_visible()