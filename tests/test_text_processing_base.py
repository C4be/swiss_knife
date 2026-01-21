import re
import pytest
from spellchecker import SpellChecker

from text_processing.numbers import NumberWordSeparator
from text_processing.spacing import SpacingNormalizer
from text_processing.roman import RomanNumeralSeparator
from text_processing.spelling import SpellCheckerService


WORD_RE = re.compile(r"\b\w+\b")


def test_number_word_separator_base():
    separator = NumberWordSeparator()

    # Тестируем разделение цифр и букв
    assert separator.separate("abc123def") == "abc 123 def"
    assert separator.separate("123abc456") == "123 abc 456"
    assert separator.separate("a1b2c3") == "a 1 b 2 c 3"
    assert separator.separate("тест456тест") == "тест 456 тест"
    assert separator.separate("456тест789") == "456 тест 789"
    assert separator.separate("тест123тест456") == "тест 123 тест 456"
    assert separator.separate("A1B2C3") == "A 1 B 2 C 3"
    assert separator.separate("123ABC456") == "123 ABC 456"
    assert separator.separate("В123АБВ456А") == "В 123 АБВ 456 А"

    # Тестируем строки без цифр или букв
    assert separator.separate("abcdef") == "abcdef"
    assert separator.separate("123456") == "123456"

    # Тестируем пустую строку
    assert separator.separate("") == ""
    assert separator.separate(" ") == " "
    assert separator.separate("  ") == "  "


def test_spacing_normalizer_base():
    normalizer = SpacingNormalizer()

    # Тестируем удаление пробелов перед знаками препинания
    assert normalizer.remove_extra_spaces("Hello , world !") == "Hello, world!"
    assert normalizer.remove_extra_spaces("Hello  , world !") == "Hello, world!"
    assert normalizer.remove_extra_spaces("Hello   , world !") == "Hello, world!"
    assert normalizer.remove_extra_spaces("Hello    , world !") == "Hello, world!"
    assert normalizer.remove_extra_spaces("This is a test .  ") == "This is a test."
    assert normalizer.remove_extra_spaces("This is a test  .  ") == "This is a test."
    assert normalizer.remove_extra_spaces("This is a test    .  ") == "This is a test."
    assert normalizer.remove_extra_spaces("This is a test.  ") == "This is a test."

    # Тестируем сохранение одного пробела после знаков препинания
    assert normalizer.remove_extra_spaces("Hello,  world!") == "Hello, world!"
    assert normalizer.remove_extra_spaces("This is a test.     ") == "This is a test."

    # Тестируем комбинированные случаи
    assert normalizer.remove_extra_spaces("  Hello ,   world !  ") == "Hello, world!"
    assert (
        normalizer.remove_extra_spaces("This  is  a         test . ")
        == "This is a test."
    )


def test_num_word_separation_and_normalizer():
    separator = NumberWordSeparator()
    normalizer = SpacingNormalizer()

    # Комбинированный тест: сначала разделение, затем нормализация
    input_text = "Hello123 ,  world456 !"
    separated_text = separator.separate(input_text)
    normalized_text = normalizer.remove_extra_spaces(separated_text)
    assert normalized_text == "Hello 123, world 456!"

    input_text = "тест456тест ,  пример123 !"
    separated_text = separator.separate(input_text)
    normalized_text = normalizer.remove_extra_spaces(separated_text)
    assert normalized_text == "тест 456 тест, пример 123!"

    input_text = "A1B2C3 ,  D4E5F6 !"
    separated_text = separator.separate(input_text)
    normalized_text = normalizer.remove_extra_spaces(separated_text)
    assert normalized_text == "A 1 B 2 C 3, D 4 E 5 F 6!"


def test_roman_numeral_separator_base():
    separator = RomanNumeralSeparator()

    # Тестируем корректное отделение римских чисел
    assert separator.separate("ChapterIVisHere") == "Chapter IV isHere"
    assert separator.separate("SectionXIIandMore") == "Section XII andMore"
    assert separator.separate("PartMMXIVisDone") == "Part MMXIV isDone"

    # Тестируем строки без римских чисел
    assert separator.separate("HelloWorld") == "HelloWorld"
    assert separator.separate("ThisIsATest") == "ThisIsATest"

    # Тестируем некорректные римские числа
    assert separator.separate("InvalidIIIIHere") == "InvalidIIIIHere"
    assert separator.separate("WrongVVSection") == "WrongVVSection"

    # Тестируем пустую строку
    assert separator.separate("") == ""
    assert separator.separate(" ") == " "
    assert separator.separate("  ") == "  "


def test_spellchecker_replaces_misspelled_words():
    spell_service = SpellCheckerService()

    text = "Ths is a smple tst."
    corrected = spell_service.correct(text)

    # Проверяем, что исходные ошибки больше не встречаются
    assert "Ths" not in corrected
    assert "smple" not in corrected
    assert "tst" not in corrected

    # Проверяем, что корректные слова остались
    assert "is" in corrected
    assert "a" in corrected


def test_spellchecker_handles_ru_and_en():
    spell_service = SpellCheckerService()

    text = "Эттт тест с ошибками и some erors."
    corrected = spell_service.correct(text)

    # Ошибочные слова должны быть исправлены
    assert "Эттт" not in corrected
    assert "erors" not in corrected

    # Правильные слова должны остаться
    assert "тест" in corrected
    assert "some" in corrected


@pytest.mark.parametrize(
    "text,expected_errors",
    [
        ("Ths is a smple tst.", ["Ths", "smple", "tst"]),
        ("Speling erors are comon.", ["Speling", "erors", "comon"]),
        ("Тест с Russian and English wrds", ["wrds"]),
    ],
)
def test_spellchecker_advanced(text, expected_errors):
    spell_service = SpellCheckerService()
    corrected = spell_service.correct(text)

    # 1. Проверяем, что исходные ошибки исправлены
    for word in expected_errors:
        assert word not in corrected, f"Слово '{word}' не исправлено: {corrected}"

    # 2. Проверяем, что слова не потерялись и корректные не изменились
    original_words = WORD_RE.findall(text)
    for word in original_words:
        # Игнорируем ожидаемые ошибки
        if word in expected_errors:
            continue
        # Остальные слова должны остаться в тексте
        assert word in corrected, (
            f"Корректное слово '{word}' было изменено: {corrected}"
        )

    # 3. Проверяем, что исправленные слова действительно валидные
    checker_en = SpellChecker(language="en")
    checker_ru = SpellChecker(language="ru")
    for word in WORD_RE.findall(corrected):
        lang = "ru" if re.search(r"[А-Яа-яЁё]", word) else "en"
        checker = checker_ru if lang == "ru" else checker_en
        assert word.lower() in checker, (
            f"Слово '{word}' после исправления не распознано как корректное"
        )
