import re
from .constants import LETTERS


class RomanNumeralSeparator:
    ROMAN_LETTERS = r"[IVXLCDM]"
    ROMAN_REGEXP = re.compile(
        r"^(M{0,3})(CM|CD|D?C{0,3})"
        r"(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$"
    )

    # три захватывающие группы: before, roman, after
    PATTERN = re.compile(rf"({LETTERS}+?)({ROMAN_LETTERS}{{2,}})((?:{LETTERS})+)")

    INVALID_PATTERNS = (
        "IIII",
        "VV",
        "XXXX",
        "LL",
        "CCCC",
        "DD",
        "MMMM",
        "IL",
        "IC",
        "ID",
        "IM",
        "VX",
        "VL",
        "VC",
        "VD",
        "VM",
        "XD",
        "XM",
        "LC",
        "LD",
        "LM",
    )

    @classmethod
    def _is_valid_roman(cls, value: str) -> bool:
        value = value.upper()
        if not cls.ROMAN_REGEXP.match(value):
            return False
        for invalid in cls.INVALID_PATTERNS:
            if invalid in value:
                return False
        return True

    @classmethod
    def separate(cls, text: str) -> str:
        def replacer(match: re.Match) -> str:
            before, roman, after = match.groups()
            after = after or ""  # может быть None

            if not roman.isupper():
                return match.group(0)

            if cls._is_valid_roman(roman):
                return f"{before} {roman} {after}"

            return match.group(0)

        return cls.PATTERN.sub(replacer, text)
