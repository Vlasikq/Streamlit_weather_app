import aiohttp
import asyncio

def format_api_error(error_message):
    return f"Ошибка API: {error_message}"

async def get_temperature_async(city_name, api_key):
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city_name,
        'appid': api_key,
        'units': 'metric'}

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(base_url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return data['main']['temp']
                else:
                    error_data = await response.json()
                    return format_api_error(error_data.get('message', 'Неизвестная ошибка'))
    except aiohttp.ClientError as e:
        return format_api_error(str(e))

async def get_multiple_temperatures(cities, api_key):
    tasks = {city: get_temperature_async(city, api_key) for city in cities}
    results = await asyncio.gather(*tasks.values(), return_exceptions=True)
    return dict(zip(tasks.keys(), results))