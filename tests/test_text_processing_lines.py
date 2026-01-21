import pytest
from text_processing.lines import LineJoiner


class TestLineJoiner:
    @pytest.fixture
    def joiner(self):
        return LineJoiner()

    @pytest.mark.parametrize(
        "input_text, expected",
        [
            # --- 1. Базовая склейка (английский) ---
            (
                "This is a test\ncase for line\njoining.",
                "This is a test case for line joining.",
            ),
            # --- 2. Базовая склейка (русский) ---
            (
                "Это тестовый\nпример для склейки\nстрок.",
                "Это тестовый пример для склейки строк.",
            ),
            # --- 3. Дефисы (перенос слова) ---
            (
                "This is a test-\ncase for line-\njoining.",
                "This is a testcase for linejoining.",
            ),
            # Случай, когда дефис стоит, но следующая строка пустая (не должно падать/склеивать)
            ("End of line-\n\nNew Paragraph.", "End of line-\n\nNew Paragraph."),
            # --- 4. Границы предложений (Не склеивать) ---
            # Если новая строка начинается с Большой буквы, считаем это новым предложением
            ("First sentence.\nSecond sentence.", "First sentence.\nSecond sentence."),
            (
                "Первое предложение.\nВторое предложение.",
                "Первое предложение.\nВторое предложение.",
            ),
            # --- 5. Абзацы (Пустые строки) ---
            ("Paragraph one.\n\nParagraph two.", "Paragraph one.\n\nParagraph two."),
            # --- 6. Аббревиатуры (Исключения для склейки) ---
            # Логика: если строка заканчивается на "X.", не склеиваем, даже если дальше маленькая буква
            # (Хотя в твоем коде проверка идет только на однобуквенные аббревиатуры типа "г." или "v.")
            (
                "See fig.\nbelow.",
                "See fig. below.",  # "fig." не попадает под ABBREVIATION_RE (там 1 символ), поэтому склеится
            ),
            (
                "Ivanov I.\nv. is important.",
                "Ivanov I.\nv. is important.",  # "I." и "v." попадают под regex, склейки не будет
            ),
            # --- 7. Цифры и списки ---
            # Если строка заканчивается цифрой - не клеим (часто это таблицы или нумерация)
            ("Page 12\n13 is next.", "Page 12\n13 is next."),
            # Если следующая строка начинается с цифры - не клеим (списки)
            ("List of items:\n1. Item one", "List of items:\n1. Item one"),
            # --- 8. Пробелы и форматирование ---
            (
                "  Indented line  \n continues here. ",
                "  Indented line continues here. ",
            ),
            # --- 9. Специфичные кейсы ---
            (
                "Протестировать все современные методы для трансляции естественного языка в язык запросов\n(text 2 sql);",
                "Протестировать все современные методы для трансляции естественного языка в язык запросов (text 2 sql);",
            ),
        ],
    )
    def test_full_logic_coverage(self, joiner, input_text, expected):
        """
        Единый параметризованный тест для проверки всех сценариев join.
        """
        assert joiner.join(input_text) == expected

    def test_multiple_hyphens_edge_case(self, joiner):
        """
        Специфичный кейс: слово само по себе содержит дефис,
        но перенос случился именно на нем.
        OCR часто делает так: 'semi-\nprofessional' -> 'semiprofessional'.
        Это ожидаемое поведение для твоего кода.
        """
        text = "semi-\nprofessional approach"
        # Твой код удалит дефис. Если нужно сохранить (semi-professional),
        # логику класса нужно менять. Сейчас проверяем текущее поведение:
        expected = "semiprofessional approach"
        assert joiner.join(text) == expected

    def test_false_positive_sentence_end(self, joiner):
        """
        Тест на ситуацию: точка есть, но предложение продолжается с маленькой буквы.
        (Обычная ошибка OCR или форматирования).
        """
        text = "It matches end.\nbut continues here."
        expected = "It matches end. but continues here."
        assert joiner.join(text) == expected
