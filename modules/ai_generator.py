import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Зареждаме тайните променливи от .env файла (твоят API ключ)
load_dotenv()

# Инициализираме клиента с ключа от .env
API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)


def generate_quiz(text: str) -> str:
    """Изпраща извлечения текст към Gemini AI и връща генериран тест в JSON формат."""
    if not text or len(text.strip()) < 10:
        return '{"error": "Текстът е твърде кратък за генериране на тест."}'

    # Инструкцията (Prompt), която казва на AI какво да прави
    prompt = f"""
    Ти си експерт учител. Твоята задача е да генерираш тест (quiz) САМО от предоставения текст.
    Създай 3 въпроса. Всеки въпрос трябва да има 4 възможни отговора, като само един е верен.

    Върни резултата СТРОГО в следния JSON формат, без никакъв друг текст преди или след него:
    [
      {{
        "question": "Текст на въпроса",
        "options": ["Отговор А", "Отговор Б", "Отговор В", "Отговор Г"],
        "correct_answer": "Верен отговор",
        "explanation": "Кратко обяснение защо това е верният отговор"
      }}
    ]

    Текст за анализ:
    {text}
    """

    try:
        # Използваме бързия и безплатен модел gemini-2.5-flash
        response = client.models.generate_content(
            model='gemini-3.8-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.2,  # Правим го 0.2, за да чете само текста и да не си измисля факти
                response_mime_type="application/json",  # Принуждаваме го да върне структуриран JSON
            ),
        )
        return response.text
    except Exception as e:
        return f'{{"error": "Грешка при комуникация с AI: {e}"}}'