UKRAINIAN_ALPHABET = "АБВГҐДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯ"
class HashTable:
    """Хеш-таблиця для ключів, які складаються з літер української абетки."""

    def __init__(self, size=33):
        """
        Створює порожню хеш-таблицю.
        :param size: кількість кошиків у внутрішньому масиві.
            За замовчуванням 33 — стільки ж, скільки літер у абетці.
        Чому список списків?
            self.table — це масив кошиків. Кожен кошик — окремий список,
            у якому зберігаються пари (ключ, значення), що мають однаковий
            індекс після хешування. Завдяки цьому ми можемо обробляти
            колізії, не втрачаючи дані.
        """
        self.size = size
        self.table = [[] for _ in range(size)]

        # Словник для швидкого перетворення літери на число.
        # Будуємо його один раз у конструкторі, щоб не обчислювати щоразу
        # під час хешування — це пришвидшує hash_function().
        self.letter_to_number = {letter: index + 1 for index, letter in enumerate(UKRAINIAN_ALPHABET)}

    def hash_function(self, key):
        """
        Обчислює хеш ключа як суму числових кодів його літер.
        Алгоритм:
            1. Переводимо ключ у верхній регістр, щоб "кіт" і "КІТ" давали
               однаковий хеш (case-insensitive).
            2. Для кожної літери беремо її номер у абетці.
            3. Сумуємо ці номери.
        :raises ValueError: якщо ключ містить символ, якого немає в
            українській абетці (наприклад, латинську літеру або цифру).
        """
        key = key.upper()

        total = 0

        for char in key:
            if char not in self.letter_to_number:
                raise ValueError(f"Unsupported character: {char}")

            total += self.letter_to_number[char]

        return total

    def insert(self, key, value):
        """
        Додає пару (ключ, значення) у таблицю або оновлює існуючу.
        Як це працює:
            1. Обчислюємо хеш ключа і беремо остачу від ділення на size —
               так ми гарантовано отримаємо коректний індекс кошика.
            2. Перевіряємо, чи такий ключ вже є в кошику.
                - Якщо є — замінюємо його значення (оновлення).
                - Якщо немає — додаємо нову пару в кінець кошика.
        Чому потрібен прохід по кошику?
            Через колізії в одному кошику можуть лежати кілька різних
            ключів. Тому перед вставкою ми маємо перевірити кожен елемент.
        """
        index = self.hash_function(key) % self.size
        bucket = self.table[index]

        for item_index, item in enumerate(bucket):
            existing_key, _ = item

            if existing_key == key:
                bucket[item_index] = (key, value)
                return

        bucket.append((key, value))

    def get(self, key):
        """
        Повертає значення за ключем.
        :raises KeyError: якщо ключа немає в таблиці.
        Складність у середньому — O(1), у найгіршому випадку (коли всі
        ключі потрапили в один кошик) — O(n).
        """
        index = self.hash_function(key) % self.size
        bucket = self.table[index]

        for existing_key, value in bucket:
            if existing_key == key:
                return value

        raise KeyError(f"Key not found: {key}")

    def delete(self, key):
        """
        Видаляє пару за ключем.
        :raises KeyError: якщо ключа немає в таблиці.
        Видаляємо саме за індексом у кошику (а не за значенням), щоб не
        випадково не зачепити інший елемент із таким самим значенням.
        """
        index = self.hash_function(key) % self.size
        bucket = self.table[index]

        for item_index, item in enumerate(bucket):
            existing_key, _ = item

            if existing_key == key:
                del bucket[item_index]
                return

        raise KeyError(f"Key not found: {key}")

    def display(self):
        """
        Виводить вміст усіх кошиків. Корисно для налагодження та
        візуалізації того, як саме розподілилися ключі по таблиці.
        """
        for index, bucket in enumerate(self.table):
            print(f"{index}: {bucket}")