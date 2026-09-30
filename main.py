import warnings

warnings.filterwarnings("ignore")

import flet as ft
from modules.text_extractor import extract_text_from_pdf
from modules.ai_generator import generate_quiz


def main(page: ft.Page):
    page.title = "AI Тест Генератор"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    page.scroll = ft.ScrollMode.AUTO

    title = ft.Text("Генератор на тестове от снимка/PDF", size=24, weight=ft.FontWeight.BOLD)
    status_text = ft.Text("Статус: Готов за работа.", color=ft.Colors.GREEN)

    extracted_text_field = ft.TextField(label="Извлечен текст (OCR)", multiline=True, min_lines=3, max_lines=5,
                                        read_only=True)
    quiz_result_field = ft.TextField(label="Генериран тест (JSON)", multiline=True, min_lines=10, read_only=True)

    def process_test_files(e):
        status_text.value = "Статус: Извличане на текст..."
        status_text.color = ft.Colors.ORANGE
        page.update()

        pdf_path = "assets/test.pdf"

        try:
            extracted_text = extract_text_from_pdf(pdf_path)
            extracted_text_field.value = extracted_text

            status_text.value = "Статус: Генериране на тест от AI..."
            page.update()

            quiz_json = generate_quiz(extracted_text)
            quiz_result_field.value = quiz_json

            status_text.value = "Статус: Готово!"
            status_text.color = ft.Colors.GREEN
        except Exception as ex:
            status_text.value = f"Грешка: {ex}"
            status_text.color = ft.Colors.RED

        page.update()

    process_btn = ft.ElevatedButton(text="Генерирай тест (От test.pdf)", icon=ft.Icons.SMART_TOY,
                                    on_click=process_test_files)

    page.add(title, ft.Divider(), process_btn, status_text, ft.Divider(), extracted_text_field, quiz_result_field)


if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.WEB_BROWSER)