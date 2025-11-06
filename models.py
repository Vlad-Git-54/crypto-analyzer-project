# Pydantic модели для валидации данных

from pydantic import BaseModel, Field

# Модель для ввода данных с валидацией
class CryptoInput(BaseModel):
    coin: str = Field(..., min_length=3, description="Название криптовалюты (минимум 3 символа)")
    price: float = Field(..., gt=0, description="Цена должна быть положительной")
