# Приложение для анализа погоды

Это проект на базе **Streamlit**, который позволяет анализировать исторические данные о температуре и сравнивать их с текущими погодными условиями, полученными через API OpenWeatherMap.
## Возможности

### 1. Загрузка и обработка данных
- Загрузка CSV-файлов с историческими данными о температуре.
- Автоматическая обработка данных:
  - Расчёт скользящих средних для сглаживания температурных колебаний.
  - Выявление аномалий на основе среднего и стандартного отклонения для сезона.

### 2. Интерактивные вкладки
Приложение разделено на три логические секции, доступные через вкладки:
- **Обзор**: 
  - Общая информация и вводные данные.
- **Анализ города**:
  - Анализ температурных трендов для выбранных городов.
  - Отображение сезонной статистики (минимальная, максимальная и средняя температура).
  - Визуализация скользящих средних, трендов и аномалий.
- **Аномалии**:
  - Подсветка городов или периодов с существенными аномалиями температуры.

### 3. Интеграция с API погоды
- Получение текущей температуры для городов через API OpenWeatherMap.
- Сравнение текущих данных с историческими для определения их соответствия норме.

### 4. Модульная структура кода
Проект разделён на модули:
- `main.py`: Точка входа в приложение.
- `data.py`: Обработка данных, выявление аномалий и расчёт трендов.
- `client.py`: Работа с API OpenWeatherMap для получения данных о температуре.

## Как запустить локально

### Требования
- Python 3.10 или новее
- pip
- API-ключ OpenWeatherMap (бесплатный ключ можно получить на сайте [OpenWeatherMap](https://openweathermap.org/)).

### Шаги
1. Клонируйте репозиторий:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```
2. Создайте виртуальное окружение и активируйте его:
   ```bash
   python -m venv venv
   source venv/bin/activate   # Для Linux/MacOS
   .\venv\Scripts\activate    # Для Windows
   ```
3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
4. Запустите приложение:
   ```bash
   streamlit run main.py
   ```
5. Откройте приложение в браузере:
   ```
   http://localhost:8501
   ```

## Запуск с помощью Docker

1. Соберите Docker-образ:
   ```bash
   docker build -t weather-analysis .
   ```

2. Запустите контейнер:
   ```bash
   docker run -p 8501:8501 weather-analysis
   ```

3. Откройте приложение по адресу:
   ```
   http://localhost:8501
   ```

## Структура проекта

```
📦 Папка проекта
├── Dockerfile            # Конфигурация Docker
├── requirements.txt      # Зависимости Python
├── main.py               # Основной файл приложения Streamlit
├── data.py               # Логика обработки и анализа данных
├── client.py             # Работа с API OpenWeatherMap
├── temperature_data.csv  # Пример CSV-файла с историческими данными
└── README.md             # Документация проекта
```

## Формат входных данных
Приложение ожидает CSV-файл со следующими колонками:
- `city`: Название города (например, Moscow, Tokyo).
- `timestamp`: Дата в формате `YYYY-MM-DD`.
- `temperature`: Средняя дневная температура в °C.
- `season`: Сезон (зима, весна, лето, осень).


## Что не успели реализовать
- **Анимации:**
  - Планировалось добавить анимации, такие как изменение температуры на временном интервале
  - Это улучшило бы интерактивность приложения и позволило визуализировать данные более наглядно.

- **Доработка тем:**
  - Хотел расширить выбор тем (кстомные)

## Итоги
Данное приложение демонстрирует возможности анализа температурных данных и интеграции с API. Основные реализованные функции:
- Обработка данных и выявление аномалий
- Интерактивный интерфейс с вкладками
- Интеграция с OpenWeatherMap API для получения текущих температур


## Идеи для улучшений
- Добавить больше тем и опций для кастомизации.
- Включить визуализацию дополнительных погодных параметров (например, ветер, влажность)
- Оптимизировать производительность для работы с большими наборами данных
- Провести глубокий анализ временных рядов