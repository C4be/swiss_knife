import re
from spellchecker import SpellChecker
from .constants import RUSSIAN_LETTERS, ENGLISH_LETTERS


class SpellCheckerService:
    """
    Орфографическая коррекция (EN / RU).
    """

    WORD_RE = re.compile(r"\b\w+\b")

    def __init__(self) -> None:
        self._checker_en = SpellChecker(language="en")
        self._checker_ru = SpellChecker(language="ru")

    @staticmethod
    def _detect_language(word: str) -> str:
        if re.search(RUSSIAN_LETTERS, word):
            return "ru"
        if re.search(ENGLISH_LETTERS, word):
            return "en"
        return "unknown"

    def correct(self, text: str) -> str:
        def replacer(match: re.Match) -> str:
            word = match.group(0)
            lang = self._detect_language(word)

            checker = (
                self._checker_ru
                if lang == "ru"
                else self._checker_en
                if lang == "en"
                else None
            )

            if not checker or word.lower() in checker:
                return word

            corrected = checker.correction(word.lower())
            if not corrected:
                return word

            return corrected.capitalize() if word[0].isupper() else corrected

        return self.WORD_RE.sub(replacer, text)
