import pytesseract
from PIL import Image
from pypdf import PdfReader

def extract_text_from_image(image_path: str) -> str:
    """Извлича текст от изображение (JPG/PNG)"""
    try:
        # Отваряме снимката
        img = Image.open(image_path)
        # Извличаме текста, като казваме на Tesseract да търси Български (bul) и Английски (eng)
        text = pytesseract.image_to_string(img, lang='bul+eng')
        return text.strip()
    except Exception as e:
        return f"Грешка при четене на снимката: {e}"

def extract_text_from_pdf(pdf_path: str) -> str:
    """Извлича текст от PDF документ"""
    text = ""
    try:
        reader = PdfReader(pdf_path)
        # Минаваме през всяка страница и вадим текста
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text.strip()
    except Exception as e:
         return f"Грешка при четене на PDF файла: {e}"

# --- ТЕСТВАНЕ ---
# Ако пуснем този файл директно, ще се изпълни кодът по-долу
if __name__ == "__main__":
    print("Модулът за четене на текст е зареден успешно!")
    # Тук по-късно може да сложим пътека до реална снимка за тест:
    # print(extract_text_from_image("път/до/твоята/снимка.jpg"))