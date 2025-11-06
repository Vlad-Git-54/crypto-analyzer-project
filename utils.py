# Утилиты для декораторов и многозадачности

import functools
import time
import asyncio
import threading
from multiprocessing import Process
import aiohttp

# Декоратор с параметрами для кэширования
def cache(ttl=60):
    """Декоратор для кэширования результатов функции на заданное время (ttl в секундах)."""
    def decorator(func):
        cache_data = {}
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = str(args) + str(kwargs)
            if key in cache_data and time.time() - cache_data[key]['time'] < ttl:
                return cache_data[key]['value']
            result = func(*args, **kwargs)
            cache_data[key] = {'value': result, 'time': time.time()}
            return result
        return wrapper
    return decorator

# Пример функции с декоратором
@cache(ttl=30)
def expensive_function(x):
    """Симуляция тяжёлой функции."""
    time.sleep(1)
    return x * 2

# Async задача
async def async_task(delay):
    """Асинхронная задача с задержкой."""
    await asyncio.sleep(delay)
    return f"Task completed after {delay} seconds"

# Threading задача
def threaded_task():
    """Задача в отдельном потоке."""
    print("Thread started")
    time.sleep(2)
    print("Thread finished")

# Multiprocessing задача
def process_task():
    """Задача в отдельном процессе."""
    print("Process started")
    time.sleep(2)
    print("Process finished")

# Async интеграция с внешним API
async def fetch_crypto_price(coin: str):
    """Асинхронный запрос к CoinGecko API для получения цены."""
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                return None
            data = await resp.json()
            return data.get(coin, {}).get("usd")
