import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# Константы
API_URL = "http://127.0.0.1:8000"

# Настройка страницы
st.set_page_config(page_title="Energy Dashboard", layout="wide")
st.title("Энергетический дашборд")

# Функции для работы с API
def fetch_data(limit=None):
    """Получить данные из API"""
    try:
        url = f"{API_URL}/records"
        if limit:
            url += f"?limit={limit}"
        response = requests.get(url)
        response.raise_for_status()
        return pd.DataFrame(response.json())
    except requests.exceptions.RequestException as e:
        st.error(f"Ошибка подключения к API: {e}")
        return pd.DataFrame()

def add_record(record):
    """Добавить запись через API"""
    try:
        response = requests.post(f"{API_URL}/records", json=record)
        response.raise_for_status()
        return True, response.json()
    except requests.exceptions.RequestException as e:
        return False, str(e)

def delete_record(record_id):
    """Удалить запись через API"""
    try:
        response = requests.delete(f"{API_URL}/records/{record_id}")
        if response.status_code == 404:
            return False, "ID не найден"
        response.raise_for_status()
        return True, "Удалено"
    except requests.exceptions.RequestException as e:
        return False, str(e)

# Загружаем данные
if 'data' not in st.session_state:
    st.session_state.data = fetch_data(limit=100)

# Боковая панель с кнопкой обновления
with st.sidebar:
    st.header("Управление")
    if st.button("Обновить данные"):
        st.session_state.data = fetch_data(limit=100)
        st.success("Данные обновлены")
    
    st.divider()
    
    # Удаление записи
    st.subheader("Удаление записи")
    delete_id = st.number_input("ID записи для удаления", min_value=1, step=1)
    if st.button("Удалить", type="primary"):
        success, message = delete_record(delete_id)
        if success:
            st.success(f"Запись {delete_id} удалена")
            st.session_state.data = fetch_data(limit=100)
        else:
            st.error(f"Ошибка: {message}")

# Основная область
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Таблица данных")
    if not st.session_state.data.empty:
        st.dataframe(st.session_state.data, use_container_width=True)
    else:
        st.info("Нет данных для отображения")

with col2:
    st.subheader("Добавить запись")
    with st.form("add_form"):
        timestep = st.text_input("Timestamp (YYYY-MM-DD HH:MM)", "2024-01-01 12:00")
        consumption_eur = st.number_input("consumption_eur", min_value=0.0, value=50000.0)
        consumption_sib = st.number_input("consumption_sib", min_value=0.0, value=15000.0)
        price_eur = st.number_input("price_eur", min_value=0.0, value=450.0)
        price_sib = st.number_input("price_sib", min_value=0.0, value=100.0)

        submitted = st.form_submit_button("Добавить")
        if submitted:
            new_record = {
                "timestep": timestep,
                "consumption_eur": consumption_eur,
                "consumption_sib": consumption_sib,
                "price_eur": price_eur,
                "price_sib": price_sib
            }
            success, result = add_record(new_record)
            if success:
                st.success("Запись добавлена")
                st.session_state.data = fetch_data(limit=100)
            else:
                st.error(f"Ошибка: {result}")

st.subheader("Визуализация")

if not st.session_state.data.empty:
    df = st.session_state.data
    df['timestep'] = pd.to_datetime(df['timestep'])
    df = df.sort_values('timestep')

    tab1, tab2 = st.tabs(["Потребление", "Цены"])

    with tab1:
        fig1 = px.line(df, x='timestep', y=['consumption_eur', 'consumption_sib'],
                      title='Потребление энергии (Европа vs Сибирь)',
                      labels={'value': 'МВт', 'timestep': 'Время', 'variable': 'Регион'})
        st.plotly_chart(fig1, use_container_width=True)

    with tab2:
        fig2 = px.line(df, x='timestep', y=['price_eur', 'price_sib'],
                      title='Цены на энергию (Европа vs Сибирь)',
                      labels={'value': 'Цена', 'timestep': 'Время', 'variable': 'Регион'})
        st.plotly_chart(fig2, use_container_width=True)
else:
    st.warning("Загрузите данные для отображения графиков")