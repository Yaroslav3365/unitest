# unitest
# 🧠 Hash Table на Python

Проста реалізація Hash Table на Python з підтримкою української абетки та unit-тестами.

---

# 📚 Зміст

- [✨ Особливості](#-особливості)
- [📂 Структура проєкту](#-структура-проєкту)
- [🔤 Українська абетка](#-українська-абетка)
- [⚡ Як працює hash function](#-як-працює-hash-function)
- [🪣 Buckets](#-buckets)
- [💥 Колізії](#-колізії)
- [➕ insert](#-insert)
- [🔍 get](#-get)
- [❌ delete](#-delete)
- [🧪 Unit Tests](#-unit-tests)
- [🚀 Запуск](#-запуск)
- [📝 Приклад використання](#-приклад-використання)

---

# ✨ Особливості

✅ Власна Hash Table  
✅ Українська абетка  
✅ Case-insensitive ключі  
✅ Collision handling  
✅ Unit tests  
✅ Обробка помилок  
✅ Підтримка будь-яких типів значень  

---

# 📂 Структура проєкту

```text
project/
│
├── hash_table.py
├── test_hash_table.py
└── README.md
```

---

# 🔤 Українська абетка

```python
UKRAINIAN_ALPHABET = [
    "А", "Б", "В", "Г", "Ґ", "Д", "Е", "Є", "Ж",
    "З", "И", "І", "Ї", "Й", "К", "Л", "М", "Н",
    "О", "П", "Р", "С", "Т", "У", "Ф", "Х", "Ц",
    "Ч", "Ш", "Щ", "Ь", "Ю", "Я"
]
```

Кожна літера має номер:

```text
А = 1
Б = 2
...
Я = 33
```

---

# ⚡ Як працює hash function

Hash function перетворює слово у число.

## Приклад

```python
hash_function("КІТ")
```

## Обчислення

```text
К = 15
І = 12
Т = 23

15 + 12 + 23 = 50
```

## Результат

```python
50
```

---

# 🪣 Buckets

Hash Table складається з buckets.

```python
[
    [],
    [],
    [("КІТ", "cat")],
    [],
]
```

Bucket — це список елементів.

---

# 💥 Колізії

Колізія виникає коли різні ключі потрапляють у той самий bucket.

## Приклад

```python
t = HashTable(size=1)
```

Тепер усі ключі потрапляють у bucket `0`.

```python
[
    ("КІТ", "cat"),
    ("ПЕС", "dog"),
]
```

Для цього використовується:

## 🔗 Chaining

---

# ➕ insert

```python
t.insert("КІТ", "cat")
```

## Алгоритм

1. Рахується hash
2. Обирається bucket
3. Якщо ключ існує → update
4. Якщо ні → append

---

# 🔍 get

```python
t.get("КІТ")
```

## Алгоритм

1. Рахується hash
2. Знаходиться bucket
3. Шукається ключ
4. Повертається value

## Якщо ключа нема

```python
KeyError
```

---

# ❌ delete

```python
t.delete("КІТ")
```

## Алгоритм

1. Знаходиться bucket
2. Шукається ключ
3. Елемент видаляється

## Якщо ключ не існує

```python
KeyError
```

---

# 🧪 Unit Tests

Для тестування використовується:

```python
unittest
```

## Тести перевіряють

- hash_function
- insert
- get
- delete
- collisions
- update existing key
- edge cases
- ValueError
- KeyError

---

# 🚀 Запуск

## Запуск усіх тестів

```bash
python -m unittest
```

або

```bash
pytest
```

---

# 📝 Приклад використання

```python
from hash_table import HashTable

t = HashTable()

t.insert("КІТ", "cat")
t.insert("ПЕС", "dog")

print(t.get("КІТ"))
print(t.get("ПЕС"))

t.delete("КІТ")
```

## Результат

```text
cat
dog
```

---

# 🛠️ Особливості реалізації

## Правильне створення buckets

✅ Правильно:

```python
self.table = [[] for _ in range(size)]
```

❌ Неправильно:

```python
self.table = [[]] * size
```

Інакше всі buckets будуть одним списком.

---

# 📖 Основні поняття

| Термін | Опис |
|---|---|
| Hash Function | Перетворює ключ у число |
| Bucket | Список елементів |
| Collision | Однаковий index для різних ключів |
| Chaining | Зберігання кількох елементів у bucket |

---

# 🎯 Висновок

У цьому проєкті реалізовано:

- Hash Table
- Hash Function
- Collision Handling
- insert/get/delete
- Unit Tests
- Error Handling

Проєкт допомагає зрозуміти:

- як працюють Hash Tables
- як працює hashing
- як працюють collisions
- як писати unit tests
- як працює Python dict

---

# 👨‍💻 Автор

Навчальний проєкт для практики Python та структур даних.
