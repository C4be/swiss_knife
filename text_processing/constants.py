import re

# ================================================================#
# Буквы и знаки                                                   #
# ================================================================#

# Знаки препинания
PUNCTUATION_SIGNS: str = r"[.,:;!?\"\'\)\]\}%]"

# Буквы
RUSSIAN_LETTERS: str = r"[А-Яа-яЁё]"
ENGLISH_LETTERS: str = r"[A-Za-z]"
LETTERS: str = rf"(?:{RUSSIAN_LETTERS}|{ENGLISH_LETTERS})"

# ================================================================#
# Предкомпилированные regex                                      #
# ================================================================#

PUNCT_BEFORE_RE = re.compile(rf"\s+({PUNCTUATION_SIGNS})")
PUNCT_AFTER_RE = re.compile(rf"({PUNCTUATION_SIGNS})\s{{2,}}")

DIGIT_LETTER_RE = re.compile(rf"(?<=\d)(?={LETTERS})")
LETTER_DIGIT_RE = re.compile(rf"(?<={LETTERS})(?=\d)")

MULTI_NEWLINE_RE = re.compile(r"\n{2,}")
MULTI_SPACES_RE = re.compile(r" {2,}")
SPACES_RE = re.compile(r"\s+")

# TODO: Добавить проверку на непечатаемые символы
NON_PRINTABLE_RE = re.compile(r"[\x00-\x1F\x7F-\x9F]")
