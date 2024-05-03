import json
import uuid
'''
Создание нового json файла с преоразованными id
'''


def update_book_ids(data):
    updated_data = {}
    for key, book in data.items():
        if key.isdigit():
            updated_id = str(uuid.uuid4())
            book['id'] = updated_id
            updated_data[updated_id] = book
        else:
            updated_data[key] = book
    return updated_data


def main():
    # Загрузка данных из файла
    with open('assets/books.json') as file:
        data = json.load(file)

    # Обновление ID книг
    updated_data = update_book_ids(data)

    # Запись обновленных данных в файл
    with open('bd_updated.json', 'w') as file:
        json.dump(updated_data, file, indent=4)


if __name__ == "__main__":
    main()
