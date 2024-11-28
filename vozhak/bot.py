import logging
import sqlite3
import asyncio
import time as t
import requests
import base64
import json
from telegram import *
from threading import Timer
import sqlite3
from telegram.error import *
from telegram.ext import *
from datetime import *
from telethon import TelegramClient
from telegram.error import TelegramError
from telegram.constants import UpdateType, ParseMode
from telethon.tl.functions.messages import GetMessagesReactionsRequest
from telethon.tl.types import InputPeerChannel, InputPeerUser

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
array_message = [-1002424140672,-1002369574391,-1002422931787,-1002385442088,-1002316623832,-1002328564507,-1002298382107]
logger = logging.getLogger(__name__)
bot_token =  '7404457828:AAHIo1qBuKlBvEZ5AQAi3JFe9WsB5FmNcEQ'
conn = sqlite3.connect('teams.db', check_same_thread=False)
cursor = conn.cursor()
# Создаем клиента
master_classes = {}
user_registrations = {}
players = []
waiting_game = {}
game_chats = [-1002498876619, -4564472209, -4517693420,-4581338414,-4550254545,-4505419264,-4586885712,-4597880004,-4591307105,-4541738040]
# Словарь для хранения игр
games = {}

# Словарь для хранения сообщений с кнопками
room_messages = {}
my_id = "6033842569"
array_id=[13,50,13,15,15,8,8]
putevki='-1002373983158'
id_put = '6'
rooms_id=[]
products = [
    {
        "id": 1,
        "name": "Вадим",
        "price": 200,
        "description": "Активчик, был в этом лагере уже 10 раз. Его знают все – админка и вожатые. С ним никогда не было проблем, каждый раз его ставили командиром отряда, не давая другим детям попробовать себя на этой должности.",
        "image": "1.jpg"
    },
    {
        "id": 2,
        "name": "Елисей",
        "price": 250,
        "description": "Этот ребёнок всегда улыбается и заряжает всех вокруг своим позитивом. Он любит шутить и веселиться, а его смех слышен даже на самых отдалённых уголках лагеря.",
        "image": "2.jpg"
    },
    {
        "id": 3,
        "name": "Анастасия",
        "price": 150,
        "description": "Этот ребёнок не признаёт никаких правил и ограничений. Он всегда делает то, что хочет, и не слушает никого. Его свободолюбивый характер вызывает восхищение у других детей, но иногда его действия могут привести к неприятностям",
        "image": "3.jpg"
    },
    {
        "id": 4,
        "name": "Владимир",
        "price": 100,
        "description": "Его талант к рисованию поражает всех. Он создаёт удивительные картины, которые украшают стены лагеря и радуют глаз каждого, кто их видит.",
        "image": "4.jpg"
    },
    {
        "id": 5,
        "name": "Оксана",
        "price": 130,
        "description": "Она всегда в центре внимания и любит привлекать к себе взгляды окружающих. Её актёрские способности позволяют ей легко вживаться в любую роль и создавать неповторимые образы",
        "image": "5.jpg"
    },
    {
        "id": 6,
        "name": "Екатерина",
        "price": 140,
        "description": "Эта девочка — настоящая спортсменка. Она участвует во всех спортивных мероприятиях лагеря и всегда стремится к победе. Её сила и выносливость вызывают восхищение у других детей.",
        "image": "6.jpg"
    },
    {
        "id": 7,
        "name": "Михаил",
        "price": 180,
        "description": "Он проводит большую часть времени за чтением книг. Его знания о мире литературы поражают даже самых опытных библиотекарей",
        "image": "7.jpg"
    },
    {
        "id": 8,
        "name": "Николай",
        "price": 170,
        "description": "У него есть свой инструмент, на котором он играет с большим мастерством. Его музыка наполняет лагерь радостью и вдохновением",
        "image": "8.jpg"
    },
{
        "id": 9,
        "name": "Артемий",
        "price": 220,
        "description": "Никто не знает, откуда он пришёл и что скрывает. Он предпочитает держаться в стороне от остальных детей и проводить время в одиночестве",
        "image": "9.jpg"
    },
    {
        "id": 10,
        "name": "Мария",
        "price": 230,
        "description": "Она всегда готова взять на себя ответственность и помочь другим. Ее лидерские качества делают его отличным кандидатом на должность командира отряда",
        "image": "10.jpg"
    },
    {
        "id": 11,
        "name": "Ангелина",
        "price": 200,
        "description": "Она часто погружается в свои мысли и мечты. Ее воображение позволяет ей создавать удивительные истории и миры",
        "image": "11.jpg"
    },
    {
        "id": 12,
        "name": "Семен",
        "price": 250,
        "description": "Он умеет петь, танцевать и играть на нескольких инструментах. Его выступления на сцене становятся настоящим праздником для всего лагеря",
        "image": "12.jpg"
    },
    {
        "id": 13,
        "name": "Аркадий",
        "price": 150,
        "description": "Ему нравится изучать новые места и открывать для себя что-то новое. Его любознательность и жажда знаний делают его интересным собеседником",
        "image": "13.jpg"
    },
    {
        "id": 14,
        "name": "Игорь",
        "price": 100,
        "description": "Он любит шутить и веселиться, но иногда его шутки могут быть не совсем безобидными. Он может подшутить над друзьями или вожатыми, но делает это без злого умысла",
        "image": "14.jpg"
    },
    {
        "id": 15,
        "name": "Алексей",
        "price": 130,
        "description": "Этот ребёнок постоянно в движении. Ему сложно усидеть на месте, и он всегда ищет новые приключения. Иногда он может создавать проблемы, но его энергия и жизнерадостность делают его любимцем лагеря",
        "image": "15.jpg"
    },
    {
        "id": 16,
        "name": "Ксения",
        "price": 140,
        "description": "Он очень ответственный и организованный, всегда следует правилам и инструкциям. Иногда его педантичность может раздражать других детей, но он всегда готов помочь и поддержать",
        "image": "16.jpg"
    },
    {
        "id": 17,
        "name": "София",
        "price": 180,
        "description": "Он редко говорит и предпочитает проводить время в одиночестве. Но когда он всё же открывает рот, его слова оказываются мудрыми и глубокими. Его молчаливость создаёт вокруг него атмосферу загадочности",
        "image": "17.jpg"
    },
    {
        "id": 18,
        "name": "Иван",
        "price": 170,
        "description": "Ему нравится испытывать себя и свои возможности. Он часто участвует в экстремальных мероприятиях и соревнованиях, что вызывает восхищение у других детей. Однако его безрассудство иногда приводит к неприятностям",
        "image": "18.jpg"
    },
    {
        "id": 19,
        "name": "Максим",
        "price": 220,
        "description": "Он всегда сомневается в том, что говорят другие. Он любит задавать вопросы и искать доказательства, прежде чем поверить во что-то. Его скептицизм может быть полезным, но иногда он мешает ему наслаждаться жизнью",
        "image": "19.jpg"
    },
    {
        "id": 20,
        "name": "Руслан",
        "price": 230,
        "description": "Иногда он может делать мелкие пакости другим детям или вожатым. Он не делает этого со злым умыслом, а скорее из любопытства или желания повеселиться. Однако его действия могут вызывать раздражение у окружающих",
        "image": "20.jpg"
    },
    {
        "id": 21,
        "name": "Маргарита",
        "price": 200,
        "description": "Этот ребенок любит прятаться и играть в прятки. Его навыки маскировки поражают даже самых опытных вожатых. Он может спрятаться так, что его не найдут даже с собаками",
        "image": "21.jpg"
    },
    {
        "id": 22,
        "name": "Дарья",
        "price": 250,
        "description": "Этот ребёнок всегда выглядит сонным и уставшим. Он часто засыпает на ходу и может проспать всё самое интересное. Но когда он бодрствует, он становится очень весёлым и активным",
        "image": "22.jpg"
    },
    {
        "id": 23,
        "name": "Елизавета",
        "price": 150,
        "description": "Этого ребёнка можно назвать тёмной лошадкой, потому что никто не может предсказать, как он поведёт себя в следующий момент. Он может быть весёлым и дружелюбным, а может внезапно стать замкнутым и агрессивным. Иногда он проявляет интерес к каким-то занятиям, но быстро теряет к ним интерес. Все надеются, что со временем смогут лучше понять этого ребёнка и помочь ему раскрыться.",
        "image": "23.jpg"
    },
    {
        "id": 24,
        "name": "Лев",
        "price": 100,
        "description": "Он всегда в центре внимания и любит быть лидером. Он умеет организовывать мероприятия и вовлекать других детей в игры и развлечения. Однако иногда его активность может перерасти в навязчивость",
        "image": "24.jpg"
    },
    {
        "id": 25,
        "name": "Ростислав",
        "price": 130,
        "description": "Он часто погружается в свои мысли и мечты. Его воображение позволяет ему создавать удивительные истории и миры. Иногда он может настолько погрузиться в свои фантазии, что забывает о реальности",
        "image": "25.jpg"
    },
    {
        "id": 26,
        "name": "Евгений",
        "price": 140,
        "description": "Ему сложно ждать и терпеть. Он всегда хочет получить всё и сразу. Его нетерпение может вызывать раздражение у других детей, но его энергия и энтузиазм делают его интересным собеседником",
        "image": "26.jpg"
    },
    {
        "id": 27,
        "name": "Александр",
        "price": 180,
        "description": "Он может починить всё что угодно: от сломанного стула до неработающего телевизора. Его навыки в области техники и механики делают его незаменимым помощником для вожатых и администрации лагеря. Он всегда готов прийти на помощь и решить любую проблему",
        "image": "27.jpg"
    },
    {
        "id": 28,
        "name": "Семен",
        "price": 170,
        "description": "Этот ребёнок обожает проводить время на свежем воздухе и изучать природу. Он знает все растения и животных, которые обитают в окрестностях лагеря, и с удовольствием рассказывает о них другим детям. Его любовь к природе делает его отличным компаньоном для прогулок и походов",
        "image": "28.jpg"
    },
    {
        "id": 29,
        "name": "Яна",
        "price": 220,
        "description": "У этого ребёнка есть настоящий талант в какой-то области. Может быть, это рисование, музыка, танцы или что-то ещё. Его талант вызывает восхищение у других детей, и они с радостью наблюдают за его выступлениями и работами",
        "image": "29.jpg"
    },
    {
        "id": 30,
        "name": "Жанна",
        "price": 230,
        "description": "Никто не знает, откуда он пришёл и что скрывает. Он предпочитает держаться в стороне от остальных детей и проводить время в одиночестве. Иногда он может показаться грустным и задумчивым, но никто не знает, что происходит у него в голове",
        "image": "30.jpg"
    }
]
products_ids = {}
message_buy_id = ''

def check_balance(user_id, price):

    cursor.execute('SELECT team FROM users WHERE username = ?', (user_id,))
    team_id = cursor.fetchone()[0]
    cursor.execute('SELECT balance FROM team WHERE id = ?', (team_id,))
    bal = cursor.fetchone()[0]

    if price <= bal:
        cursor.execute('UPDATE team SET balance = balance - ? WHERE id = ?', (price, team_id))
        conn.commit()
        return True
    else:
        return False



async def pstart(update: Update, context: CallbackContext) -> None:
    for product in products:
        with open(f'photos/{product["image"]}', 'rb') as photo_file:
            try:
                await asyncio.sleep(5)
                keyboard = [
                    [InlineKeyboardButton(text=f"Оплатить путевку для {product['name']}", callback_data=f"buy_{product['name']}")]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                message = await context.bot.send_photo(
                    chat_id=update.effective_chat.id,
                    photo=photo_file,
                    message_thread_id=6,
                    caption=f"Имя: {product['name']}\nХарактеристика: {product['description']}\nСтоимость путевки: {product['price']}",
                    reply_markup=reply_markup,
                )
                products_ids[product['name']] = message.message_id
            except Exception as e:
                print(f"Error sending product photo: {e}")


mk_to_id = {}
mk_id = {}
async def check_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global master_classes
    args = context.args
    if len(args) < 2:
        await update.message.reply_text('Используйте /mk "кол-во людей" "Название"')
        return

    try:
        places = int(args[0])
        name = ' '.join(args[1:])
    except ValueError:
        await update.message.reply_text('Неверный формат количества мест. Используйте /mk "кол-во людей" "Название"')
        return

    if places <= 0:
        await update.message.reply_text('Количество мест должно быть больше нуля.')
        return

    # Use the full name to create the master class entry
    if name == '':
        times = ["10:30", "13:40", "15:10"]
    elif name == '':
        times = ["13:40"]
    else:
        times = ["10:30", "13:40", "15:10"]
    master_classes[name] = {'places': {time: places for time in times}, 'users': {time: [] for time in times}, 'id': 0}
    reply_markup = register(name)

    message = await context.bot.send_message(chat_id="-1002373983158",
                text=f'Спикер: <b><i>{name}</i></b>\nНазвание: <i>{name}</i>',parse_mode=ParseMode.HTML, message_thread_id=919, reply_markup=reply_markup)
    mk_to_id[name] = message.message_id

master_class_mapping = {
    'Напарничество: взгляд сверху': 'np1',
    'Как научиться управлять привычками, которые управляют нами': 'np2',
    'Исповедь училок или 10 причин почему ты плохой вожатый': 'np3',
    'Как генерировать людей без 6 пальца или краткий экскурс в мир AI': 'np4',
    'Какие вопросы задать вселенной, чтобы написать актуальную программу смены? И как исправить все, если вдруг что-то пошло не по плану': 'np5',
    'От слез к улыбкам: секреты создания атмосферы в лагере': 'np6',
    'Вожатый тоже актёр': 'np7',
    'Креативный контент от паблика «Вожатник»': 'np8',
    'Театр Теней': 'tt1',
    'Нейровожатый': 'nv1',
    'Зины': 'zn1',
    'Медиа и цифровизация': 'md1',
    'Объединяй вдохновением': 'oi1',
    'Ненасильственное общение: от напарничества к единству': 'no1',
    'Мк по созданию настольных игр': 'ng1',
    'Лови Момент': 'lm1',
    'Ораторское искусство': 'oi2',
    'Вожатник': 'vg1',
    'Дождь мне нашептал': 'dn1',
    'Создание гимна: от идеии до реализации': 'sg1',
    'Я - новый Пикассо': 'np9',
    'Пресс-центр': 'pc1',
    'Визуальные чтения': 'vc1'
}


master_class_author = {
    'Напарничество: взгляд сверху': 'np1',
    'Как научиться управлять привычками, которые управляют нами': 'np2',
    'Исповедь училок или 10 причин почему ты плохой вожатый': 'np3',
    'Как генерировать людей без 6 пальца или краткий экскурс в мир AI': 'np4',
    'Какие вопросы задать вселенной, чтобы написать актуальную программу смены? И как исправить все, если вдруг что-то пошло не по плану': 'np5',
    'От слез к улыбкам: секреты создания атмосферы в лагере': 'np6',
    'Вожатый тоже актёр': 'np7',
    'Креативный контент от паблика «Вожатник»': 'np8',
}

def register(name):
    if name == 'Креативный контент от паблика «Вожатник':
        times = ["10:30", "15:10"]
    elif name == 'Напарничество: взгляд сверху':
        times = ["13:40"]
    else:
        times = ["10:30", "13:40", "15:10"]
    keyboard = []
    for time in times:
        if master_clas[name]['places'][time] > 0:
            # Use the shorter identifier from the mapping
            short_name = master_class_mapping.get(name, name)
            callback_data = f"register_{short_name}_{time}"
            # Ensure callback_data is within the allowed length
            if len(callback_data.encode('utf-8')) > 64:
                logger.error(f"Callback data too long: {callback_data}")
                continue
            keyboard.append([InlineKeyboardButton(
                f"Записаться в {time}\n Мест: {master_clas[name]['places'][time]}",
                callback_data=callback_data
            )])
    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup

messages_storage = {}
async def handle_messages(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.message_thread_id == 4:
        print("yes")
        message_id = update.message.message_id
        if message_id not in messages_storage:
            messages_storage[message_id] = update.message

async def get_reactions(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message_reaction:
        print("Received a reaction")
        message_id = update.message_reaction.message_id
        user_id = update.message_reaction.user.id
        username = update.message_reaction.user.username

        old_reaction = update.message_reaction.old_reaction
        new_reaction = update.message_reaction.new_reaction

        print(f"Message ID: {message_id}, User ID: {user_id}, Username: {username}, Old Reaction: {old_reaction}, New Reaction: {new_reaction}")

        if message_id in messages_storage:
            cursor.execute('SELECT team FROM users WHERE username = ?', (username,))
            team_id = cursor.fetchone()
            if team_id is None:
                print(f"No team found for user ID: {user_id}")
                return
            team_id = team_id[0]

            if new_reaction and not old_reaction:
                cursor.execute('UPDATE team SET balance = balance + 5 WHERE id = ?', (team_id,))
                print(f"Added 5 to team {team_id}'s balance")
            elif old_reaction and not new_reaction:
                cursor.execute('UPDATE team SET balance = balance - 5 WHERE id = ?', (team_id,))
                print(f"Subtracted 5 from team {team_id}'s balance")

            conn.commit()
            chat = array_message[team_id - 1]

            cursor.execute('SELECT balance FROM team WHERE id = ?', (team_id,))
            balance = cursor.fetchone()
            if balance is None:
                print(f"No balance found for team ID: {team_id}")
                return
            balance = balance[0]
            id = array_id[team_id - 1]
            await context.bot.edit_message_text(chat_id=chat, message_id=id, text=f'Баланс вашей команды: {balance}')
async def handle_dice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    dice = update.message.dice
    user_id = update.message.from_user.id
    username = update.message.from_user.username
    cursor.execute('SELECT team FROM users WHERE username = ?', (username,))
    team_id = cursor.fetchone()[0]
    cursor.execute('SELECT balance FROM team WHERE id = ?', (team_id,))
    current_balance = cursor.fetchone()[0]
    cursor.execute('SELECT last_reward_time FROM team WHERE id = ?', (team_id,))
    last_reward_time_str = cursor.fetchone()[0]
    last_reward_time = datetime.strptime(last_reward_time_str, '%Y-%m-%d %H:%M:%S') if last_reward_time_str else None

    if last_reward_time and datetime.now() - last_reward_time < timedelta(hours=4):
        await context.bot.send_message(chat_id=update.effective_chat.id, text='Часики еще не дотикали')
        return

    if dice.emoji == '🎲':
        if dice.value == 1:
            new_balance = current_balance + 5
            if new_balance < 0: new_balance = 0
            mess = f'Вам выпало число 1! Вы получаете 5 вожиков!'
        elif dice.value == 2:
            new_balance = current_balance + 10
            mess = f'Вам выпало число 2! Вы получаете 10 вожиков!'
        elif dice.value == 3:
            new_balance = current_balance + 15
            mess = f'Вам выпало число 3! Вы получаете 15 вожиков!'
        elif dice.value == 4:
            new_balance = current_balance + 20
            mess = f'Вам выпало число 4! Вы получаете 20 вожиков!'
        elif dice.value == 5:
            new_balance = current_balance + 25
        elif dice.value == 6:
            new_balance = current_balance + 30
            mess = f'Вам выпало число 6! Вы получаете 30 вожиков!'
        cursor.execute('UPDATE team SET balance=?,last_reward_time = ? WHERE id = ?', (new_balance, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), team_id))
        conn.commit()
        chat = array_message[team_id - 1]
        await context.bot.send_message(chat_id=chat, text=mess)
        id = array_id[team_id - 1]
        await context.bot.edit_message_text(chat_id=chat, message_id=id, text=f'Баланс вашей команды: {new_balance}')

async def unban(update: Update,context)-> None:
    await context.bot.unban_chat_member(chat_id=game_chats[0], user_id=391743540)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="123")

async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    if update.effective_chat.type != 'private':
        await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.message.message_id)
    if user_id in [391743540, 390561523, 6755435741, 6033842569]:
        args = context.args
        if len(args) != 2:
            await context.bot.send_message(chat_id=update.effective_chat.id, text='Используйте команду в формате: /balance "номер команды" "число"')
            return

        target_team = int(args[0])
        try:
            amount = int(args[1])
        except ValueError:
            await context.bot.send_message(chat_id=update.effective_chat.id, text='Пожалуйста, введите корректное число.')
            return

        cursor.execute('SELECT balance FROM team WHERE id = ?', (target_team,))
        existing_user = cursor.fetchone()

        if not existing_user:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f'Команда номер {target_team} не найдена в базе данных.')
            return

        cursor.execute('UPDATE team SET balance = balance + ? WHERE id = ?', (amount, target_team))
        conn.commit()
        cursor.execute('SELECT balance FROM team WHERE id = ?', (target_team,))
        bal = cursor.fetchone()[0]
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f'Команде номер {target_team} было начислено {amount} вожиков.')
        chat = array_message[target_team - 1]
        id = array_id[target_team -1]
        await context.bot.edit_message_text(chat_id=chat, message_id=id, text=f'Баланс вашей команды: {bal}')
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Нет доступа к этой команде!")

master_classes_data = [
    {
        'name': 'Театр Теней',
        'team': 'Kid.Team',
        'desc': 'На нашем мк вы сможете познакомиться с искусством театра теней. На нем вы сможете увидеть представление, узнать о том, на сколько полезен может быть театр теней в лагере, а также получите возможность самостоятельно создать декорации и собрать их в собственное представление!',
        'number': 6,
        'queue': 1
    },{
        'name': 'Медиа и цифровизация',
        'team': 'ПОПЧ',
        'desc': 'Бу! Испугался? Не бойся, это Медиа и цифровизация #ПОПЧ! На мастер-классе мы расскажем про дизайн для тех, кто давно хотел научиться качественно и быстро работать в figma! Про то, как nfc-метки могут обогатить ваше взаимодействие с детьми и сделать мероприятия интереснее. Погружение в цифровизацию начнется совсем скоро!',
        'number': 15,
        'queue': 1
    },{
        'name': 'Вожатник',
        'team': 'Многогранник',
        'desc': 'Мастер-класс по созданию сценического выступления вожатых. Расскажем тонкости и сложности масштабных выступлений вожатых на сцене. Проблемы и их решения, которые могут при этом возникать.',
        'number': 15,
        'queue': 1
    },{
        'name': 'Дождь мне нашептал',
        'team': 'Big Family',
        'desc': 'На мастер-классе вожатская команда «Big family» поделится секретами создания волшебной атмосферы на вечерних сборах с использованием уникальной атрибутики и погрузит участников в атмосферу музыкального огонька, где звуки природы и мелодии вселяют в сердце ощущение магии. Каждый из участников научится создавать инструмент, который зажжет огонь в сердцах детей во время вечернего сбора. А также рассмотрим концепцию саундхилинга и его влияние на снятие эмоционального напряжения. Ждем по одному человеку от вашего педагогического отряда!',
        'number': 10,
        'queue': 1
    },{
        'name': 'Мк по созданию настольных игр',
        'team': 'Добро',
        'desc': 'Твори, чувствуй и играй! 🦄🎲\nПО «Добро» приглашает в свою игровую комнату, чтобы погрузить вас в мир создания настольных игр!\nЭти знания вы сможете использовать не только в личной жизни, но и на работе в лагере. \nМы предоставим вам возможность познакомиться с тонкостями создания игр, поделимся известными механиками и нашими личными лайфхаками. 🤫 \nС нами вы научитесь делать игры для детей любого возраста, попытаетесь создать собственную прямо во время мастер-класса, а ещё сможете попробовать угощения, которые мы для вас приготовили.😋💜\nБудем ждать вас на мастер-классе!',
        'number': 10,
        'queue': 1
    },{
        'name': 'Я - новый Пикассо',
        'team': 'Сила',
        'desc': 'Всем известен почерк великого Пикассо, а если нет - не страшно! На нашем Мастер Классе будет возможность сделать для себя или своего близкого портрет собственным руками! Тебе будут предоставлены буквально сотни вариантов разных форм частей лица, из которых ты сможешь собрать что-то индивидуальное - то, как именно ты видишь человека! В конечном результате получится безумно яркий и креативный автопортрет/портрет своего друга или родственника, который позволит тебе подарить эмоции людям и погрузиться как в мир Пикассо, так и в воспоминания об этом мероприятии!',
        'number': 15,
        'queue': 1
    },
    {
        'name': 'Нейровожатый',
        'team': 'Атмосфера',
        'desc': 'Уникальный мастер-класс для вожатых и организаторов! Научим, как использовать нейросети для облегчения и улучшения лагерной деятельности. Участники узнают, как быстро генерировать контент, создавать сценарии для мероприятий, находить музыку и визуальные материалы с помощью искусственного интеллекта. Каждый сможет попробовать свои силы и получить полезные навыки для решения реальных задач лагеря. Практика, обратная связь и доступные бесплатные инструменты — всё это ждет вас на нашем МК!',
        'number': 20,
        'queue': 1
    },
    {
        'name': 'Зины',
        'team': 'Спарта',
        'desc': 'Зин (англ. «zine») — это независимое печатное издание или мини-журнал, самостоятельно напечатанный автором небольшим тиражом. По факту, малая форма самиздата, способ самовыражения. Зин может быть любого формата, из любого материала и любого содержания. Может быть в единственном экземпляре или выпущен целым тиражом. Сделан как на компьютере, так и в ручную (или комбинированной технике!).',
        'number': 9,
        'queue': 'X'
    },

    {
        'name': 'Объединяй вдохновением',
        'team': 'Вышка Детям',
        'desc': 'Всем привет! Мы понимаем, как важен обмен опытом, поэтому приглашаем вас на наш мастер-класс! Здесь вы сможете визуализировать свои сильные стороны и особенности вашего педагогического отряда. В итоге вы получите не просто мудборд, а ценную базу контактов для дальнейшего общения. Ждем по одному человеку от вашего педагогического отряда!',
        'number': 10,
        'queue': 2
    },
    {
        'name': 'Ненасильственное общение: от напарничества к единству',
        'team': 'Товарищ',
        'desc': 'Если хоть раз в вашей жизни при сближении с человеком в работе на просьбы отвечали грубостью, а потребности не замечали — значит, вы столкнулись с насилием. Разбираемся, как улучшить отношения с напарниками, отрядом или детьми, используя методы ненасильственного общения.',
        'number': 20,
        'queue': 'X'
    },

    {
        'name': 'Лови Момент',
        'team': 'Миллениум',
        'desc': '«Лови момент» — мастер-класс, где мы научимся превращать обычные повседневные кадры в приятные воспоминания! Будет полезно как для вожатых, так и для начинающих блогеров, которые хотели бы развить личный бренд. Мы ждём всех желающих, кто хотел бы освоить искусство видеоблогинга и научиться создавать качественный и интересный контент. Вы сможете применить полученные знания на практике и создать собственные видеокадры. Не упустите возможность поймать тот самый момент!',
        'number': 10,
        'queue': 2
    },
    {
        'name': 'Ораторское искусство',
        'team': 'Вертикаль',
        'desc': 'Всем привет! СПО Вертикаль приглашает Вас на мастер класс по ораторскому искусству. На нем мы расскажем о важности правильной речи, покажем несколько действенных упражнений. Так же вы поучаствуете в дебатах где попробуете свои навыки.',
        'number': 8,
        'queue': 'X'
    },


    {
        'name': 'Создание гимна: от идеии до реализации',
        'team': 'Рассвет',
        'desc': 'Научимся создавать гимн не только к образу вожатого, а к лагерю и педотряда! На мастер-классе напишем текст гимна для фестиваля "Вожак", подберем музыку и найдем идеальное сочетание слов и мелодий.',
        'number': 15,
        'queue': 2
    },

    {
        'name': 'Пресс-центр',
        'team': 'Мёд',
        'desc': '"Творческий подход вожатый использует во время написания мероприятия, для проведения самой восхитительной свечки, когда думает над новым КТД и… для создания самых крутых соцсетей своего педотряда👨🏼‍💻\nУже догадались, про что будет наш мастер-класс ?\nСкорее смотри и готовься развить в себе smm жилку 👇🏻💛\nПресс-центр: организация его работы  во время&вне смен  или «сколько человек стоит за красивой картинкой?»\nЗнакомство с трендами и то, как адаптировать их в вожатскую нишу\nВидео-форматы: да или нет?\n«Красивая картинка»: как, почему и для чего?"',
        'number': 25,
        'queue': 2
    },
    {
        'name': 'Визуальные чтения',
        'team': 'Enjoy Camp',
        'desc': 'Мы познакомим зрителей с уникальным форматом вечернего мероприятия, которое можно провести с детьми в рамках лагерной смены.\n\nЗрители погрузятся в удивительный мир литературы, где прямо на их глазах оживут герои рассказа. Каждый сможет на себе прочувствовать и окунуться в атмосферу творчества вместе с рассказчиком. \n\nВизуальные чтения:\n🔮 Открывают новые смыслы и тайны произведений\n🎶 Музыка наполняет атмосферу новыми эмоциями и раскрывает глубокие оттенки каждого рассказа\n🎨 Художники превращают текст в живые картины\n\n💬 Это шанс взглянуть на современную литературу с другой стороны, обсудить увиденное, поделиться впечатлениями и понять, как и зачем такой формат взаимодействия с детьми можно применять в лагерной среде.',
        'number': 20,
        'queue': 2
    }
]
master_clas = {}
async def po(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global master_clas

    # Подготавливаем данные для мастер-классов
    master_clas = {}

    for mc in master_classes_data:
        full_name = mc['name']
        team = mc['team']
        desc = mc['desc']
        queue = mc['queue']
        place = mc['number']

        # Определяем короткое имя из маппинга
        short_name = master_class_mapping.get(full_name, None)
        if not short_name:
            logger.error(f"Мастер-класс {full_name} не имеет сокращенного имени.")
            continue

        # Определяем время
        times = ["17:10"] if queue == 1 else ["18:00"]

        # Если команда еще не добавлена, создаем запись
        if team not in master_clas:
            master_clas[team] = {}

        # Добавляем мастер-класс в команду
        master_clas[team][short_name] = {
            'full_name': full_name,
            'places': {time: place for time in times},
            'users': {time: [] for time in times},
            'desc': desc,
        }

        # Создаем клавиатуру для записи
        reply_markup = create_register_keyboard(team, short_name, times)

        # Отправляем сообщение с форматированной информацией
        message = await context.bot.send_message(
            chat_id="-1002373983158",  # Замените на ваш ID чата
            text=(
                f"----------------------------------------------------------\n"
                f"<b>Организатор:</b> {team}\n\n"
                f"<b>Название:</b> {full_name}\n\n"
                f"<i>{desc}</i>"
            ),
            parse_mode=ParseMode.HTML,
            message_thread_id=919,  # Замените на нужный ID потока
            reply_markup=reply_markup
        )
        # Сохраняем ID сообщения для отслеживания (если требуется)
        mk_id[short_name] = message.message_id
        await asyncio.sleep(1)


def create_register_keyboard(team, short_name, times):
    keyboard = []
    for time in times:
        # Проверяем наличие мест
        if master_clas[team][short_name]['places'][time] > 0:
            callback_data = f"reg_{team}_{short_name}_{time}"
            if len(callback_data.encode('utf-8')) > 64:
                logger.error(f"Callback data too long: {callback_data}")
                continue
            keyboard.append([InlineKeyboardButton(
                f"Записаться в {time}\nМест: {master_clas[team][short_name]['places'][time]}",
                callback_data=callback_data
            )])
    return InlineKeyboardMarkup(keyboard)

class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)]  # 3x3 поле
        self.current_player = 'X'  # Начинает X
        self.players = []  # Список игроков
        self.player_ids = {'X': None, 'O': None}
        self.player_nicks = {'X': None, 'O': None} # Словарь, который связывает символ с ID игрока

    def add_player(self, player_id,player_nick):
        if len(self.players) < 2 and player_id not in self.players:
            if len(self.players) == 0:
                self.player_ids['X'] = player_id
                self.player_nicks['X'] = player_nick# Первому игроку даем символ X
            else:
                self.player_ids['O'] = player_id
                self.player_nicks['O'] = player_nick# Второму игроку даем символ O
            self.players.append(player_id)
            return True
        return False

    def make_move(self, position):
        if self.board[position] == ' ':
            self.board[position] = self.current_player
            return True
        return False

    def switch_player(self):
        self.current_player = 'O' if self.current_player == 'X' else 'X'

    def check_winner(self):
        winning_combinations = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # горизонтальные
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # вертикальные
            (0, 4, 8), (2, 4, 6)              # диагонали
        ]
        for a, b, c in winning_combinations:
            if self.board[a] == self.board[b] == self.board[c] != ' ':
                winner_symbol = self.board[a]
                loser_symbol = 'O' if winner_symbol == 'X' else 'X'
                return winner_symbol, loser_symbol  # Возвращаем символы победителя и проигравшего
        if ' ' not in self.board:
            return 'Draw', None  # Ничья, проигравшего нет
        return None, None  # Игра продолжается

    def get_board_str(self):
        return f"""
        {self.board[0]} | {self.board[1]} | {self.board[2]}
        ---------
        {self.board[3]} | {self.board[4]} | {self.board[5]}
        ---------
        {self.board[6]} | {self.board[7]} | {self.board[8]}
        """
def get_key_by_value(dictionary, value):
    for key, val in dictionary.items():
        if val == value:
            return key
    return None
async def handle_callback(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    user_id = query.from_user.id  # Get the user ID

    # Log the button data
    logger.info(f"User {user_id} clicked button with data: {query.data}")

    try:
        await query.answer()  # Acknowledge the callback query
    except BadRequest as e:
        logger.error(f"Error answering callback query: {e}")
        return

    # Split the callback data
    data = query.data.split("_")
    action, short_name, time = data[0], data[1], data[2]
    print()
    # Map the short name back to the full name


    if action == "register":
        name = get_key_by_value(master_class_mapping, short_name)
        if user_id in user_registrations:
            registered_time = user_registrations[user_id].get(name)
            if registered_time:
                try:
                    await query.answer(
                        text=f'Вы уже записаны на: {name} в {registered_time}',
                        show_alert=True  # Display as a pop-up alert
                    )
                except BadRequest as e:
                    logger.error(f"Error answering callback query: {e}")
                return  # Exit if the user is already registered for this time

        # Check if the user is registered for another master class at the same time
        if user_id in user_registrations:
            for mc_name, mc_time in user_registrations[user_id].items():
                if mc_time == time:
                    try:
                        await query.answer(
                            text=f'Вы уже записаны на: {mc_name} в {mc_time}',
                            show_alert=True  # Display as a pop-up alert
                        )
                    except BadRequest as e:
                        logger.error(f"Error answering callback query: {e}")
                    return  # Exit if the user is already registered for this time

        if name in master_classes:
            master_classes[name]['users'][time].append(user_id)
            if name not in user_registrations:
                user_registrations[user_id] = {}
            user_registrations[user_id][name] = time
            master_classes[name]['places'][time] -= 1
            reply_markup = register(name)
            await query.edit_message_text(
                text=f'Спикер: <b><i>{name}</i></b>\nНазвание: <i>{name}</i>',
                parse_mode=ParseMode.HTML,
                reply_markup=reply_markup
            )
            try:
                await context.bot.send_message(
                    chat_id=6033842569,
                    text=f'@{query.from_user.username} на: {name} в {time}',
                )
            except BadRequest as e:
                logger.error(f"Error answering callback query: {e}")
            await context.bot.send_message(chat_id=6033842569, text=f'@{query.from_user.username} {name} в {time}')


    elif action == "reg":
        data = query.data.split("_")
        if len(data) != 4 or data[0] != "reg":
            logger.error(f"Invalid callback data: {query.data}")
            return

        team, short_name, time = data[1], data[2], data[3]
        user_id = query.from_user.id
        username = query.from_user.username

        # Проверяем, что мастер-класс существует
        if team not in master_clas or short_name not in master_clas[team]:
            logger.error(f"Invalid team or short_name in callback: {query.data}")
            await query.answer("Ошибка! Мастер-класс не найден.")
            return

        # Проверяем, записался ли пользователь ранее
        for t in master_clas:
            for short, mc_data in master_clas[t].items():
                for t_slot, users in mc_data['users'].items():
                    if user_id in users:
                        await query.answer(
                            "Вы уже записаны на мастер-класс!",
                            show_alert=True
                        )
                        return

        mc = master_clas[team][short_name]

        # Проверяем наличие мест
        if mc['places'][time] <= 0:
            await query.answer("Мест больше нет!", show_alert=True)
            return

        # Регистрируем пользователя
        mc['places'][time] -= 1
        mc['users'][time].append(user_id)

        # Обновляем сообщение с количеством мест
        reply_markup = create_register_keyboard(team, short_name, mc['places'].keys())
        try:
            await query.edit_message_text(
                text=(
                    f"----------------------------------------------------------\n"
                    f"<b>Организатор:</b> {team}\n\n"
                    f"<b>Название:</b> {mc['full_name']}\n\n"
                    f"<i>{mc['desc']}</i>"
                ),
                parse_mode=ParseMode.HTML,
                reply_markup=reply_markup
            )
        except BadRequest as e:
            logger.error(f"Ошибка при обновлении сообщения: {e}")

        # Отправляем сообщение администратору
        try:
            await context.bot.send_message(
                chat_id=6033842569,
                text=f"@{username} записался на {mc['full_name']} в {time}."
            )
        except BadRequest as e:
            logger.error(f"Ошибка при отправке сообщения администратору: {e}")

    elif action == "join":
        chat_id = int(short_name)
        game = games.get(chat_id)

        if game is None:
            games[chat_id] = TicTacToe()
            game = games[chat_id]

        if game.add_player(user_id):
            if len(game.players) == 2:
                await context.bot.send_message(
                    chat_id=chat_id,
                    text=f"Игра началась! Ходит X:\n{game.get_board_str()}",
                    reply_markup=create_keyboard()
                )
            else:
                # Устанавливаем таймер на 2 минуты
                context.job_queue.run_once(kick_user, 120, data={'chat_id': chat_id, 'user_id': user_id})
                await update.callback_query.answer("Вы присоединились к игре. Ожидаем второго игрока...")
        else:
            await update.callback_query.answer("Игра уже заполнена или вы уже участвуете.")


    elif action.isdigit():

        position = int(action)

        chat_id = update.callback_query.message.chat.id

        game = games.get(chat_id)

        if game is None:
            await update.callback_query.answer("Игра не найдена.")

            return

        if user_id != game.players[0] and user_id != game.players[1]:
            await update.callback_query.answer("Вы не участвуете в этой игре.")

            return

        if user_id != game.player_ids[game.current_player]:
            await update.callback_query.answer(f"Ходит игрок {game.player_ids[game.current_player]}.")

            return

        if not game.make_move(position):
            await update.callback_query.answer("Эта клетка уже занята!")

            return

        winner_symbol, loser_symbol = game.check_winner()

        if winner_symbol:
            if winner_symbol == 'Draw':
                # Отправляем сообщение о ничьей в другой чат
                await context.bot.send_message(
                    chat_id=putevki,  # Замените на ID целевого чата
                    text=f"Игра закончилась ничьей!\n{game.get_board_str()}",
                    message_thread_id=54
                )
                await update.callback_query.edit_message_text(
                    text=f"Игра закончилась ничьей!\n{game.get_board_str()}"
                )
            else:
                # Отправляем сообщение о победе в другой чат
                await context.bot.send_message(
                    chat_id=putevki,  # Замените на ID целевого чата
                    text=f"Игрок {game.player_ids[winner_symbol]} победил!\n{game.get_board_str()}",
                    message_thread_id=54
                )
                await update.callback_query.edit_message_text(
                    text=f"Игрок {game.player_ids[winner_symbol]} победил!\n{game.get_board_str()}"
                )

                # Логика для обновления баланса команд

                cursor.execute('SELECT team FROM users WHERE id = ?', (game.player_nicks[winner_symbol],))

                team_win = cursor.fetchone()

                cursor.execute('SELECT team FROM users WHERE id = ?', (game.player_nicks[loser_symbol],))

                team_lose = cursor.fetchone()

                if team_win and team_lose:
                    # Обновляем баланс команд

                    cursor.execute('UPDATE team SET balance = balance + 5 WHERE id = ?', (team_win[0],))

                    conn.commit()

                    cursor.execute('SELECT balance FROM team WHERE id = ?', (team_win[0],))

                    bal = cursor.fetchone()

                    chat = array_message[team_win[0] - 1]  # Индексируем по команде

                    id = array_id[team_win[0] - 1]

                    await context.bot.edit_message_text(chat_id=chat, message_id=id,
                                                        text=f'Баланс вашей команды: {bal[0]}')

                    cursor.execute('UPDATE team SET balance = balance - 5 WHERE id = ?', (team_lose[0],))

                    conn.commit()

                    cursor.execute('SELECT balance FROM team WHERE id = ?', (team_lose[0],))

                    bal = cursor.fetchone()

                    chat = array_message[team_lose[0] - 1]  # Индексируем по команде

                    id = array_id[team_lose[0] - 1]

                    await context.bot.edit_message_text(chat_id=chat, message_id=id,
                                                        text=f'Баланс вашей команды: {bal[0]}')

            invite = await context.bot.create_chat_invite_link(chat_id=chat_id)

            keyboard = [

                [InlineKeyboardButton(f"Комната", url=invite.invite_link)]

            ]

            reply_markup = InlineKeyboardMarkup(keyboard)

            await context.bot.edit_message_reply_markup(chat_id=putevki, message_id=room_messages[chat_id],

                                                        reply_markup=reply_markup)

            del games[chat_id]  # Удаляем игру после завершения

        else:

            game.switch_player()  # Меняем игрока

            await update.callback_query.edit_message_text(

                text=f"Ходит {game.current_player}:\n{game.get_board_str()}",

                reply_markup=create_keyboard()  # Редактируем текущее сообщение с новым состоянием поля

            )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if all(chat_id in games for chat_id in game_chats):
        await update.message.reply_text("Все чаты заняты. Попробуйте позже.")
        return

    # Создаем сообщения с кнопками для перехода в игровые чаты
    for i, game_chat in enumerate(game_chats):
        invite = await context.bot.create_chat_invite_link(chat_id=game_chat)
        keyboard = [
            [InlineKeyboardButton(f"Комната {i+1}",url= invite.invite_link)]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        message = await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Комната {i+1}",
            reply_markup=reply_markup,
            message_thread_id=54
        )
        await asyncio.sleep(1)

        print(game_chat,message.message_id)
        room_messages[game_chat] = message.message_id

async def player_move(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.callback_query.message.chat.id
    user_id = update.callback_query.from_user.id
    game = games.get(chat_id)

    if game is None:
        await update.callback_query.answer("Игра не найдена.")
        return

    if user_id != game.players[0] and user_id != game.players[1]:
        await update.callback_query.answer("Вы не участвуете в этой игре.")
        return

    if user_id != game.player_ids[game.current_player]:
        await update.callback_query.answer(f"Ходит игрок {game.player_ids[game.current_player]}.")
        return

    position = int(update.callback_query.data)

    if not game.make_move(position):
        await update.callback_query.answer("Эта клетка уже занята!")
        return

    winner_symbol, loser_symbol = game.check_winner()
    if winner_symbol:
        if winner_symbol == 'Draw':
            await update.callback_query.edit_message_text(
                text=f"Игра закончилась ничьей!\n{game.get_board_str()}"
            )
        else:
            await update.callback_query.edit_message_text(
                text=f"Игрок {game.player_ids[winner_symbol]} победил!\n{game.get_board_str()}"
            )

        # Логика для обновления баланса команд
        cursor.execute('SELECT team FROM users WHERE id = ?', (game.player_nicks[winner_symbol],))
        team_win = cursor.fetchone()
        cursor.execute('SELECT team FROM users WHERE id = ?', (game.player_nicks[loser_symbol],))
        team_lose = cursor.fetchone()

        if team_win and team_lose:
            # Обновляем баланс команд
            cursor.execute('UPDATE team SET balance = balance + 5 WHERE id = ?', (team_win[0],))
            conn.commit()

            cursor.execute('SELECT balance FROM team WHERE id = ?', (team_win[0],))
            bal = cursor.fetchone()
            chat = array_message[team_win[0] - 1]  # Индексируем по команде
            id = array_id[team_win[0] - 1]
            await context.bot.edit_message_text(chat_id=chat, message_id=id, text=f'Баланс вашей команды: {bal[0]}')

            cursor.execute('UPDATE team SET balance = balance - 5 WHERE id = ?', (team_lose[0],))
            conn.commit()

            cursor.execute('SELECT balance FROM team WHERE id = ?', (team_lose[0],))
            bal = cursor.fetchone()
            chat = array_message[team_lose[0] - 1]  # Индексируем по команде
            id = array_id[team_lose[0] - 1]
            await context.job_queue.run_once(kick_user,1,data={'chat_id': chat_id, 'user_id': game.player_ids[loser_symbol]})
            await context.job_queue.run_once(kick_user,1,data={'chat_id': chat_id, 'user_id': game.player_ids[winner_symbol]})
            await context.bot.edit_message_text(chat_id=chat, message_id=id, text=f'Баланс вашей команды: {bal[0]}')
        for player_id in game.players:
            await context.bot.kick_chat_member(chat_id=chat_id, user_id=player_id)
        await context.bot.send_message(chat_id=chat_id, text="Игра завершена. Всех игроков кикнули из чата.")
        del games[chat_id]  # Удаляем игру после завершения
    else:
        game.switch_player()  # Меняем игрока
        await update.callback_query.edit_message_text(
            text=f"Ходит {game.current_player}:\n{game.get_board_str()}",
            reply_markup=create_keyboard()  # Редактируем текущее сообщение с новым состоянием поля
        )

def create_keyboard():
    keyboard = [
        [InlineKeyboardButton("1", callback_data='0'), InlineKeyboardButton("2", callback_data='1'), InlineKeyboardButton("3", callback_data='2')],
        [InlineKeyboardButton("4", callback_data='3'), InlineKeyboardButton("5", callback_data='4'), InlineKeyboardButton("6", callback_data='5')],
        [InlineKeyboardButton("7", callback_data='6'), InlineKeyboardButton("8", callback_data='7'), InlineKeyboardButton("9", callback_data='8')]
    ]
    return InlineKeyboardMarkup(keyboard)

job_queue = JobQueue()

async def handle_new_chat_members(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat.id
    if chat_id in game_chats:
        new_members = update.message.new_chat_members
        if chat_id in game_chats:
            game = games.get(chat_id)
            if game is None:
                games[chat_id] = TicTacToe()
                game = games[chat_id]

            for member in new_members:
                user_id = member.id
                if game.add_player(user_id):
                    if len(game.players) == 2:
                        await context.bot.send_message(
                            chat_id=chat_id,
                            text=f"Игра началась! Ходит X:\n{game.get_board_str()}",
                            reply_markup=create_keyboard()
                        )
                        await context.bot.edit_message_reply_markup(chat_id=putevki, message_id=room_messages[chat_id],
                                                                    reply_markup=None)
                    else:
                        # Устанавливаем таймер на 2 минуты
                        context.job_queue.run_once(kick_user, 120, data={'chat_id': chat_id, 'user_id': user_id})
                        await context.bot.send_message(
                            chat_id=chat_id,
                            text=f"Вы присоединились к игре. Ожидаем второго игрока..."
                        )
                else:
                    await context.bot.send_message(
                        chat_id=chat_id,
                        text="Игра уже заполнена или вы уже участвуете."
                    )

async def kick_user(context):
    data = context.job.data
    chat_id = data['chat_id']
    user_id = data['user_id']
    bot: Bot = context.bot
    await bot.ban_chat_member(chat_id, user_id)
    await bot.unban_chat_member(chat_id, user_id)
    del games[chat_id]

async def handle_message(update: Update, context: CallbackContext) -> None:
    text = update.message.text
    tasks = text.split('\n')[1:]

    for i, task in enumerate(tasks):
        if i < len(tasks):
            keyboard = [
                [InlineKeyboardButton("Перейти в чат", url=f"https://t.me/mary_vii")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await context.bot.send_message(chat_id=putevki,text=task, reply_markup=reply_markup,message_thread_id=57)
            await asyncio.sleep(1)

def xd(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет! Отправьте мне сообщение, и я перешлю его в другой чат.')

async def forward_message(update: Update, context: CallbackContext) -> None:
    video_note = update.message.video_note

    # Отправляем видеосообщение в другой чат как новое сообщение
    await context.bot.send_video_note(chat_id=putevki,message_thread_id=919, video_note=video_note.file_id)


def main():
    application = ApplicationBuilder().token(bot_token).build()

    application.add_handler(MessageReactionHandler(get_reactions))
    application.add_handler(CommandHandler('help', unban))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_messages))
    application.add_handler(CommandHandler('tasks',handle_message))
    application.add_handler(CommandHandler("game", start))
    application.add_handler(CallbackQueryHandler(handle_callback))
    application.add_handler(MessageHandler(filters.VIDEO_NOTE, forward_message))
    application.add_handler(MessageHandler(filters.Dice.ALL, handle_dice))
    application.add_handler(CommandHandler("product", pstart))
    application.add_handler(CommandHandler("po",po))
    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, handle_new_chat_members))
    application.add_handler(CommandHandler("mk", check_answer))
    application.add_handler(CommandHandler("balance", balance))

    application.run_polling()

if __name__ == '__main__':
    main()
