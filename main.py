# Внасяме функциите, които написахме в text_extractor.py
from modules.text_extractor import extract_text_from_image, extract_text_from_pdf

print("Стартиране на теста...\n")

# 1. Задаваме пътя до нашите файлове в папката assets
image_path = "assets/test.jpg"  # Внимавай името да съвпада точно с твоята снимка
pdf_path = "assets/test.pdf"    # Внимавай името да съвпада точно с твоя PDF

# 2. Тестваме четенето от снимка
print("--- РЕЗУЛТАТ ОТ СНИМКАТА ---")
text_from_image = extract_text_from_image(image_path)
print(text_from_image)

# 3. Тестваме четенето от PDF
print("\n--- РЕЗУЛТАТ ОТ PDF ---")
text_from_pdf = extract_text_from_pdf(pdf_path)
print(text_from_pdf)