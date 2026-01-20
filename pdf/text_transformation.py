import re

class RawTextHandler:
    # Знаки препинания
    PUNCTUATION_SIGNS = r'[.,:;!?\"\'\)\]\}%]'
    
    # Буквы (латиница + кириллица)
    LETTERS = r'[A-Za-zА-Яа-яЁё]'
    
    # цифра -> буква
    DIGIT_LETTER_PATTERN = f'(?<=\d)(?={LETTERS})'
    
    # буква -> цифра
    LETTER_DIGIT_PATTERN = f'(?<={LETTERS})(?=\d)'
    
    # Римские буквы
    ROMAN_LETTERS = r'[IVXLCDMivxlcdm]'
    
    # Простая проверка на корректность через regex для чисел 1-3999
    ROMAN_REGEXP = r'^(M{0,3})(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$'
    
    # Проверка шаблона буква - цифра - буква для римских чисел
    LETTER_ROMAN_LETTER = f'({LETTERS}+?)({ROMAN_LETTERS}{1,4})({LETTERS}+)'

    def remove_extra_spaces(text: str) -> str:
        """
        Функция:
            1. Убирает пробелы перед знаками препинания в тексте;
            2. Оставляет один пробел после знаков препинания, если их несколько;
        Знаки препинания: . , ; : ! ? " ' ) ] } %
        """
        
        # 1. Лишние пробелы перед знаками препинания
        text = re.sub(f'\s+({RawTextHandler.PUNCTUATION_SIGNS})', r'\1', text)
        
        # 2. Лишние пробелы после знаков препинания
        text = re.sub(f'({RawTextHandler.PUNCTUATION_SIGNS})\s{2,}', r'\1 ', text)
        
        return text
    
    
    def separate_numbers_and_words(text: str) -> str:
        """
        Добавление пробелов между "слипшимися" цифрами и буквами.
        Примеры:
            Что меняем
                1. "abc123" -> "abc 123"
                2. "123abc" -> "123 abc"
                3. "тест456тест" -> "тест 456 тест"
            Что оставляем
                1. "версия1.2.3" -> "версия 1.2.3" (сохраняем точки внутри числел)
        """
        text = re.sub(RawTextHandler.DIGIT_LETTER_PATTERN, ' ', text)
        text = re.sub(RawTextHandler.LETTER_DIGIT_PATTERN, ' ', text)
        return text
    
    
    def separete_roman(text: str) -> str:
        """
        Умное (с проверкой) разделение римских чисел от слов.
        """
        
        def is_valid_roman(s):
            """
            Проверяет, является ли строка валидным римским числом
            """
            s = s.upper().strip()
            
            # Базовые правила римских чисел
            if not s or not re.fullmatch(f'{RawTextHandler.ROMAN_LETTERS}+', s):
                return False
            
            # Проверка порядка и повторений
            # IV, IX, XL, XC, CD, CM - валидные комбинации
            invalid_patterns = [
                'IIII', 'VV', 'XXXX', 'LL', 'CCCC', 'DD', 'MMMM',  # Повторения
                'IL', 'IC', 'ID', 'IM',                            # Неправильные вычитания
                'VX', 'VL', 'VC', 'VD', 'VM',
                'XD', 'XM',
                'LC', 'LD', 'LM',
            ]
            
            for inv in invalid_patterns:
                if inv in s:
                    return False
            
            
            return bool(re.match(RawTextHandler.ROMAN_REGEXP, s))
        
        def process_match(match):
            # Нашли потенциальную римскую цифру в контексте
            before = match.group(1) or ''
            roman_candidate = match.group(2) or ''
            after = match.group(3) or ''
            
            # Проверяем, является ли кандидат валидным римским числом
            if is_valid_roman(roman_candidate):
                return f'{before} {roman_candidate} {after}'
            else:
                # Не римская цифра - оставляем как есть
                return match.group(0)
        
        pattern = RawTextHandler.LETTER_ROMAN_LETTER
        result = text
        # Применяем несколько раз для вложенных случаев
        for _ in range(3):  # Максимум 3 уровня вложенности
            new_result = re.sub(pattern, process_match, result)
            if new_result == result:
                break
            result = new_result
        
        # Очищаем лишние пробелы
        result = re.sub(r'\s+', ' ', result).strip()
        return result 
        