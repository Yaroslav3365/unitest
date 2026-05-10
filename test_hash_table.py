import unittest

from hash_table import HashTable, UKRAINIAN_ALPHABET


class TestHashTable(unittest.TestCase):
    # ------------------------------------------------------------------
    # Тести хеш-функції
    # ------------------------------------------------------------------

    def test_single_letter_returns_alphabet_index(self):
        # Перевірте базову домовленість: А=1, Я=33. Якщо ця відповідність
        # зламається, всі інші тести стануть ненадійними.
        #
        # Приклади:
        #   hash_function("А") -> 1
        #   hash_function("Б") -> 2
        #   hash_function("Я") -> 33
        hash_table = HashTable()
        self.assertEqual(hash_table.hash_function("А"), 1)
        self.assertEqual(hash_table.hash_function("Б"), 2)
        self.assertEqual(
            hash_table.hash_function("Я"), len(UKRAINIAN_ALPHABET)
        )

    def test_word_sums_letter_values(self):
        # Хеш слова має дорівнювати сумі хешів літер. Візьміть конкретний
        # приклад "КІТ" (К=15, І=12, Т=23) і звірте очікуваний результат.
        #
        # Приклад:
        #   hash_function("КІТ") -> 50  (бо 15 + 12 + 23 = 50)
        hash_table = HashTable()
        self.assertEqual(hash_table.hash_function("КІТ"), 15 + 12 + 23)

    def test_lowercase_is_uppercased(self):
        # Хеш-функція має бути case-insensitive: "кіт" і "КІТ" — це
        # логічно той самий ключ. Якщо це не так, користувач не зможе
        # знайти значення, яке щойно вставив у іншому регістрі.
        #
        # Приклад:
        #   hash_function("кіт") == hash_function("КІТ")  -> True
        hash_table = HashTable()
        self.assertEqual(
            hash_table.hash_function("кіт"),
            hash_table.hash_function("КІТ"),
        )

    def test_mixed_case(self):
        # Перевірте, що змішаний регістр (типова помилка вводу) теж
        # коректно нормалізується.
        #
        # Приклад:
        #   hash_function("Кіт") == hash_function("КІТ")  -> True
        hash_table = HashTable()
        self.assertEqual(
            hash_table.hash_function("Кіт"),
            hash_table.hash_function("КІТ"),
        )

    def test_empty_string_returns_zero(self):
        # Граничний випадок: порожній рядок. Сума порожньої послідовності
        # дорівнює 0 — функція не повинна падати на такому вході.
        #
        # Приклад:
        #   hash_function("") -> 0
        hash_table = HashTable()
        self.assertEqual(hash_table.hash_function(""), 0)
    def test_unsupported_character_raises(self):
        # Латинські літери не належать до української абетки — функція
        # має явно повідомити про помилку, а не "тихо" повернути щось.
        #
        # Приклад:
        #   hash_function("HELLO") -> ValueError
        hash_table = HashTable()

        with self.assertRaises(ValueError):
            hash_table.hash_function("HELLO")

    def test_unsupported_character_message_contains_char(self):
        # Повідомлення про помилку повинно містити сам символ-порушник,
        # щоб користувач одразу бачив, що саме не так із вхідними даними.
        #
        # Приклад:
        #   hash_function("А1") -> ValueError, текст помилки містить "1"
        hash_table = HashTable()

        with self.assertRaises(ValueError) as context:
            hash_table.hash_function("А1")

        self.assertIn("1", str(context.exception))

    def test_space_is_unsupported(self):
        # Пробіл — це не літера абетки. Тест має зафіксувати поточну
        # поведінку: ключі з пробілами не дозволені.
        #
        # Приклад:
        #   hash_function("А Б") -> ValueError
        hash_table = HashTable()

        with self.assertRaises(ValueError):
            hash_table.hash_function("А Б")

    # ------------------------------------------------------------------
    # Тести конструктора
    # ------------------------------------------------------------------

    def test_default_size(self):
        # За замовчуванням таблиця має 33 кошики (за кількістю літер).
        # Перевірте і атрибут size, і реальну довжину масиву.
        #
        # Приклад:
        #   HashTable().size            -> 33
        #   len(HashTable().table)      -> 33
        hash_table = HashTable()

        self.assertEqual(hash_table.size, 33)
        self.assertEqual(len(hash_table.table), 33)


def test_custom_size(self):
        # Користувач має змогу задати свій розмір. Це важливо, бо
        # інакше неможливо було б симулювати колізії в тестах.
        #
        # Приклад:
        #   HashTable(size=10).size           -> 10
        #   len(HashTable(size=10).table)     -> 10
        hash_table = HashTable(size=10)

        self.assertEqual(hash_table.size, 10)
        self.assertEqual(len(hash_table.table), 10)

    def test_buckets_are_empty_lists(self):
        # Усі кошики на старті мають бути порожніми списками — інакше
        # перший же insert/get матиме непередбачувану поведінку.
        #
        # Приклад:
        #   HashTable(size=5).table -> [[], [], [], [], []]
        hash_table = HashTable(size=5)

        self.assertEqual(hash_table.table, [[], [], [], [], []])

    def test_buckets_are_independent(self):
        # Класична пастка: якщо створити кошики через [[]] * size, усі
        # вони будуть посиланнями на один список. Цей тест має гарантувати,
        # що реалізація використовує list comprehension і кошики незалежні.
        #
        # Приклад:
        #   t = HashTable(size=3)
        #   t.table[0].append("щось")
        #   t.table[1] -> []   (другий кошик НЕ змінився)
        #   t.table[2] -> []   (третій кошик НЕ змінився)
        hash_table = HashTable(size=3)

        hash_table.table[0].append("щось")

        self.assertEqual(hash_table.table[1], [])
        self.assertEqual(hash_table.table[2], [])

    def test_letter_to_number_mapping(self):
        # Перевірте внутрішній словник: він має покривати всю абетку
        # і починатися з 1 (а не з 0), бо 0 використовується як хеш
        # порожнього рядка.
        #
        # Приклад:
        #   t.letter_to_number["А"]    -> 1
        #   t.letter_to_number["Я"]    -> 33
        #   len(t.letter_to_number)    -> 33
        hash_table = HashTable()

        self.assertEqual(hash_table.letter_to_number["А"], 1)
        self.assertEqual(
            hash_table.letter_to_number["Я"],
            len(UKRAINIAN_ALPHABET),
        )
        self.assertEqual(
            len(hash_table.letter_to_number),
            len(UKRAINIAN_ALPHABET),
        )

    # ------------------------------------------------------------------
    # Тести insert
    # ------------------------------------------------------------------

    def test_insert_stores_value(self):
        # Найпростіший сценарій: вставили — отримали назад те саме.
        #
        # Приклад:
        #   t.insert("КІТ", "cat")
        #   t.get("КІТ")   -> "cat"
        t = HashTable()

        t.insert("КІТ", "cat")

        self.assertEqual(t.get("КІТ"), "cat")

    def test_insert_multiple_keys(self):
        # Кілька різних ключів мають співіснувати, не перезаписуючи
        # один одного.
        #
        # Приклад:
        #   t.insert("КІТ", "cat")
        #   t.insert("ПЕС", "dog")
        #   t.get("КІТ") -> "cat"
        #   t.get("ПЕС") -> "dog"
        t = HashTable()

        t.insert("КІТ", "cat")
        t.insert("ПЕС", "dog")

        self.assertEqual(t.get("КІТ"), "cat")
        self.assertEqual(t.get("ПЕС"), "dog")

    def test_insert_updates_existing_key(self):
        # Повторна вставка з тим самим ключем — це оновлення, а не
        # дублювання. Це поведінка, до якої звикли користувачі словника.
        #
        # Приклад:
        #   t.insert("КІТ", "cat")
        #   t.insert("КІТ", "kitten")
        #   t.get("КІТ") -> "kitten"
        t = HashTable()

        t.insert("КІТ", "cat")
        t.insert("КІТ", "kitten")

        self.assertEqual(t.get("КІТ"), "kitten")

    def test_insert_update_does_not_grow_bucket(self):
        # Доповнення до попереднього тесту: оновлення не повинно
        # додавати новий елемент у кошик. Інакше через час таблиця
        # розпухне дублікатами і всі операції стануть повільнішими.
        #
        # Приклад:
        #   t.insert("КІТ", "cat")
        #   t.insert("КІТ", "kitten")
        #   len(t.table[index_of_КІТ]) -> 1   (а не 2)
        t = HashTable()

        t.insert("КІТ", "cat")
        index = t.hash_function("КІТ") % t.size

        t.insert("КІТ", "kitten")

        self.assertEqual(len(t.table[index]), 1)

    def test_insert_handles_collision(self):
        # Створіть штучну колізію: таблиця з одним кошиком — усі ключі
        # потраплять туди. Перевірте, що ланцюжковий метод працює і
        # обидва значення доступні.
        #
        # Приклад:
        #   t = HashTable(size=1)
        #   t.insert("КІТ", "cat")
        #   t.insert("ПЕС", "dog")
        #   t.get("КІТ")    -> "cat"
        #   t.get("ПЕС")    -> "dog"
        #   len(t.table[0]) -> 2
        t = HashTable(size=1)

        t.insert("КІТ", "cat")
        t.insert("ПЕС", "dog")

        self.assertEqual(t.get("КІТ"), "cat")
        self.assertEqual(t.get("ПЕС"), "dog")
        self.assertEqual(len(t.table[0]), 2)

    def test_insert_unsupported_character_raises(self):
        # insert повинен прокидати ValueError від hash_function — щоб
        # таблиця не приймала ключі, які потім неможливо буде знайти.
        #
        # Приклад:
        #   t.insert("CAT", "feline") -> ValueError
        t = HashTable()

        with self.assertRaises(ValueError):
            t.insert("CAT", "feline")

    # ------------------------------------------------------------------
    # Тести get
    # ------------------------------------------------------------------

    def test_get_existing_key(self):
        # Базовий happy path для get.
        #
        # Приклад:
        #   t.insert("КІТ", "cat")
        #   t.get("КІТ") -> "cat"
        t = HashTable()

        t.insert("КІТ", "cat")

        self.assertEqual(t.get("КІТ"), "cat")

    def test_get_missing_key_raises(self):
        # Запит ключа в порожній таблиці. KeyError — стандартний спосіб
        # повідомити, що ключа нема (як у вбудованому dict).
        #
        # Приклад:
        #   t.get("КІТ") -> KeyError
        t = HashTable()

        with self.assertRaises(KeyError):
            t.get("КІТ")

    def test_get_missing_key_in_non_empty_bucket_raises(self):
        # Окремо протестуйте випадок, коли кошик не порожній, але
        # потрібного ключа в ньому немає. Це інша гілка коду, ніж
        # порожній кошик.
        #
        # Приклад:
        #   t = HashTable(size=1)
        #   t.insert("КІТ", "cat")
        #   t.get("ПЕС") -> KeyError
        t = HashTable(size=1)

        t.insert("КІТ", "cat")

        with self.assertRaises(KeyError):
            t.get("ПЕС")

    def test_get_after_collision(self):
        # Після кількох колізій кожен ключ усе одно має знаходитися
        # коректно. Це інтеграційний тест ланцюжкового методу.
        #
        # Приклад:
        #   t = HashTable(size=1)
        #   t.insert("КІТ",  "cat")
        #   t.insert("ПЕС",  "dog")
        #   t.insert("МИША", "mouse")
        #   t.get("КІТ")  -> "cat"
        #   t.get("ПЕС")  -> "dog"
        #   t.get("МИША") -> "mouse"
        t = HashTable(size=1)

        t.insert("КІТ", "cat")
        t.insert("ПЕС", "dog")
        t.insert("МИША", "mouse")

        self.assertEqual(t.get("КІТ"), "cat")
        self.assertEqual(t.get("ПЕС"), "dog")
        self.assertEqual(t.get("МИША"), "mouse")

    def test_get_supports_various_value_types(self):
        # Значенням може бути будь-який Python-об'єкт: число, список,
        # None. Тест має зафіксувати, що таблиця не накладає обмежень
        # на тип значення.
        #
        # Приклад:
        #   t.insert("А", 42)
        #   t.insert("Б", [1, 2, 3])
        #   t.insert("В", None)
        #   t.get("А") -> 42
        #   t.get("Б") -> [1, 2, 3]
        #   t.get("В") -> None
        t = HashTable()

        t.insert("А", 42)
        t.insert("Б", [1, 2, 3])
        t.insert("В", None)

        self.assertEqual(t.get("А"), 42)
        self.assertEqual(t.get("Б"), [1, 2, 3])
        self.assertIsNone(t.get("В"))

    def test_get_unsupported_character_raises_value_error(self):
        # get із некоректним ключем має падати з ValueError (від
        # hash_function), а не з KeyError — щоб користувач побачив
        # справжню причину проблеми.
        #
        # Приклад:
        #   t.get("CAT") -> ValueError  (а не KeyError!)
        t = HashTable()

        with self.assertRaises(ValueError):
            t.get("CAT")

    # ------------------------------------------------------------------
    # Тести delete
    # ------------------------------------------------------------------

    def test_delete_removes_key(self):
        # Після видалення ключ більше не повинен знаходитися.
        #
        # Приклад:
        #   t.insert("КІТ", "cat")
        #   t.delete("КІТ")
        #   t.get("КІТ") -> KeyError
        t = HashTable()

        t.insert("КІТ", "cat")
        t.delete("КІТ")

        with self.assertRaises(KeyError):
            t.get("КІТ")


def test_delete_missing_key_raises(self):
        # Видалення неіснуючого ключа — це помилка, а не "no-op".
        # Так користувач одразу побачить, що в його логіці щось не так.
        #
        # Приклад:
        #   t.delete("КІТ") -> KeyError
        t = HashTable()

        with self.assertRaises(KeyError):
            t.delete("КІТ")


def test_delete_missing_key_in_non_empty_bucket_raises(self):
        # Аналогічно до get: окремо перевірте випадок із непорожнім
        # кошиком, де потрібного ключа все одно немає.
        #
        # Приклад:
        #   t = HashTable(size=1)
        #   t.insert("КІТ", "cat")
        #   t.delete("ПЕС") -> KeyError
        t = HashTable(size=1)

        t.insert("КІТ", "cat")

        with self.assertRaises(KeyError):
            t.delete("ПЕС")

    def test_delete_keeps_other_keys_in_same_bucket(self):
        # Найважливіший тест для delete у контексті колізій: видалення
        # одного ключа НЕ повинно зачіпати сусідів у тому самому кошику.
        #
        # Приклад:
        #   t = HashTable(size=1)
        #   t.insert("КІТ", "cat")
        #   t.insert("ПЕС", "dog")
        #   t.delete("КІТ")
        #   t.get("ПЕС") -> "dog"     (сусід уцілів)
        #   t.get("КІТ") -> KeyError  (видалений)
        t = HashTable(size=1)

        t.insert("КІТ", "cat")
        t.insert("ПЕС", "dog")

        t.delete("КІТ")

        self.assertEqual(t.get("ПЕС"), "dog")

        with self.assertRaises(KeyError):
            t.get("КІТ")

    def test_delete_then_reinsert(self):
        # Перевірте повний життєвий цикл: вставка → видалення →
        # повторна вставка. Часта реальна послідовність дій.
        #
        # Приклад:
        #   t.insert("КІТ", "cat")
        #   t.delete("КІТ")
        #   t.insert("КІТ", "kitten")
        #   t.get("КІТ") -> "kitten"
        t = HashTable()

        t.insert("КІТ", "cat")
        t.delete("КІТ")

        t.insert("КІТ", "kitten")

        self.assertEqual(t.get("КІТ"), "kitten")


def test_delete_unsupported_character_raises_value_error(self):
        # Симетрично до get: некоректний ключ → ValueError.
        #
        # Приклад:
        #   t.delete("CAT") -> ValueError
        t = HashTable()

        with self.assertRaises(ValueError):
            t.delete("CAT")


if __name__ == "__main__":
    unittest.main()