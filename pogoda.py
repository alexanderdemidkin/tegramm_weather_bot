import requests
from bs4 import BeautifulSoup
from telegram.ext import Updater    
from telegram.ext import CommandHandler
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


tok = 'your token'

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, 
        text="Начинаем работу бота. Выберите нужную команду: /1 /2 /3 или /help для помощи")

def help(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Прогноз погоды берет актуальную информацию с яндекс карт за текущий день.")
    context.bot.send_message(chat_id=update.effective_chat.id, text="1 для просмотра информации о погоде в Нижнем Новгороде(Кузнечиха)")
    context.bot.send_message(chat_id=update.effective_chat.id, text="2 для просмотра информации о погоде в Шацке(Черная слобода)")
    context.bot.send_message(chat_id=update.effective_chat.id, text="3 Для просмотра информации о погоде в Шарье(Алешунино)")

def nino(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=ya_weather(1))

def sharya(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=ya_weather(3))

def shack(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=ya_weather(2))

updater = Updater(token=tok, use_context=True)
start_handler = CommandHandler('start', start)
help_handler = CommandHandler('help', help)
nino_handler = CommandHandler('1',nino)
shack_handler = CommandHandler('2',shack)
sharya_handler = CommandHandler('3',sharya)
dispatcher = updater.dispatcher
dispatcher.add_handler(start_handler)
dispatcher.add_handler(help_handler)
dispatcher.add_handler(nino_handler)
dispatcher.add_handler(shack_handler)
dispatcher.add_handler(sharya_handler)
updater.start_polling()  # поехали!


def ya_weather(pos):
    st = ''
    url = "https://yandex.ru/pogoda/116675"
    url1 = "https://yandex.ru/pogoda/137477"
    url2 = "https://yandex.ru/pogoda/?lat=58.39247131&lon=45.49722672"
    if pos == 1:
        response = requests.get(url)
    elif pos == 2:
        response = requests.get(url1)
    elif pos == 3:
        response = requests.get(url1)
    soup = BeautifulSoup(response.text,'lxml')
    cur_temp = soup.find('div', class_='fact__temp').text
    cloudly = soup.find('div',class_= 'day-anchor').text
    fill_temp = soup.find('div',class_= 'fact__feels-like').text
    wind = soup.find('div',class_= 'fact__wind-speed').text
    humidity = soup.find('div',class_= 'fact__humidity').text
    pressure = soup.find('div',class_= 'fact__pressure').text
    rainfall = soup.find('p',class_= 'maps-widget-fact__title').text
    quotes7 = soup.find_all('span',class_= 'fact__hour-elem',recursive=True)
    list_hour_temp = [x.text for x in quotes7]
    st += str(cur_temp[0:20]) + ': ' + str(cur_temp[20:25]) + '\n'
    st += str(fill_temp[0:14]) + ': ' + str(fill_temp[14:18]) + '\n'
    st +=str(cloudly) + '\n'
    st +='Ветер: ' + str(wind) + '\n'
    st +='Влажность: ' + str(humidity) + '\n'
    st +='Давление: ' + str(pressure) + '\n'
    st +=str(rainfall) + '\n'
    st += "Погода по часам: \n"
    for hour_temp in list_hour_temp:
        if hour_temp.find('°') != -1 :
            st += str(hour_temp[0:5]) + ': ' + str(hour_temp[5:12]) + '\n'
    return st


