
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import plotly.express as px

def data_prep(df):
    df['moving_avg'] = df.groupby('city')['temperature'].transform(
        lambda x: x.rolling(window=30, min_periods=1).mean()
    )
    seasonal_stats = df.groupby(['city', 'season'])['temperature'].agg(['mean', 'std']).reset_index()
    df = df.merge(seasonal_stats, on=['city', 'season'], suffixes=('', '_seasonal'))
    df['is_anomaly'] = (
        (df['temperature'] < (df['mean'] - 2 * df['std'])) | 
        (df['temperature'] > (df['mean'] + 2 * df['std']))
    )
    return df

def trend_calc(city_df, city):
    city_df = city_df[~city_df['is_anomaly']]
    city_df['timestamp'] = pd.to_datetime(city_df['timestamp'])
    
    X = city_df['timestamp'].astype('int64').values.reshape(-1, 1)
    y = city_df['temperature'].values

    model = LinearRegression()
    model.fit(X, y)
    pred = model.predict(X)

    trend = 'положительный' if model.coef_[0] > 0 else 'отрицательный'
    return pred, f"Наблюдается {trend} тренд температуры в городе {city}."

def city_stats(df, city_name):
    seasonal_profile = df.groupby('season')['temperature'].agg(['mean', 'std']).reset_index()
    return {
        'min_temperature': df['temperature'].min(),
        'average_temperature': df['temperature'].mean(),
        'max_temperature': df['temperature'].max(),
        'seasonal_profile': seasonal_profile
    }

def compare_temperature(date, actual_temp, city, df):
    date = pd.to_datetime(date)
    city_data = df[(df['city'] == city) & 
                   (df['timestamp'].dt.month == date.month) & 
                   (df['timestamp'].dt.day == date.day) & 
                   (~df['is_anomaly'])]

    if city_data.empty:
        return f"Нет данных для города {city} на указанную дату."

    mean_temp = city_data['temperature'].median()
    std_temp = city_data['temperature'].std()
    deviation = actual_temp - mean_temp

    if abs(deviation) < std_temp:
        assessment = "Температура в пределах нормы."
    elif abs(deviation) < 2 * std_temp:
        assessment = "Температура немного отличается от нормы."
    else:
        assessment = "Температура сильно отличается от нормы."

    return (
        f"Город: {city}\n"
        f"Фактическая температура: {actual_temp}°C\n"
        f"Средняя историческая температура: {round(mean_temp, 2)}°C\n"
        f"Отклонение: {round(deviation, 2)}°C\n"
        f"Вывод: {assessment}\n"
    )

def hist_plot(df, stats, city, pred):
    fig = px.line(df, x='timestamp', y='temperature', 
                  labels={'temperature': 'Температура (°C)', 'timestamp': 'Дата'},
                  title=f'Температура и аномалии в {city}')

    anomalies = df[df['is_anomaly']]
    fig.add_scatter(x=anomalies['timestamp'], y=anomalies['temperature'], 
                    mode='markers', name='Аномалии', marker=dict(color='red'))
    fig.add_scatter(x=df['timestamp'], y=pred, mode='lines', 
                    name='Тренд', line=dict(color='black', width=2))

    return fig