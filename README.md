## ToDo API

REST API для управления списком задач (ToDo) на FastAPI и PostgreSQL.

### Функциональность

- **Регистрация и аутентификация** пользователей (JWT).
- **CRUD** операций над задачами:
  - Создание
  - Просмотр списка
  - Просмотр конкретной задачи
  - Обновление и удаление
- **Права доступа**:
  - Только автор задачи может выдавать/отзывать права другим пользователям.
  - Возможные права: чтение, обновление.

### Структура проекта

```
├── app/
│   ├── main.py          
│   ├── database.py      
│   ├── models.py        
│   ├── schemas.py       
│   ├── crud.py          
│   ├── auth.py          
│   ├── deps.py          
│   └── routers/
│       ├── users.py     
│       └── tasks.py     
├── alembic/             
├── tests/               
│   └── test_basic.py    
├── .env.example         
├── requirements.txt     
├── pytest.ini           
└── README.md            
```

### Требования

- Python 3.10+
- PostgreSQL
- FastAPI
- SQLAlchemy
- Alembic
- Uvicorn
- Pytest

### Установка и запуск

1. **Клонировать репозиторий**:
   ```bash
   git clone https://github.com/aivazovaa/apitodo.git
   cd apitodo
   ```
2. **Создать виртуальное окружение** и активировать его:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. **Скопировать пример окружения** и настроить `.env`:
   ```bash
   cp .env.example .env
   # Отредактировать DATABASE_URL и SECRET_KEY
   ```
4. **Установить зависимости**:
   ```bash
   pip install -r requirements.txt
   ```
5. **Настроить базу данных** PostgreSQL:
   ```sql
   CREATE DATABASE tododb;
   CREATE USER todo_user WITH PASSWORD 'todo_pass';
   GRANT ALL PRIVILEGES ON DATABASE tododb TO todo_user;
   ```
6. **Создать таблицы** (миграции или вручную):
   ```bash
   alembic upgrade head
   # или
   python3 - << 'EOF'
   from app.database import engine, Base
   import app.models
   Base.metadata.create_all(bind=engine)
   EOF
   ```
7. **Запустить приложение**:
   ```bash
   uvicorn app.main:app --reload
   ```
8. **Проверить Swagger UI**: Открыть в браузере [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### Тестирование

1. Активировать окружение и убедиться, что тестовая БД настроена.
2. Запустить pytest:
   ```bash
   pytest -q
   ```

