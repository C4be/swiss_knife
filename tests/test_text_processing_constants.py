import pytest
from text_processing.constants import (
    PUNCT_BEFORE_RE,
    PUNCT_AFTER_RE,
    DIGIT_LETTER_RE,
    LETTER_DIGIT_RE,
    MULTI_NEWLINE_RE,
    MULTI_SPACES_RE,
    SPACES_RE,
    NON_PRINTABLE_RE,
)


# Проверка PUNCT_BEFORE_RE
@pytest.mark.parametrize(
    "text,expected",
    [
        ("Hello , world", " ,"),
        ("Test .", " ."),
        ("Привет !", " !"),
    ],
)
def test_punct_before(text, expected):
    matches = PUNCT_BEFORE_RE.findall(text)
    assert matches and matches[0] == expected.strip(), f"Не сработало для '{text}'"


# Проверка PUNCT_AFTER_RE
@pytest.mark.parametrize(
    "text,expected",
    [
        ("Hello!  world", "! "),
        ("Test.   ", ". "),
    ],
)
def test_punct_after(text, expected):
    matches = PUNCT_AFTER_RE.findall(text)
    assert matches and matches[0] == expected.strip(), f"Не сработало для '{text}'"


# Проверка DIGIT_LETTER_RE
@pytest.mark.parametrize(
    "text,expected_positions",
    [
        ("123abc", [3]),  # между '3' и 'a'
        ("9X", [1]),  # между '9' и 'X'
    ],
)
def test_digit_letter(text, expected_positions):
    matches = [m.start() for m in DIGIT_LETTER_RE.finditer(text)]
    assert matches == expected_positions, (
        f"Не совпадает позиции DIGIT_LETTER в '{text}'"
    )


# Проверка LETTER_DIGIT_RE
@pytest.mark.parametrize(
    "text,expected_positions",
    [
        ("abc123", [3]),  # между 'c' и '1'
        ("X9", [1]),  # между 'X' и '9'
    ],
)
def test_letter_digit(text, expected_positions):
    matches = [m.start() for m in LETTER_DIGIT_RE.finditer(text)]
    assert matches == expected_positions, (
        f"Не совпадает позиции LETTER_DIGIT в '{text}'"
    )


# Проверка MULTI_NEWLINE_RE
def test_multi_newline():
    text = "Hello\n\n\nWo\n\n\n\n\n\n\n\n\nrld\n\n"
    replaced = MULTI_NEWLINE_RE.sub("\n", text)
    assert replaced == "Hello\nWo\nrld\n"


# Проверка MULTI_SPACES_RE
def test_multi_spaces():
    text = "Hello   world  !"
    replaced = MULTI_SPACES_RE.sub(" ", text)
    assert replaced == "Hello world !"


# Проверка SPACES_RE
def test_spaces():
    text = "Hello\tworld \n test"
    replaced = SPACES_RE.sub(" ", text)
    assert replaced == "Hello world test"


# Проверка NON_PRINTABLE_RE
def test_non_printable():
    text = "Hello\x01World\x7f!"
    replaced = NON_PRINTABLE_RE.sub("", text)
    assert replaced == "HelloWorld!"
