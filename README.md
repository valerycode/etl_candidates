# Описание проекта
Скрипт, который позволяет загружать данные:
- резюме кандидатов(файлы с расширением .doc и .pdf)
- информацию о самих кандидатах из файла Excel c БД

в систему Хантфлоу с помощью API - https://dev-100-api.huntflow.dev/v2/docs
### Технологии
- [Python 3.10](https://www.python.org/) - is an interpreted high-level general-purpose programming language.
- [Openpyxl](https://openpyxl.readthedocs.io/en/stable/) - is a Python library to read/write Excel 2010 xlsx/xlsm/xltx/xltm files.
- [Pydantic](https://docs.pydantic.dev/latest/) - is the most widely used data validation library for Python.
- [Requests](https://requests.readthedocs.io/en/latest/user/quickstart/) - is a module allows you to send HTTP requests using Python.

### Как развернуть проект

- скачать репозиторий, перейти в директорию с проектом

```git clone git@github.com:ваш-логин/etl_candidates.git```

```cd /<путь-до-директории>/```

- создать виртуальное окружение, активировать его

```python3.10 -m venv venv```

```. venv/bin/activate```

- установить зависимости

```python -m pip install -r requirements.txt```

- переименовать файл `.env.example` в `.env` и добавить свои данные в переменные:
```
ORGANIZATION_NAME
API_URL
ACCESS_TOKEN
FILE_PATH
LOGGING_LEVEL
FILEMODE
FILENAME
```

- запустить скрипт

```python main.py```

### Список планируемых доработок

- Сделать методы класса Loader более универсальными
- Добавить класс State, который бы хранил состояние, на каком этапе загрузке была прекращена работа скрипта
- Добавить тесты
- Добавить backoff на запросы к API(на случай, если API в течение какого-то времени недоступно)
