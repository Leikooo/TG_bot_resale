# - *- coding: utf- 8 - *-
import asyncio
import datetime
import time

import requests
from aiogram import Dispatcher
# from bs4 import BeautifulSoup
from data.config import admins
from loader import bot
from utils.db_api.sqlite import *
import random
# Уведомление и проверка обновления при запуске скрипта
async def on_startup_notify(dp: Dispatcher):
    pass
    # if len(admins) >= 1:
    #     await send_all_admin(f"<b>✅ The bot was successfully launched</b>\n"
    #                             f"➖➖➖➖➖➖➖➖➖➖\n"
    #                             f"{bot_description}")

# Рассылка сообщения всем администраторам
async def send_all_admin(message, markup=None, not_me=0):
    if markup is None:
        for admin in admins:
            try:
                if str(admin) != str(not_me):
                    await bot.send_message(admin, message, disable_web_page_preview=True)
            except:
                pass
    else:
        for admin in admins:
            try:
                if str(admin) != str(not_me):
                    await bot.send_message(admin, message, reply_markup=markup, disable_web_page_preview=True)
            except:
                pass


# Очистка имени пользователя от тэгов
def clear_firstname(firstname):
    if "<" in firstname: firstname = firstname.replace("<", "*")
    if ">" in firstname: firstname = firstname.replace(">", "*")
    return firstname


# Проверка на обновление счётчика 24-х часов при запуске
def update_profit():
    settings = get_settingsx()
    now_unix = int(time.time())
    if now_unix - int(settings[4]) >= 86400:
        update_settingsx(profit_buy=now_unix)
    if now_unix - int(settings[5]) >= 86400:
        update_settingsx(profit_refill=now_unix)


# Автоматическая ежечасовая проверка на обновление счётчика 24-х часов
async def update_last_profit():
    while True:
        await asyncio.sleep(3600)
        settings = get_settingsx()
        now_unix = int(time.time())
        if now_unix - int(settings[4]) >= 86400:
            update_settingsx(profit_buy=now_unix)
        if now_unix - int(settings[5]) >= 86400:
            update_settingsx(profit_refill=now_unix)


# Получение текущей даты
def get_dates():
    return datetime.datetime.today().replace(microsecond=0)
