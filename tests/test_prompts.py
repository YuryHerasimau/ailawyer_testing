import pytest
from pages.chat_page import ChatPage
from playwright.sync_api import expect


class TestPromptsSelection:
    def test_prompts_popup_opens(self, chat_page):
        """Тест открытия попапа с промптами"""
        chat_page.prompts_button.click()

        # Проверяем, что попап открылся
        expect(chat_page.prompts_popup, "Попап с промптами не открылся").to_be_visible()
        expect(chat_page.prompts_header, "Заголовок попапа с промптами не отображается").to_be_visible()

    def test_close_prompts_popup(self, chat_page):
        chat_page.prompts_button.click()
        
        # Проверяем, что попап открыт
        expect(chat_page.prompts_popup, "Попап с промптами не открыт").to_be_visible()
        
        # Находим и кликаем кнопку закрытия
        chat_page.prompts_close_button.click()
        
        # Проверяем, что попап закрылся
        expect(chat_page.prompts_popup, "Попап с промптами не закрылся").to_be_hidden()

    def test_prompts_categories_visible(self, chat_page):
        """Тест видимости основных категорий промптов"""
        chat_page.prompts_button.click()
        
        # Проверяем, что видны основные категории промптов
        expect(chat_page.prompts_categories_custom_prompts, "Категория 'Custom Prompts' не отображается").to_be_visible()
        expect(chat_page.prompts_categories_prompts_for_legal_consumers, "Категория 'Prompts for Legal Consumers' не отображается").to_be_visible()
        expect(chat_page.prompts_categories_prompts_for_legal_research, "Категория 'Prompts for Legal Research' не отображается").to_be_visible()
        expect(chat_page.prompts_categories_prompts_for_drafting_legal_documents, "Категория 'Prompts for Drafting Legal Documents' не отображается").to_be_visible()
        expect(chat_page.prompts_categories_prompts_for_family_lawyers, "Категория 'Prompts for Family Lawyers' не отображается").to_be_visible()
        expect(chat_page.prompts_categories_prompts_for_personal_injury_lawyers, "Категория 'Prompts for Personal Injury Lawyers' не отображается").to_be_visible()
        expect(chat_page.prompts_categories_prompts_for_employment_and_labor_lawyers, "Категория 'Prompts for Employment and Labor Lawyers' не отображается").to_be_visible()
        expect(chat_page.prompts_categories_prompts_for_immigration_lawyers, "Категория 'Prompts for Immigration Lawyers' не отображается").to_be_visible()
        expect(chat_page.prompts_categories_prompts_for_business_lawyers, "Категория 'Prompts for Business Lawyers' не отображается").to_be_visible()
        expect(chat_page.prompts_categories_prompts_for_tax_lawyers, "Категория 'Prompts for Tax Lawyers' не отображается").to_be_visible()
        expect(chat_page.prompts_categories_prompts_for_real_estate_lawyers, "Категория 'Prompts for Real Estate Lawyers' не отображается").to_be_visible()
        expect(chat_page.prompts_categories_prompts_for_intellectual_property_ip_lawyers, "Категория 'Prompts for Intellectual Property (IP) Lawyers' не отображается").to_be_visible()
        expect(chat_page.prompts_categories_prompts_for_criminal_defense_lawyers, "Категория 'Prompts for Criminal Defense Lawyers' не отображается").to_be_visible()

    def test_expand_collapse_prompt_category(self, chat_page):
        """Тест сворачивания и разворачивания категории промптов Custom prompts"""
        chat_page.prompts_button.click()
        
        # Находим кнопку категории и проверяем, что она свернута
        category_button = chat_page.page.locator('button:has-text("Custom prompts")')
        expect(category_button).to_be_visible()
        
        # Локатор контейнера с промптами (используем более надежный селектор)
        prompts_container = category_button.locator('xpath=./following-sibling::div[contains(@class, "bg-openFolder")][1]')

        # Проверяем, что контейнер изначально скрыт
        expect(prompts_container).to_be_hidden()
        
        # Кликаем, чтобы развернуть
        category_button.click()
        chat_page.page.wait_for_timeout(300)

        # Проверяем, что контейнер стал видимым и содержит ожидаемый промпт
        expect(prompts_container).to_be_visible()
        expect(prompts_container.locator('text=Используя техники граничных условий')).to_be_visible()
        
        # Кликаем снова, чтобы свернуть
        category_button.click()
        chat_page.page.wait_for_timeout(300)
        
        # Проверяем, что контейнер снова скрыт
        expect(prompts_container).to_be_hidden()

    def test_select_prompt(self, chat_page):
        """Тест выбора конкретного промпта"""
        chat_page.prompts_button.click()
        
        # Разворачиваем категорию
        chat_page.page.locator('button:has-text("Custom prompts")').click()
        
        # Выбираем конкретный промпт
        prompt_text = "Используя техники граничных условий и классов эквивалентности напиши тест-кейсы для тестирования"
        
        # Точный локатор для элемента промпта
        prompt_item = chat_page.page.locator(
            f'div.bg-openFolder div.flex:has-text("{prompt_text}")'
        ).first  # Берем первый подходящий элемент
        
        # Альтернативный вариант, если предыдущий не работает:
        # prompt_item = chat_page.page.locator(
        #     f'xpath=//div[contains(@class, "bg-openFolder")]//div[contains(@class, "flex")][contains(., "{prompt_text}")]'
        # )
        
        expect(prompt_item).to_be_visible()
        
        # Находим кнопку меню (3 точки) внутри этого элемента
        menu_button = prompt_item.locator('button:has(> svg)').first
        expect(menu_button).to_be_visible()
        menu_button.click()
        
        # Кликаем на "Add to input field" в появившемся меню
        add_button = chat_page.page.locator(
            'button:has-text("Add to input field")'
        )
        expect(add_button).to_be_visible()
        add_button.click()
        
        # Проверяем, что текст промпта появился в поле ввода
        expect(chat_page.message_input).to_have_value(prompt_text)

    def test_create_new_prompt(self, chat_page):
        """Тест создания нового промпта"""
        chat_page.prompts_button.click()
        
        # Проверяем кнопку создания нового промпта
        new_prompt_button = chat_page.page.get_by_text("Create new prompt", exact=True)
        expect(new_prompt_button).to_be_visible()
        
        # Кликаем на кнопку
        new_prompt_button.click()
        
        # Проверяем основные элементы формы без проверки всего контейнера
        # Проверяем заголовок
        expect(chat_page.page.get_by_text("Create your own quick access prompt")).to_be_visible()
        
        # Проверяем поле ввода
        prompt_input = chat_page.page.get_by_placeholder("Your prompt")
        expect(prompt_input).to_be_visible()
        expect(prompt_input).to_have_value("")
        
        # Проверяем кнопки
        cancel_button = chat_page.page.get_by_text("Cancel", exact=True)
        save_button = chat_page.page.get_by_text("Save", exact=True)
        expect(cancel_button).to_be_visible()
        expect(save_button).to_be_visible()
        
        # Тест ввода текста
        test_prompt = "Новый тестовый промпт"
        prompt_input.fill(test_prompt)
        expect(prompt_input).to_have_value(test_prompt)
        
        # Закрываем модальное окно (опционально)
        cancel_button.click()
        expect(chat_page.page.get_by_text("Create your own quick access prompt")).not_to_be_visible()

    @pytest.mark.parametrize("action, test_prompt", [
        ("save", "Test prompt for save"),
        ("cancel", "Test prompt for cancel"),
    ])
    def test_create_custom_prompt(self, chat_page, action, test_prompt):
        """Тест создания нового промпта с параметризацией"""
        # 1. Открываем форму создания промпта
        chat_page.prompts_button.click(force=True)  # Добавляем force для обхода overlays
        new_prompt_button = chat_page.page.get_by_text("Create new prompt", exact=True)
        expect(new_prompt_button).to_be_visible()
        new_prompt_button.click()

        # 2. Проверяем элементы формы
        form_title = chat_page.page.get_by_text("Create your own quick access prompt")
        expect(form_title).to_be_visible()
        
        prompt_input = chat_page.page.get_by_placeholder("Your prompt")
        expect(prompt_input).to_be_visible()
        expect(prompt_input).to_have_value("")

        # 3. Заполняем поле ввода
        prompt_input.fill(test_prompt)
        expect(prompt_input).to_have_value(test_prompt)

        if action == "cancel":
            # 4a. Сценарий отмены
            cancel_button = chat_page.page.get_by_text("Cancel", exact=True)
            expect(cancel_button).to_be_visible()
            cancel_button.click()

            # 5a. Проверяем, что форма скрылась
            expect(form_title).not_to_be_visible()
            
            # 6a. Снова открываем аккордеон для проверки. Проверяем, что промпт не добавился
            # custom_prompts_button = chat_page.page.locator('button:has-text("Custom prompts")')
            chat_page.page.locator('button:has-text("Custom prompts")').click(force=True)
            expect(chat_page.page.get_by_text(test_prompt)).not_to_be_visible()

        elif action == "save":
            # 4b. Сценарий сохранения
            save_button = chat_page.page.get_by_text("Save", exact=True)
            expect(save_button).to_be_visible()
            save_button.click()

            # 5b. Ждем схлопывания аккордеона
            expect(form_title).not_to_be_visible(timeout=10000)

            # 6b. Снова открываем аккордеон для проверки
            # custom_prompts_button = chat_page.page.locator('button:has-text("Custom prompts")')
            chat_page.page.locator('button:has-text("Custom prompts")').click(force=True)
            
            # 7b. Проверяем, что промпт добавился в список (берем первый если несколько)
            prompt_locator = chat_page.page.get_by_text(test_prompt).first
            expect(prompt_locator).to_be_visible(timeout=10000)
            
            # 8b. Очистка
            try:
                # Ищем все matching промпты
                prompts = chat_page.page.locator(
                    f'div.bg-openFolder div.flex:has-text("{test_prompt}")'
                ).all()

                for prompt_item in prompts:
                    expect(prompt_item).to_be_visible()
                    prompt_item.scroll_into_view_if_needed()
                    prompt_item.hover()

                    menu_button = prompt_item.locator('button:has(> svg)').first
                    expect(menu_button).to_be_visible()
                    menu_button.click()

                    # Кликаем Delete prompt
                    delete_button = chat_page.page.locator('button:has-text("Delete prompt")').first
                    expect(delete_button).to_be_visible()
                    delete_button.click()

                    # Подтверждаем удаление в модальном окне
                    confirm_modal = chat_page.page.locator('text=Delete prompt?')
                    confirm_modal.wait_for(state='visible')
                    confirm_delete = chat_page.page.get_by_text("Delete", exact=True).first
                    confirm_delete.click(force=True)

                    # Ждем исчезновения промпта
                    chat_page.page.wait_for_timeout(500)  # Пауза для завершения анимации

                    # Проверяем, что промпт исчез из списка
                    expect(prompt_locator).not_to_be_visible()

            except Exception as e:
                print(f"Ошибка при удалении промпта: {e}")
                pass

    @pytest.mark.skip
    def test_all_prompts_selectable(self, chat_page):
        chat_page.prompts_button.click()
        
        # Список категорий для проверки
        categories = [
            "Custom prompts",
            "Prompts for Legal Consumers",
            "Prompts for Legal Research",
            "Prompts for Drafting Legal Documents",
            "Prompts for Family Lawyers",
            "Prompts for Personal Injury Lawyers",
            "Prompts for Employment and Labor Lawyers",
            "Prompts for Immigration Lawyers",
            "Prompts for Business Lawyers",
            "Prompts for Tax Lawyers",
            "Prompts for Real Estate Lawyers",
            "Prompts for Intellectual Property (IP) Lawyers",
            "Prompts for Criminal Defense Lawyers",
        ]
        
        for category in categories:
            # Разворачиваем категорию
            category_button = chat_page.page.locator(f'button:has-text("{category}")')
            category_button.click()
            
            # Находим все промпты в категории
            prompts = chat_page.page.locator(f'button:has-text("{category}") + div.bg-openFolder button:has(p)')
            count = prompts.count()
            
            for i in range(count):
                prompt = prompts.nth(i)
                prompt_text = prompt.locator('p').inner_text()
                
                # Кликаем на промпт
                prompt.click()
                
                # Проверяем, что текст появился в поле ввода
                expect(chat_page.message_input).to_have_value(prompt_text)
                
                # Очищаем поле ввода для следующего теста
                chat_page.message_input.fill("")
                
                # Возвращаемся в попап промптов
                chat_page.prompts_button.click()
                category_button.click()