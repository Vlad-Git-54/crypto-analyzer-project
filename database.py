# Модели и операции с базой данных.

from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker

# Подключение к SQLite 
engine = create_engine("sqlite:///crypto.db")
Base = declarative_base()
Session = sessionmaker(bind=engine)

# Модель данных
class CryptoData(Base):
    __tablename__ = "crypto_data"
    id = Column(Integer, primary_key=True)
    coin = Column(String, unique=True)  # Название криптовалюты
    price = Column(Float)  # Цена в USD

# Инициализация БД
def init_db():
    Base.metadata.create_all(engine)

# CRUD операции
def add_data(coin: str, price: float):
    """Добавление новой записи (Create)."""
    session = Session()
    existing = session.query(CryptoData).filter(CryptoData.coin == coin).first()
    if existing:
        existing.price = price 
    else:
        new_data = CryptoData(coin=coin, price=price)
        session.add(new_data)
    session.commit()
    session.close()

def get_data(coin: str):
    """Получение записи (Read)."""
    session = Session()
    data = session.query(CryptoData).filter(CryptoData.coin == coin).first()
    session.close()
    return data
