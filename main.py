import warnings
warnings.filterwarnings("ignore")

from PIL.PdfParser import pdf_repr

from modules.text_extractor import extract_text_from_pdf
from modules.ai_generator import generate_quiz

print("1. Извличане на текст от PDF...")
pdf_path = "assets/test.pdf"
extracted_text = extract_text_from_pdf(pdf_path)

print("2. Текстът е извлечен. Изпращане към AI за генериране на тест...\n")

# Викаме AI функцията и ѝ подаваме прочетения текст
quiz_json = generate_quiz(extracted_text)

print("--- ГЕНЕРИРАН ТЕСТ ---")
print(quiz_json)