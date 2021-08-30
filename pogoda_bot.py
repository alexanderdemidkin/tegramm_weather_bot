import requests
import datetime
from telegram.ext import Updater
from telegram.ext import CommandHandler
import logging
from yaweather import YaWeather
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

'demi_ya_weather_bot'
tok = 'your token'


def help(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Прогноз погоды берет актуальную информацию с яндекс карт за текущий день.")
    context.bot.send_message(chat_id=update.effective_chat.id, text="y1 для просмотра информации о погоде в Нижнем Новгороде(yandex)")
    context.bot.send_message(chat_id=update.effective_chat.id, text="y2 для просмотра информации о погоде в Шацке(yandex)")
    context.bot.send_message(chat_id=update.effective_chat.id, text="y3 Для просмотра информации о погоде в Шарье(yandex)")
    context.bot.send_message(chat_id=update.effective_chat.id, text="o1 для просмотра информации о погоде в Нижнем Новгороде(openmap)")
    context.bot.send_message(chat_id=update.effective_chat.id, text="o2 для просмотра информации о погоде в Шацке(openmap)")
    context.bot.send_message(chat_id=update.effective_chat.id, text="o3 Для просмотра информации о погоде в Шарье(openmap)")


def nino1(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=ya_weather(1))

def sharya1(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=ya_weather(3))

def shack1(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=ya_weather(2))

def nino2(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=opweather(1))

def sharya2(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=opweather(3))

def shack2(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=opweather(2))

updater = Updater(token=tok, use_context=True)
help_handler = CommandHandler('help', help)
nino_handler1 = CommandHandler('y1', nino1)
shack_handler1 = CommandHandler('y2', shack1)
sharya_handler1 = CommandHandler('y3', sharya1)
nino_handler2 = CommandHandler('o1', nino2)
shack_handler2 = CommandHandler('o2', shack2)
sharya_handler2 = CommandHandler('o3', sharya2)
dispatcher = updater.dispatcher
dispatcher.add_handler(help_handler)
dispatcher.add_handler(nino_handler1)
dispatcher.add_handler(shack_handler1)
dispatcher.add_handler(sharya_handler1)
dispatcher.add_handler(nino_handler2)
dispatcher.add_handler(shack_handler2)
dispatcher.add_handler(sharya_handler2)
updater.start_polling()  # поехали!


def ya_weather(n):
    shack = (54.013406, 41.721666)
    nn = (56.284443, 44.039993)
    sharya = (58.389616, 45.493691)
    y = YaWeather(api_key='yandex_api_key')
    DESCRIPTION_DIC = {
        'clear': 'Ясно',
        'light-rain': 'Небольшой дождь',
        'partly-cloudy': 'Малооблачно',
        'cloudy': 'Облачно с прояснениями',
        'overcast': 'Пасмурно',
        'partly-cloudy-and-light-rain': 'Небольшой дождь',
        'partly-cloudy-and-rain': 'Дождь',
        'overcast-and-rain': 'Сильный дождь',
        'overcast-thunderstorms-with-rain': 'Сильный дождь, гроза',
        'cloudy-and-light-rain': 'Небольшой дождь',
        'overcast-and-light-rain': 'Небольшой дождь',
        'cloudy-and-rain': 'Дождь',
        'overcast-and-wet-snow': 'Дождь со снегом',
        'partly-cloudy-and-light-snow': 'Небольшой снег',
        'partly-cloudy-and-snow': 'Снег',
        'overcast-and-snow': 'Снегопад',
        'cloudy-and-light-snow': 'Небольшой снег',
        'overcast-and-light-snow': 'Небольшой снег',
        'cloudy-and-snow': 'Снег',
    }
    weath = ''
    city = nn
    if n == 1:
        city = nn
        weath += 'Погода(yandex) в Нижнем Новгороде \n '
    elif n == 2:
        city = shack
        weath += 'Погода(yandex) в Шацке \n '
    elif n == 3:
        city = sharya
        weath += 'Погода(yandex) в Шарье \n '

    res = y.forecast(city, lang='ru_RU')
    f1 = open("d:test.json",'w')
    f1.write(str(res))
    f1.close()
    a = []
    for el in res.forecasts[0].hours:
       l_time = datetime.datetime.utcfromtimestamp(int(el.hour_ts)) + datetime.timedelta(hours=3)
       if l_time > datetime.datetime.now():
           b = []
           b.extend([l_time,el.temp,el.feels_like,DESCRIPTION_DIC[el.condition],el.wind_speed,el.pressure_mm,el.humidity])
           a.append(b)

    print(a)

    for el in res.forecasts[1].hours:
        b = []
        l_time = datetime.datetime.utcfromtimestamp(int(el.hour_ts)) + datetime.timedelta(hours=3)
        b.extend([l_time, el.temp, el.feels_like, DESCRIPTION_DIC[el.condition], el.wind_speed, el.pressure_mm, el.humidity])
        a.append(b)

    weath += 'Текущая температура: ' + str(res.fact.temp) + '°C, ощущается как:' + str(res.fact.feels_like) + '°C, ' + DESCRIPTION_DIC[res.fact.condition] + ' \n '
    weath += 'ветер: ' + str(res.fact.wind_speed) + 'м\с, влажность: ' + str(res.fact.humidity) + '%, давление ' + str(res.fact.pressure_mm) + ' мм.рт.ст \n '
    for b in a:
        weath += str(b[0]) + ': температура: ' + str(b[1]) + '°C, ощущается как: ' + str(b[2]) + '°C, \n '
        weath += 'ветер: ' + str(b[4]) + ' м/с,  ' + str(b[3]) + ' \n '
    return weath

appid = "openweather_api"

def get_wind_direction(deg):
    l = ['С ','СВ',' В','ЮВ','Ю ','ЮЗ',' З','СЗ']
    for i in range(0,8):
        step = 45.
        min = i*step - 45/2.
        max = i*step + 45/2.
        if i == 0 and deg > 360-45/2.:
            deg = deg - 360
        if deg >= min and deg <= max:
            res = l[i]
            break
    return res

# Запрос текущей погоды
def request_current_weather(city_id):
    weath = ''
    res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                     params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
    data = res.json()
    weath += 'Текущая температура: ' + str(data['main']['temp'])[0:2] + '°C, ощущается как: ' + \
                 str(data['main'] ['feels_like'])[0:2] + '°C, ' + data['weather'][0]['description'] + ',  \n '
    weath += 'ветер: ' + str(data['wind']['speed']) + ' м\с ' +   get_wind_direction(data['wind']['deg']) + \
                 ', влажность: ' + str(format(data['main']['humidity'])) + '%, давление ' + str(int(data['main']['pressure'])/1.33324)[0:3] + ' мм.рт.ст \n '

    return weath


# Прогноз
def request_forecast(city_id):
    res = requests.get("http://api.openweathermap.org/data/2.5/forecast",
                           params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
    data = res.json()
    a = []
    for i in data['list']:
        b = []
        b.extend([str(i['dt_txt'])[:16], str(i['main']['temp'])[0:2],
                 str(i['main']['feels_like'])[0:2], i['weather'][0]['description'],
                  str(i['wind']['speed']), get_wind_direction(i['wind']['deg']),
                  str(format(i['main']['humidity'])), str(int(i['main']['pressure']) / 1.33324)[0:3]])
        a.append(b)

    weath = ''
    for b in a:
        weath += b[0] + ': температура: ' + b[1] + '°C, ощущается как: ' + b[2] + '°C, \n '
        weath += 'ветер: ' + b[4] + ' м/с ' + b[5] + ',  ' + str(b[3]) + ' \n '
    return weath

#city_id for SPb
nn = 520555
shatsk = 495532
sharya = 495619

def opweather(n):
    city_id = 520555
    st = ''
    if n == 1:
        city_id = 520555
        st += 'Погода(openmaps) в Нижнем Новгороде \n '
    elif n == 2:
        city_id = 495532
        st += 'Погода(openmaps) в Шацке \n '
    elif n == 3:
        city_id = 495619
        st += 'Погода(openmaps) в Шарье \n '

    st += str(request_current_weather(city_id))
    st += str(request_forecast(city_id))
    return st
