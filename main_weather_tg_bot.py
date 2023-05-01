import requests
import datetime
from config import tg_bot_token, open_weather_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor


bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply('Привет! Напиши мне название города и я пришлю сводку погоды!')


@dp.message_handler()
async def get_weather(message: types.Message):
    code_to_smile = {
        'Clear': 'Ясно \U00002600',
        'Clouds': 'Облачно \U00002601',
        'Rain': 'Дождь \U00002614',
        'Drizzle': 'Дождь \U00002614',
        'Thunderstorm': 'Гроза \U000026A1',
        'Snow': 'Снег \U0001F328',
        'Mist': 'Туман \U0001F32B'
    }
    try:
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"
        )
        data = r.json()

        city = data['name']
        cur_weather = data['main']['temp']

        weather_description = data['weather'][0]['main']
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = 'Посмотри в окно. Не пойму, что там за погода!'


        feels_like = data['main']['feels_like']
        humidity = data['main']['humidity']
        pressure = round(int(data['main']['pressure'])/1.333)
        wind_sp = data['wind']['speed']
        wind_dir = ('С' if data['wind']['deg'] <= 10 or data['wind']['deg'] >= 350 else 'В' if 80 <= data['wind']['deg'] <= 100
        else 'Ю' if 170 <= data['wind']['deg'] <= 190 else 'З' if 260 <= data['wind']['deg'] <= 280
        else 'С/В' if 10 < data['wind']['deg'] < 80 else 'Ю/В' if 100 < data['wind']['deg'] < 170
        else 'Ю/З' if 190 < data['wind']['deg'] < 260 else 'С/З' if 280 < data['wind']['deg'] < 350 else '')
        sunrise_timestamp = datetime.datetime.fromtimestamp(data['sys']['sunrise']).strftime("%H:%M:%S")
        sunset_timestamp = datetime.datetime.fromtimestamp(data['sys']['sunset']).strftime("%H:%M:%S")
        lenght_of_the_day = datetime.datetime.fromtimestamp(data['sys']['sunset']) - datetime.datetime.fromtimestamp(
            data['sys']['sunrise'])

        await message.reply(f'***{datetime.datetime.now().strftime("%d.%m.%Y %H:%M")}***\n'
              f'Погода в городе: {city}\nТемпература: {cur_weather} C° {wd}\nОщущается как: {feels_like} C°\n'
              f'Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст\nВетер: {wind_dir}, {wind_sp} м/с\n'
              f'Восход солнца: {sunrise_timestamp}\n'f'Заход солнца: {sunset_timestamp}\nПродолжительность дня: {lenght_of_the_day}\n' 
              f'***Хорошего дня!***'
              )

    except:
        await message.reply('\U00000620Проверьте правильность города\U00000620')


if __name__ == '__main__':
    executor.start_polling(dp)