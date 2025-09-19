import json
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ChatMemberUpdated
from aiogram.types import InlineKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

with open('token.txt', 'r') as tokenfile:
    token = tokenfile.readline()

bot = Bot(token) 
dp = Dispatcher()

DB_FILE = 'users.json'
DB_FILE_GANGS = 'gangs.json'

def load_users():
    try:
        with open(DB_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_users(users):
    with open(DB_FILE, 'w') as f:
        json.dump(users, f, indent=4)

def load_gangs():
    try:
        with open(DB_FILE_GANGS, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_gangs(gangs):
    with open(DB_FILE_GANGS, 'w') as f:
        json.dump(gangs, f, indent=4)

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    user_id = str(message.from_user.id)
    users = load_users()
    
    if user_id not in users:
        users[user_id] = {'gang': None}
        save_users(users)

    await message.answer(
        "Привет! Я бот для поиска команды от Киберполигона.\n"
        "\n"
        "Используйте команды:\n\n"
        "/find - зарегистрироваться в команду\n\n"
        "'/find_duo username1' -\nзарегистрироваться вдвоем\n\n"
        "'/find_trio username1 username2' -\nзарегистрироваться втроем\n\n"
        "/status - показать информацию о команде"
    )

@dp.message(Command("find"))
async def cmd_start(message: types.Message):
    user_id = str(message.from_user.id)
    user_name = str(message.from_user.username)
    users = load_users()
    gangs = load_gangs()
    
    if users[user_id]['gang'] == None:
        lengang = len(gangs)
        mingang = -1
        
        for i in gangs:
            if len(gangs[i]) < 4: # Если команды на другое количество участников, поменять число 4"
                mingang = i
                break
        
        if mingang == -1:
            mingang = lengang

        if len(gangs) == 0:
            gangs['0'] = [user_name + ' ' + user_id]
            save_gangs(gangs)

        elif int(mingang) < int(lengang):
            gangs[str(mingang)].append(user_name + ' ' + user_id)
            save_gangs(gangs)

        else:
            gangs[str(lengang)] = [user_name + ' ' + user_id]
            save_gangs(gangs)

        users[user_id] = {'gang': str(mingang)}
        save_users(users)
        await message.answer("Вы зарегистрированы в команду")
    
    else:
        await message.answer(
            "Вы уже зарегистрированы"
        )

@dp.message(Command("find_duo"))
async def cmd_start(message: types.Message):
    msg = str(message.text).split()
    msg.remove(msg[0])

    if len(msg) == 0:
        await message.answer("Отсутсвуют аргументы")

    else:
        msg = msg[0]

        user_id = str(message.from_user.id)
        user_name = str(message.from_user.username)
        users = load_users()
        gangs = load_gangs()

        if msg[0] == '@':
            msg = msg[1:]
        if 'https://t.me/' in msg:
            msg = msg[13:]

        if users[user_id]['gang'] == None:
            lengang = len(gangs)
            mingang = -1
            
            for i in gangs:
                if len(gangs[i]) < 3: # Если команды на другое количество участников, поменять число "3"
                    mingang = i
                    break
            
            if mingang == -1:
                mingang = lengang

            if len(gangs) == 0:
                gangs['0'] = [user_name + ' ' + user_id]
                save_gangs(gangs)

            elif int(mingang) < int(lengang):
                gangs[str(mingang)].append(user_name + ' ' + user_id)
                gangs[str(mingang)].append(msg)
                save_gangs(gangs)

            else:
                gangs[str(lengang)] = [user_name + ' ' + user_id]
                gangs[str(lengang)].append(msg)
                save_gangs(gangs)

            users[user_id] = {'gang': str(mingang)}
            save_users(users)
            await message.answer("Вы зарегистрированы в команду")
        
        else:
            await message.answer(
                "Вы уже зарегистрированы"
            )
    
@dp.message(Command("find_trio"))
async def cmd_start(message: types.Message):
    msg = str(message.text).split()
    msg.remove(msg[0])

    if len(msg) == 0:
        await message.answer("Отсутсвуют аргументы")

    else:
        user_id = str(message.from_user.id)
        user_name = str(message.from_user.username)
        users = load_users()
        gangs = load_gangs()
        

        if msg[0][0] == '@':
            msg[0] = msg[0][1:]
        if 'https://t.me/' in msg[0]:
            msg[0] = msg[0][13:]
        
        if msg[1][0] == '@':
            msg[1] = msg[1][1:]
        if 'https://t.me/' in msg[1]:
            msg[1] = msg[1][13:]

        if users[user_id]['gang'] == None:
            lengang = len(gangs)
            mingang = -1
            
            for i in gangs:
                if len(gangs[i]) < 2: # Если команды на другое количество участников, поменять число "2"
                    mingang = i
                    break
            
            if mingang == -1:
                mingang = lengang

            if len(gangs) == 0:
                gangs['0'] = [user_name + ' ' + user_id]
                save_gangs(gangs)

            elif int(mingang) < int(lengang):
                gangs[str(mingang)].append(user_name + ' ' + user_id)
                gangs[str(mingang)].append(msg[0])
                gangs[str(mingang)].append(msg[1])
                save_gangs(gangs)

            else:
                gangs[str(lengang)] = [user_name + ' ' + user_id]
                gangs[str(lengang)].append(msg[0])
                gangs[str(lengang)].append(msg[1])
                save_gangs(gangs)

            users[user_id] = {'gang': str(mingang)}
            save_users(users)
            await message.answer("Вы зарегистрированы в команду")
        
        else:
            await message.answer(
                "Вы уже зарегистрированы"
            )

@dp.message(Command("status"))
async def cmd_start(message: types.Message):
    user_id = str(message.from_user.id)
    user_name = str(message.from_user.username)
    users = load_users()
    gangs = load_gangs()
    mygang_number = users[user_id]["gang"]

    try:
        if len(gangs[mygang_number]) != 1:
            mygang_usernames = []
            for i in gangs[mygang_number]:
                mygang_usernames.append(i.split()[0])
            mygang_usernames.remove(user_name)
            await message.answer('Ваша команда:', reply_markup=ease_link_kb(mygang_usernames))
    
    except:
        await message.answer('В команде пока нет других пользователей')

def ease_link_kb(mygang_usernames):
    inline_kb_list = []
    for i in mygang_usernames:
        inline_kb_list.append([InlineKeyboardButton(text=i, url='t.me/' + i)])
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)

async def main():    
    await dp.start_polling(bot)
    
if __name__ == '__main__':
    asyncio.run(main())