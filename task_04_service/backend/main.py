import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os

# Определяем окружение
IS_PRODUCTION = os.environ.get("RENDER", False)

if IS_PRODUCTION:
    # На Render - данные будут храниться в памяти (файлы недоступны)
    ORIGINAL_FILE = None
    WORKING_FILE = None
    in_memory_data = None
else:
    # Локально - работаем с файлами
    ORIGINAL_FILE = "RU_Electricity_Market_PZ_dayahead_price_volume.csv"
    WORKING_FILE = "backend/data.csv"

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Константы с путями к файлам
ORIGINAL_FILE = "RU_Electricity_Market_PZ_dayahead_price_volume.csv"
WORKING_FILE = "backend/data.csv"

# Pydantic модели
class RecordCreate(BaseModel):
    timestep: str
    consumption_eur: float
    consumption_sib: float
    price_eur: float
    price_sib: float

class Record(RecordCreate):
    id: int

# Функции для работы с CSV
def init_data():
    """Создает рабочий файл при первом запуске"""
    if not os.path.exists(WORKING_FILE):
        if not os.path.exists(ORIGINAL_FILE):
            raise HTTPException(status_code=500, detail="Исходный файл не найден")
        
        df = pd.read_csv(ORIGINAL_FILE)
        df.insert(0, 'id', range(1, len(df) + 1))
        df.to_csv(WORKING_FILE, index=False)

def load_data() -> pd.DataFrame:
    """Загружает данные из рабочего файла"""
    if not os.path.exists(WORKING_FILE):
        init_data()
    
    try:
        df = pd.read_csv(WORKING_FILE)
        return df
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка чтения файла: {str(e)}")

def save_data(df: pd.DataFrame):
    """Сохраняет данные в рабочий файл"""
    try:
        df.to_csv(WORKING_FILE, index=False)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка сохранения файла: {str(e)}")

# Эндпоинты
@app.get("/records", response_model=List[Record])
def get_records(limit: Optional[int] = None):
    """Получить все записи или ограничить количество параметром limit"""
    df = load_data()
    
    if limit:
        df = df.head(limit)
    
    return df.to_dict('records')

@app.post("/records", response_model=Record)
def add_record(record: RecordCreate):
    """Добавить новую запись"""
    df = load_data()
    
    # Генерируем новый id
    new_id = df['id'].max() + 1 if not df.empty else 1
    
    # Создаем новую запись
    new_record = record.model_dump()
    new_record['id'] = new_id
    
    # Добавляем в DataFrame
    df = pd.concat([df, pd.DataFrame([new_record])], ignore_index=True)
    
    # Сохраняем
    save_data(df)
    
    return new_record

@app.delete("/records/{id}")
def delete_record(id: int):
    """Удалить запись по id"""
    df = load_data()
    
    # Проверяем существует ли id
    if id not in df['id'].values:
        raise HTTPException(status_code=404, detail=f"Запись с id {id} не найдена")
    
    # Удаляем запись
    df = df[df['id'] != id]
    
    # Сохраняем
    save_data(df)
    
    return {"message": f"Запись с id {id} удалена"}

# Инициализация при запуске
init_data()