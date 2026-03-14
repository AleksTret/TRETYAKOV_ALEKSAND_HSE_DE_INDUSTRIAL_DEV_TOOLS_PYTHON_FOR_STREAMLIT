markdown
# Энергетический дашборд

Веб-сервис для просмотра и редактирования данных о потреблении и ценах на энергию.

## Структура проекта
```text
task_04_service/
├── backend/ # FastAPI приложение
│ ├── main.py 
│ └── data.csv 
├── frontend/ # Streamlit приложение
│ └── app.py 
├── requirements.txt 
└── README.md 
```

## Установка

1. Создать виртуальное окружение:
    ```bash
    py -3.11 -m venv venv
    ```
    Активировать окружение:

    ```bash
    venv\Scripts\activate.ps1
    ```
    Установить зависимости:

    ```bashe 
    pip install -r requirements.txt
    ```

2. Запуск backend (FastAPI)
    ```bash
    uvicorn backend.main:app --reload
    ```
    Сервер будет доступен по адресу: http://127.0.0.1:8000

    Документация Swagger: http://127.0.0.1:8000/docs

    #### API Endpoints

    - `GET /records` - получить все записи (с опциональным параметром `limit`)
    - `POST /records` - добавить новую запись
    - `DELETE /records/{id}` - удалить запись по ID

    <img src="./assets/2026-03-14 152825.jpg" width="700"> 

    Для удобства получения записей установлен `LIMIT` 

    <img src="./assets/2026-03-14 152917.jpg" width="700"> 

    <img src="./assets/2026-03-14 152959.jpg" width="700"> 

    <img src="./assets/2026-03-14 153041.jpg" width="700"> 

    Исходные данные берутся из `RU_Electricity_Market_PZ_dayahead_price_volume.csv`

3. Запуск frontend (Streamlit)
    В отдельном терминале:

    ```bash
    streamlit run frontend/app.py
    ```
    Дашборд откроется в браузере по адресу: http://localhost:8501

4. Возможности
    - Просмотр данных в таблице
    - Добавление новых записей
    - Удаление записей по ID
    - Визуализация потребления и цен на графиках
    - Автоматическое сохранение данных в CSV
    - Валидация данных через Pydantic
    - Обработка ошибок с соответствующими HTTP статусами

    <img src="./assets/2026-03-14 153120.jpg" width="700"> 

    <img src="./assets/2026-03-14 153139.jpg" width="700"> 

    <img src="./assets/2026-03-14 153250.jpg" width="700"> 

    <img src="./assets/2026-03-14 153309.jpg" width="700"> 

    <img src="./assets/2026-03-14 153327.jpg" width="700"> 