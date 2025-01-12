import asyncio
from datetime import date
import pandas as pd
import pydeck as pdk
import streamlit as st

from client import get_temperature_async
from data import data_prep, compare_temperature, hist_plot, city_stats, trend_calc

CITY_COORDINATES = {
    'New York': (40.7128, -74.0060),
    'London': (51.5074, -0.1278),
    'Paris': (48.8566, 2.3522),
    'Tokyo': (35.6895, 139.6917),
    'Moscow': (55.7558, 37.6173),
    'Sydney': (-33.8688, 151.2093),
    'Berlin': (52.5200, 13.4050),
    'Beijing': (39.9042, 116.4074),
    'Rio de Janeiro': (-22.9068, -43.1729),
    'Dubai': (25.276987, 55.296249),
    'Los Angeles': (34.0522, -118.2437),
    'Singapore': (1.3521, 103.8198),
    'Mumbai': (19.0760, 72.8777),
    'Cairo': (30.0444, 31.2357),
    'Mexico City': (19.4326, -99.1332)
}

PAGE_TITLE = "Weather Analysis"

def set_page_config():
    st.set_page_config(
        layout="wide",
        initial_sidebar_state="auto",
        page_title=PAGE_TITLE,
    )

def render_main_page():
    st.title("Анализ температуры в выбранных городах")

def upload_file():
    st.header("Загрузка данных наблюдений")
    uploaded_file = st.file_uploader("Выберите файл CSV", type="csv")
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
        return data_prep(df)
    st.info("Загрузите CSV-файл для анализа.")
    return None

def select_city(cities):
    return st.radio("Выберите режим:", ['Один город', 'Несколько городов'])

def render_map(city, latitude, longitude):
    layer = pdk.Layer(
        'ScatterplotLayer',
        data=[{'latitude': latitude, 'longitude': longitude}],
        get_position='[longitude, latitude]',
        get_color='[200, 30, 0, 160]',
    )
    view_state = pdk.ViewState(
        latitude=latitude,
        longitude=longitude,
        zoom=10,
        pitch=0,
    )
    st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state))

def analyze_city_data(df, city):
    latitude, longitude = CITY_COORDINATES[city]
    st.subheader(f"Координаты города: {city}")
    render_map(city, latitude, longitude)

    city_df = df[df['city'] == city]
    st.subheader(f"Данные для города {city}")
    st.dataframe(city_df)

    stats = city_stats(city_df, city)
    st.metric("Минимальная температура", f"{stats['min_temperature']:.2f} °C")
    st.metric("Средняя температура", f"{stats['average_temperature']:.2f} °C")
    st.metric("Максимальная температура", f"{stats['max_temperature']:.2f} °C")

    pred, trend = trend_calc(city_df, city)
    st.write(trend)

    st.plotly_chart(hist_plot(city_df, stats, city, pred))

def fetch_temperature(city, api_key, df):
    temp = asyncio.run(get_temperature_async(city, api_key))
    if temp is None:
        st.error(f"Ошибка получения температуры для {city}.")
    else:
        st.subheader(f"Текущая температура в {city}: {temp} °C")
        comparison = compare_temperature(date.today(), temp, city, df)
        st.text(comparison)

def apply_custom_theme():
    st.markdown(
        """
        <style>
        .css-1d391kg {{
            background-color: #f0f0f5;
        }}
        .css-18e3th9 {{
            color: #4CAF50;
        }}
        .css-1q8dd3e {{
            color: #262730;
        }}
        .stButton > button {{
            background-color: #4CAF50;
            color: white;
            border-radius: 5px;
            border: none;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def main():
    set_page_config()
    apply_custom_theme()
    render_main_page()

    df = upload_file()
    if df is not None:
        cities = df['city'].unique()
        tab1, tab2, tab3 = st.tabs(["Обзор", "Анализ города", "Аномалии"])

        with tab1:
            st.header("Общая информация")
            st.write("Добавьте сюда элементы для общего анализа.")

        with tab2:
            city_mode = select_city(cities)

            if city_mode == 'Один город':
                city = st.selectbox("Выберите город:", cities)
                analyze_city_data(df, city)
            else:
                st.write("Режим: несколько городов.")

        with tab3:
            st.header("Аномалии температуры")
            st.write("Добавьте визуализацию аномалий.")

        api_key = st.text_input("Введите API-ключ OpenWeatherMap:", type="password")
        if api_key:
            for city in cities:
                fetch_temperature(city, api_key, df)

if __name__ == "__main__":
    main()
