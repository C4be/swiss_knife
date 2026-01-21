from .constants import PUNCT_BEFORE_RE, PUNCT_AFTER_RE, MULTI_SPACES_RE


class SpacingNormalizer:
    """
    Нормализация пробелов
    """

    @staticmethod
    def remove_extra_spaces(text: str) -> str:
        """
        1. Убирает пробелы перед знаками препинания
        2. Оставляет ровно один пробел после них
        3. Убирает лишние пробелы
        """
        text = PUNCT_BEFORE_RE.sub(r"\1", text)
        text = PUNCT_AFTER_RE.sub(r"\1 ", text)
        text = MULTI_SPACES_RE.sub(" ", text)
        return text.strip()
