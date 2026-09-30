import warnings

warnings.filterwarnings("ignore")
import os

import flet as ft
from modules.text_extractor import extract_text_from_pdf
from modules.ai_generator import generate_quiz


def main(page: ft.Page):
    page.title = "AI Тест Генератор"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    page.scroll = ft.ScrollMode.AUTO

    title = ft.Text("Генератор на тестове от снимка/PDF", size=24, weight=ft.FontWeight.BOLD)
    status_text = ft.Text("Статус: Изчаква се файл...", color=ft.Colors.GREEN)

    extracted_text_field = ft.TextField(label="Извлечен текст (OCR)", multiline=True, min_lines=3, max_lines=5,
                                        read_only=True)
    quiz_result_field = ft.TextField(label="Генериран тест (JSON)", multiline=True, min_lines=10, read_only=True)

    file_picker = ft.FilePicker()
    page.overlay.append(file_picker)

    def process_uploaded_file(file_name):
        file_path = os.path.join("assets", file_name)
        try:
            status_text.value = f"Статус: Извличане на текст от {file_name}..."
            status_text.color = ft.Colors.ORANGE
            page.update()

            extracted_text = extract_text_from_pdf(file_path)
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

    def on_file_upload_progress(e: ft.FilePickerUploadEvent):
        status_text.value = f"Статус: Качване на файла... {int(e.progress * 100)}%"
        page.update()

        if e.progress == 1.0:
            process_uploaded_file(e.file_name)

    def on_file_picked(e: ft.FilePickerResultEvent):
        if e.files and len(e.files) > 0:
            status_text.value = "Статус: Подготовка на файла..."
            status_text.color = ft.Colors.ORANGE
            page.update()

            f = e.files[0]
            upload_url = page.get_upload_url(f.name, 60)
            file_picker.upload([ft.FilePickerUploadFile(f.name, upload_url=upload_url)])

    file_picker.on_result = on_file_picked
    file_picker.on_upload = on_file_upload_progress

    process_btn = ft.ElevatedButton(
        text="Избери PDF файл",
        icon=ft.Icons.UPLOAD_FILE,
        on_click=lambda _: file_picker.pick_files(allow_multiple=False, allowed_extensions=["pdf"])
    )

    page.add(title, ft.Divider(), process_btn, status_text, ft.Divider(), extracted_text_field, quiz_result_field)


if __name__ == "__main__":
    assets_dir = os.path.abspath("assets")
    if not os.path.exists(assets_dir):
        os.makedirs(assets_dir)

    # ЗАДАВАМЕ ТАЙНИЯ КЛЮЧ ТУК:
    os.environ["FLET_SECRET_KEY"] = "diploma2026"

    # Стартираме без грешки
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, upload_dir=assets_dir)