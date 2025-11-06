# Маршруты (Controllers) для FastAPI.
# Интегрирует шаблоны, анализ, многозадачность.

from fastapi import APIRouter, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from database import get_data, add_data
from models import CryptoInput
from utils import (async_task, threaded_task, process_task, expensive_function,
                   fetch_crypto_price)
import asyncio
import pandas as pd
import plotly.express as px

crypto_router = APIRouter(prefix="/crypto")

templates = Jinja2Templates(directory="templates")

# Async эндпоинт для цены 
@crypto_router.get("/price/{coin}")
async def get_price(coin: str):
    """Получить цену криптовалюты из БД или API."""
    data = get_data(coin)
    if data:
        return {"price": data.price}
    # Если нет в БД, fetch async
    price = await fetch_crypto_price(coin)
    if price is None:
        raise HTTPException(status_code=404, detail="Coin not found")
    add_data(coin, price)  # Сохраняем в БД
    return {"price": price}

# POST с валидацией
@crypto_router.post("/add")
def add_crypto(data: CryptoInput):
    """Добавить/обновить данные в БД."""
    add_data(data.coin, data.price)
    return {"message": "Added/Updated"}

# Шаблон для просмотра
@crypto_router.get("/view/{coin}")
def view_crypto(coin: str, request: Request):
    """Отобразить данные через динамический шаблон."""
    data = get_data(coin)
    if not data:
        raise HTTPException(404, detail="Data not found")
    return templates.TemplateResponse("index.html", {"request": request, "coin": data.coin, "price": data.price})

# Анализ и визуализация
@crypto_router.get("/analyze/{coin}")
async def analyze(coin: str):
    """Анализ данных с Pandas, async API и Plotly график."""
    price = await fetch_crypto_price(coin)  # Async API
    if price is None:
        raise HTTPException(404, detail="Coin not found")
    
    # Pandas обработка (фильтрация)
    df = pd.DataFrame({"coin": [coin, coin], "price": [price, price * 1.1]})  # Симуляция данных
    filtered = df[df['price'] > 0]  # Фильтрация
    
    # Plotly визуализация
    fig = px.line(filtered, x="coin", y="price", title=f"Price Analysis for {coin}")
    graph = fig.to_html(full_html=False)
    
    return HTMLResponse(content=graph)

# Демонстрация многозадачности
@crypto_router.get("/demo-multitask")
async def demo_multitask():
    """Демонстрация декораторов и многозадачности."""
    # Asyncio
    results = await asyncio.gather(async_task(1), async_task(2))
    
    # Threading
    thread = threading.Thread(target=threaded_task)
    thread.start()
    thread.join()
    
    # Multiprocessing
    proc = Process(target=process_task)
    proc.start()
    proc.join()
    
    # Декоратор
    cached = expensive_function(10)
    
    return {"async_results": results, "cached": cached}
