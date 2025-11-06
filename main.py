# main.py: Основной файл приложения. Реализует FastAPI app, инициализацию и подключение маршрутов.

from fastapi import FastAPI
from fastapi.templating import Jinja2Templates  # Для шаблонов
from database import init_db  # Инициализация БД
from routers.crypto import crypto_router  # Контроллеры 

app = FastAPI(title="Crypto Analyzer")  # Основное приложение FastAPI

# Подключение шаблонов 
templates = Jinja2Templates(directory="templates")

# Инициализация при старте
@app.on_event("startup")
async def startup():
    init_db()  # Создаём таблицы в БД

# Подключение маршрутов
app.include_router(crypto_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)  # Запуск сервера
