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
from telegram.constants import UpdateType
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
game_chats = [1002498876619, -4564472209, -4517693420,-4581338414,-4550254545,-4505419264,-4586885712,-4597880004,-4591307105,-4541738040]
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
    cursor.execute('SELECT team FROM users WHERE id = ?', (user_id,))
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

    times = ["12:30", "14:00", "16:30"]
    master_classes[name] = {'places': {time: places for time in times}, 'users': {time: [] for time in times}, 'id': 0}
    reply_markup = register(name)

    message = await context.bot.send_message(chat_id="-1002373983158", text=f'Название мастер-класса: {name}\n', message_thread_id=919, reply_markup=reply_markup)
    mk_to_id[name] = message.message_id

def register(name):
    times = ["12:30", "14:00", "16:30"]
    keyboard = []
    for time in times:
        if master_classes[name]['places'][time] > 0:
            keyboard.append([InlineKeyboardButton(f"Записаться в {time}\n Мест: {master_classes[name]['places'][time]}", callback_data=f"register_{name}_{time}")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup

messages_storage = {}
async def handle_messages(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.message_thread_id == 4:
        message_id = update.message.message_id
        if message_id not in messages_storage:
            messages_storage[message_id] = update.message

async def get_reactions(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message_reaction:
        message_id = update.message_reaction.message_id
        user_id = update.message_reaction.user.id
        username = update.message_reaction.user.username

        old_reaction = update.message_reaction.old_reaction
        new_reaction = update.message_reaction.new_reaction

        if message_id in messages_storage:
            cursor.execute('SELECT team FROM users WHERE id = ?', (user_id,))
            team_id = cursor.fetchone()[0]

            if new_reaction and not old_reaction:
                cursor.execute('UPDATE team SET balance = balance + 5 WHERE id = ?', (team_id,))
            elif old_reaction and not new_reaction:
                cursor.execute('UPDATE team SET balance = balance - 5 WHERE id = ?', (team_id,))

            conn.commit()
            chat = array_message[team_id - 1]

            cursor.execute('SELECT balance FROM team WHERE id = ?', (team_id,))
            balance = cursor.fetchone()[0]
            id = array_id[team_id-1]
            await context.bot.edit_message_text(chat_id=chat, message_id=id, text=f'Баланс вашей команды: {balance}')

async def handle_dice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    dice = update.message.dice
    user_id = update.message.from_user.id
    cursor.execute('SELECT team FROM users WHERE id = ?', (user_id,))
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


class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)]  # 3x3 поле
        self.current_player = 'X'  # Начинает X
        self.players = []  # Список игроков
        self.player_ids = {'X': None, 'O': None}  # Словарь, который связывает символ с ID игрока

    def add_player(self, player_id):
        if len(self.players) < 2 and player_id not in self.players:
            if len(self.players) == 0:
                self.player_ids['X'] = player_id  # Первому игроку даем символ X
            else:
                self.player_ids['O'] = player_id  # Второму игроку даем символ O
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

async def handle_callback(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()  # Подтверждаем получение запроса
    user_id = query.from_user.id  # Получаем ID пользователя

    # Логируем информацию о нажатой кнопке
    logger.info(f"User {user_id} clicked button with data: {query.data}")

    # Разделяем действие, имя и время из callback_data
    action, *args = query.data.split("_", 2)

    print(action)
    if action == "register":
        name, time = args
        if user_id in user_registrations:
            registered_time = user_registrations[user_id].get(name)
            if registered_time:
                await context.bot.send_message(chat_id=query.from_user.id, text=f'Вы уже записаны на мастер-класс: {name} в {registered_time}')
                return  # Прерываем выполнение, если пользователь уже зарегистрирован на это время

        # Проверяем, записан ли пользователь на другой мастер-класс в это же время
        if user_id in user_registrations:
            for mc_name, mc_time in user_registrations[user_id].items():
                if mc_time == time:
                    await context.bot.send_message(chat_id=query.from_user.id, text=f'Вы уже записаны на мастер-класс: {mc_name} в {mc_time}')
                    return  # Прерываем выполнение, если пользователь уже зарегистрирован на это время

        if name in master_classes:
            master_classes[name]['users'][time].append(user_id)
            if name not in user_registrations:
                user_registrations[user_id] = {}
            user_registrations[user_id][name] = time
            master_classes[name]['places'][time] -= 1
            reply_markup = register(name)
            await query.edit_message_text(text=f'Название мастер-класса: {name}\n', reply_markup=reply_markup)
            await context.bot.send_message(chat_id=user_id, text=f'Вы записаны на мастер-класс: {name} в {time}')
        else:
            await query.edit_message_text(f'Мастер-класс "{name}" не найден.')

    elif action == "buy":
        name = args[0]
        product = next((p for p in products if p['name'] == name), None)
        if product:
            cursor.execute('SELECT team FROM users WHERE id = ?', (user_id,))
            team_id = cursor.fetchone()[0]

            if check_balance(user_id, product['price']):
                await context.bot.send_message(
                    chat_id=array_message[team_id - 1],
                    text=f"{product['name']} теперь в вашем отряде!",
                )

                if product['name'] in products_ids:
                    message_id = products_ids[product['name']]
                    if message_id:
                        await context.bot.delete_message(
                            chat_id=update.effective_chat.id,
                            message_id=message_id
                        )
                        del products_ids[product['name']]

                if message_buy_id:
                    await context.bot.delete_message(
                        chat_id=update.effective_chat.id,
                        message_id=message_buy_id
                    )

                cursor.execute('SELECT balance FROM team WHERE id = ?', (team_id,))
                bal = cursor.fetchone()[0]
                chat = array_message[team_id - 1]
                id = array_id[team_id - 1]
                await context.bot.edit_message_text(chat_id=chat, message_id=id, text=f'Баланс вашей команды: {bal}')
                products.remove(product)
                await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=query.message.message_id)

            else:
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=f"Недостаточно средств для покупки {product['name']}.",
                )
                await context.bot.delete_message(
                    chat_id=update.effective_chat.id,
                    message_id=query.message.message_id
                )
        else:
            await query.edit_message_text(f'Продукт "{name}" не найден.')

    elif action == "join":
        chat_id = int(args[0])
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

                # Удаляем обоих игроков из чата в случае ничьей

                context.job_queue.run_once(kick_user, 1, data={'chat_id': chat_id, 'user_id': game.player_ids[0]})

                context.job_queue.run_once(kick_user, 2, data={'chat_id': chat_id, 'user_id': game.player_ids[1]})

                await context.bot.send_message(chat_id=putevki,

                                               text=f"Игра закончилась ничьей!\n{game.get_board_str()}",
                                               message_thread_id=54

                                               )

            else:

                context.job_queue.run_once(kick_user, 1,
                                           data={'chat_id': chat_id, 'user_id': game.player_ids[loser_symbol]})

                context.job_queue.run_once(kick_user, 2,
                                           data={'chat_id': chat_id, 'user_id': game.player_ids[winner_symbol]})

                await context.bot.send_message(chat_id=putevki,

                                               text=f"Игрок {winner_symbol} победил!\n{game.get_board_str()}",
                                               message_thread_id=54

                                               )

                # Логика для обновления баланса команд

                cursor.execute('SELECT team FROM users WHERE id = ?', (game.player_ids[winner_symbol],))

                team_win = cursor.fetchone()

                cursor.execute('SELECT team FROM users WHERE id = ?', (game.player_ids[loser_symbol],))

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
        cursor.execute('SELECT team FROM users WHERE id = ?', (game.player_ids[winner_symbol],))
        team_win = cursor.fetchone()
        cursor.execute('SELECT team FROM users WHERE id = ?', (game.player_ids[loser_symbol],))
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


def main():
    application = ApplicationBuilder().token(bot_token).build()
    application.add_handler(CommandHandler('help', unban))
    application.add_handler(CommandHandler('tasks',handle_message))
    application.add_handler(CommandHandler("game", start))
    application.add_handler(CallbackQueryHandler(handle_callback))  # Обработчик движения игрока
    application.add_handler(MessageHandler(filters.Dice.ALL, handle_dice))
    application.add_handler(CommandHandler("product", pstart))
    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, handle_new_chat_members))
    application.add_handler(CommandHandler("mk", check_answer))
    application.add_handler(CommandHandler("balance", balance))

    application.run_polling()

if __name__ == '__main__':
    main()
