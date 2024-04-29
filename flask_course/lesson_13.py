from flask import Flask

from data import UserRepository, user, user2

import os

app = Flask(__name__)
# Секретный ключ, который используется для криптографической подписи
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')  # файла сессии

# Хранилище объектов
repo = UserRepository()

# Сохранение
repo.save(user)

# Ещё одно сохранение
repo.save(user2)

# Извлечение по идентификатору
repo.find(user.id)  # => user

# Извлечение всех сущностей
repo.content()  # => [user, user2]
