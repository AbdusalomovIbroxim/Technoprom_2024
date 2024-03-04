# Technoprom

# Инструкция по установке и запуску проекта

## Шаг 1: Клонирование репозитория

Склонируйте репозиторий проекта из Git:

```bash
https://github.com/AbdusalomovIbroxim/Technoprom_2024.git
```

## Шаг 2: Изменение имени файла `.env(copy)` на `.env`

Переименуйте файл `.env(copy)` в `.env`.

```bash
mv .env\(copy\) .env
```

[//]: # (необходимые данные в файл .env, такие как настройки базы данных, секретный ключ и другие конфигурационные параметры)

## Шаг 3: Добавление данных в файл .env

```text
SECRET_KEY="SECRET_KEY"
EMAIL_HOST_USER="EMAIL_HOST_USER"
EMAIL_HOST_PASSWORD="EMAIL_HOST_PASSWORD"
DEBUG="DEBUG"
TOKEN="TOKEN"
CHAT_ID="CHAT_ID"
```

Добавьте необходимые данные в файл .env, такие как настройки базы данных, секретный ключ и другие конфигурационные
параметры.

## Шаг 4: Установка зависимостей

Установите необходимые зависимости из файла requirements.txt, выполнив следующую команду:

```bash
pip install -r requirements.txt
```

## Шаг 5: Создание и применение миграций базы данных

Создайте и примените миграции базы данных:

```bash
python manage.py makemigrations
python manage.py migrate
```

## Шаг 6: Запуск проекта

Теперь вы можете запустить проект, выполнив следующую команду:

```bash
python manage.py runserver
```

После этого вы сможете открыть ваш проект в браузере по адресу http://localhost:8000/.

