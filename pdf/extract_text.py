from PyPDF2 import PdfReader, PageObject
from pathlib import Path
from typing import Union, Dict
import re


def read_page(page: PageObject) -> str:
    return page.extract_text()


def extract_only_text_from_pdf(file_path: Union[str, Path]) -> str:
    """Извлекаем текст из PDF файла целиком (без картинок)

    Args:
        file_path (Union[str, Path]): путь до файла

    Returns:
        str: весь текст в виде одной строки
    """
    reader = PdfReader(file_path)
    text = ""
    for i, page in enumerate(reader.pages):
        raw_text = read_page(page)
        postprocessed_text = remove_spaces_before_punctuation_marks(raw_text)
        postprocessed_text = join_full_sentences(postprocessed_text)
        postprocessed_text = separate_numbers_from_words(postprocessed_text)
        postprocessed_text = normalize_newlines(postprocessed_text)
        text += f"""Page#{i + 1}\n\n{postprocessed_text}\n\n"""
    return text


def extract_only_text_by_pages(file_path: Union[str, Path]) -> Dict[int, str]:
    """Извлекаем текст из PDF постронично (без картинок)

    Args:
        file_path (Union[str, Path]): путь до файла

    Returns:
        str: весь текст постронично
    """
    reader = PdfReader(file_path)
    text_by_pages = dict()
    for i, page in enumerate(reader.pages):
        raw_text = read_page(page)
        postprocessed_text = remove_spaces_before_punctuation_marks(raw_text)
        postprocessed_text = join_full_sentences(postprocessed_text)
        postprocessed_text = separate_numbers_from_words(postprocessed_text)
        text_by_pages[i + 1] = postprocessed_text + "\n"
    return text_by_pages

# ====================================================
# Модуль обработки текста после извлечения из PDF
# ====================================================

def remove_spaces_before_punctuation_marks(text: str) -> str:
    """Удаляет пробелы перед знаками препинания в тексте

    Args:
        text (str): исходный текст

    Returns:
        str: текст без пробелов перед знаками препинания
    """
    return re.sub(r'\s+([.,!?;:])', r'\1', text)


def join_full_sentences(text: str) -> str:
    """
    Улучшенная версия с обработкой большего количества граничных случаев
    """
    lines = text.split('\n')
    result = []
    
    for i, line in enumerate(lines):
        current_line = line.rstrip('\r')
        
        # Пропускаем пустые строки (сохраняем их)
        if not current_line.strip():
            result.append(current_line)
            continue
            
        # Если это не последняя строка
        if i < len(lines) - 1:
            next_line = lines[i + 1].lstrip('\r')
            
            # Если следующая строка не пустая
            if next_line.strip():
                # Проверяем, можем ли объединить
                current_last_char = current_line[-1] if current_line else ''
                next_first_char = next_line[0] if next_line else ''
                
                # Проверяем условия для объединения:
                should_join = (
                    # Текущая строка не заканчивается цифрой
                    not current_last_char.isdigit() and
                    # Следующая строка начинается с маленькой буквы
                    next_first_char.islower() and
                    # Следующая строка не начинается с цифры
                    not next_first_char.isdigit() and
                    # Текущая строка не заканчивается на сокращения типа "т.д."
                    not re.search(r'\b[а-яa-z]\.$', current_line, re.IGNORECASE)
                )
                
                if should_join:
                    # Добавляем следующую строку к текущей
                    result.append(current_line + ' ' + next_line.lstrip())
                    # Пропускаем следующую строку при следующей итерации
                    lines[i + 1] = ''
                    continue
        
        result.append(current_line)
    
    return '\n'.join(result)

def separate_numbers_from_words(text: str) -> str:
    """
    Вставляет пробелы между слипшимися цифрами и словами/символами.
    Сохраняет переносы строк!
    
    Примеры:
    - "abc123" → "abc 123"
    - "123abc" → "123 abc"
    - "тест456тест" → "тест 456 тест"
    - "версия1.2.3" → "версия 1.2.3" (сохраняет точки в числах)
    - "100$" → "100 $" (разделяет цифры и валютные символы)
    - "№123" → "№ 123" (разделяет знак номера и цифры)
    
    Args:
        text (str): исходный текст
        
    Returns:
        str: текст с пробелами между цифрами и словами
    """
    # Паттерны теперь исключают символы новой строки и табуляции
    # [^\d\s.,\n\r\t] - не цифра, не пробел, не точка, не запятая, не новая строка
    pattern1 = r'(?<=\d)(?=[^\d\s.,\n\r\t])'      # цифра → не-цифра
    pattern2 = r'(?<=[^\d\s.,\n\r\t])(?=\d)'      # не-цифра → цифра
    
    # Применяем оба паттерна
    text = re.sub(pattern1, ' ', text)
    text = re.sub(pattern2, ' ', text)
    
    # Дополнительно: разделяем цифры и валютные символы/спецсимволы
    currency_pattern = r'(\d)([$\€\£\¥\₹\₽%\№\#])'
    text = re.sub(currency_pattern, r'\1 \2', text)
    
    # Разделяем спецсимволы и цифры (обратный случай)
    currency_pattern_rev = r'([$\€\£\¥\₹\₽%\№\#])(\d)'
    text = re.sub(currency_pattern_rev, r'\1 \2', text)
    
    # Убираем лишние пробелы (но сохраняем переносы строк)
    # Заменяем 2 и более пробелов на один, но не затрагиваем \n
    lines = text.split('\n')
    processed_lines = []
    
    for line in lines:
        # Обрабатываем пробелы только внутри строк
        line = re.sub(r'[ \t]+', ' ', line)
        processed_lines.append(line)
    
    return '\n'.join(processed_lines)

def post_process_text(text: str) -> str:
    """Постобработка текста после извлечения из PDF

    Args:
        text (str): текст после извлечения

    Returns:
        str: обработанный текст
    """
    pass


def normalize_newlines(text: str) -> str:
    """
    Заменяет несколько подряд идущих символов новой строки на один.
    
    Примеры:
    - "текст\n\n\nтекст" → "текст\nтекст"
    - "первая\nвторая\n\nтретья" → "первая\nвторая\nтретья"
    - "абзац1\n\n\n\nабзац2" → "абзац1\nабзац2"
    
    Args:
        text (str): исходный текст с возможными множественными переносами строк
        
    Returns:
        str: текст с одиночными переносами строк
    """
    # Заменяем 2 и более \n на один \n
    return re.sub(r'\n{2,}', '\n', text)

if __name__ == "__main__":
    test_file = Path(__file__).parent.parent / "materials" / "sample.pdf"
    full_text = extract_only_text_from_pdf(test_file)
    print(full_text)