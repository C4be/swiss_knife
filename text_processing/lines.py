import re


class LineJoiner:
    """
    Объединение строк после OCR и случайных переносов.
    """

    ABBREVIATION_RE = re.compile(r"\b[a-zа-я]\.$", re.IGNORECASE)

    # Символы, с которых может начинаться строка-продолжение (кроме маленьких букв)
    # ( скобки, [ квадратные, { фигурные, " ' кавычки, « елочки
    OPENING_PUNCTUATION = {"(", "[", "{", '"', "'", "«"}

    @staticmethod
    def join(text: str) -> str:
        lines = text.split("\n")
        if not lines:
            return ""

        result: list[str] = []
        buffer = lines[0].rstrip()

        for i in range(1, len(lines)):
            next_line_original = lines[i].rstrip()
            next_line_stripped = lines[i].lstrip()

            if not buffer or not next_line_stripped:
                result.append(buffer)
                buffer = next_line_original
                continue

            # --- Логика склейки ---

            # 1. Перенос по дефису (всегда клеим)
            if buffer.endswith("-"):
                buffer = buffer[:-1] + next_line_stripped
                continue

            # Для проверки мягкого переноса нам нужен первый символ следующей строки
            first_char = next_line_stripped[0]

            # 2. Мягкий перенос (пробел)
            # Строка считается продолжением, если:
            # - Она начинается с маленькой буквы
            # - ИЛИ она начинается со скобки/кавычки (исправление твоей ошибки)
            is_continuation = (
                first_char.islower() or first_char in LineJoiner.OPENING_PUNCTUATION
            )

            if (
                not buffer[-1].isdigit()  # Предыдущая не кончается цифрой
                and is_continuation  # Следующая похожа на продолжение
                and not first_char.isdigit()  # Следующая не начинается с цифры (защита от списков)
                and not LineJoiner.ABBREVIATION_RE.search(buffer)  # Не аббревиатура
            ):
                buffer = buffer + " " + next_line_stripped
                continue

            # Иначе: это новая строка
            result.append(buffer)
            buffer = next_line_original

        result.append(buffer)
        return "\n".join(result)
