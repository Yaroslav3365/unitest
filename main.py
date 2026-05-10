from hash_table import HashTable


def main():
    hash_table = HashTable()

    hash_table.insert("МОЛОКО", "75 грн")
    hash_table.insert("МОРКВА", "22 грн")
    hash_table.insert("ОГІРКИ", "16 грн")
    hash_table.insert("СМЕТАНА", "66 грн")
    hash_table.insert("ЯБЛУКА", "12 грн")
    hash_table.insert("МЯСО", "150 грн")

    print("Хеш-таблиця:")
    hash_table.display()

    print()
    print("Пошук:")
    print("МОЛОКО ->", hash_table.get("МОЛОКО"))
    print("МОРКВА ->", hash_table.get("МОРКВА"))

    print()
    print("Видалення ОГІРКИ")
    hash_table.delete("ОГІРКИ")
    hash_table.display()


if __name__ == "__main__":
    main()