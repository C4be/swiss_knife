from .spacing import SpacingNormalizer
from .numbers import NumberWordSeparator
from .roman import RomanNumeralSeparator
from .lines import LineJoiner
from .spelling import SpellCheckerService
from .constants import MULTI_NEWLINE_RE


class RawTextNormalizer:
    """
    Основной пайплайн нормализации текста.
    """

    def __init__(self, enable_spellcheck: bool = False) -> None:
        self._spellchecker = SpellCheckerService() if enable_spellcheck else None

    def normalize(self, text: str) -> str:
        text = MULTI_NEWLINE_RE.sub("\n", text)
        text = LineJoiner.join(text)
        text = SpacingNormalizer.remove_extra_spaces(text)
        text = NumberWordSeparator.separate(text)
        text = RomanNumeralSeparator.separate(text)

        if self._spellchecker:
            text = self._spellchecker.correct(text)

        return text
