from .constants import DIGIT_LETTER_RE, LETTER_DIGIT_RE


class NumberWordSeparator:
    """
    Разделение 'слипшихся' цифр и слов.
    """

    @staticmethod
    def separate(text: str) -> str:
        """
        Примеры:
            "abc123" -> "abc 123"
            "123abc" -> "123 abc"
            "тест456тест" -> "тест 456 тест"
        """
        text = DIGIT_LETTER_RE.sub(" ", text)
        text = LETTER_DIGIT_RE.sub(" ", text)
        return text
