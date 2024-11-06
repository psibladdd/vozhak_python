import logging
import sqlite3
import asyncio
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
array_message = [-1002424140672,-1002369574391,-1002422931787,-1002385442088,-1002316623832]
logger = logging.getLogger(__name__)
bot_token =  '7817513170:AAHiSByrlrUD1rQ8wMtG_7l-zPDOc3ISzdI'
conn = sqlite3.connect('teams.db', check_same_thread=False)
cursor = conn.cursor()
# Создаем клиента
master_classes = {}
user_registrations = {}
players = []
waiting_game = {}
my_id = "6033842569"

putevki='-1002373983158'
id_put = '6'
products = [
    {
        "id": 1,
        "name": "Вадим",
        "price": 100,
        "description": "Активчик, был в этом лагере уже 10 раз. Его знают все – админка и вожатые. С ним никогда не было проблем, каждый раз его ставили командиром отряда, не давая другим детям попробовать себя на этой должности.",
        "image": "1.jpg"
    },
    {
        "id": 2,
        "name": "Елисей",
        "price": 125,
        "description": "Этот ребёнок всегда улыбается и заряжает всех вокруг своим позитивом. Он любит шутить и веселиться, а его смех слышен даже на самых отдалённых уголках лагеря.",
        "image": "2.jpg"
    },
    {
        "id": 3,
        "name": "Анастасия",
        "price": 75,
        "description": "Этот ребёнок не признаёт никаких правил и ограничений. Он всегда делает то, что хочет, и не слушает никого. Его свободолюбивый характер вызывает восхищение у других детей, но иногда его действия могут привести к неприятностям",
        "image": "3.jpg"
    },
    {
        "id": 4,
        "name": "Владимир",
        "price": 50,
        "description": "Его талант к рисованию поражает всех. Он создаёт удивительные картины, которые украшают стены лагеря и радуют глаз каждого, кто их видит.",
        "image": "4.jpg"
    },
    {
        "id": 5,
        "name": "Оксана",
        "price": 65,
        "description": "Она всегда в центре внимания и любит привлекать к себе взгляды окружающих. Её актёрские способности позволяют ей легко вживаться в любую роль и создавать неповторимые образы",
        "image": "5.jpg"
    },
    {
        "id": 6,
        "name": "Екатерина",
        "price": 70,
        "description": "Эта девочка — настоящая спортсменка. Она участвует во всех спортивных мероприятиях лагеря и всегда стремится к победе. Её сила и выносливость вызывают восхищение у других детей.",
        "image": "6.jpg"
    },
    {
        "id": 7,
        "name": "Михаил",
        "price": 90,
        "description": "Он проводит большую часть времени за чтением книг. Его знания о мире литературы поражают даже самых опытных библиотекарей",
        "image": "7.jpg"
    },
    {
        "id": 8,
        "name": "Николай",
        "price": 85,
        "description": "У него есть свой инструмент, на котором он играет с большим мастерством. Его музыка наполняет лагерь радостью и вдохновением",
        "image": "8.jpg"
    },
{
        "id": 9,
        "name": "Артемий",
        "price": 110,
        "description": "Никто не знает, откуда он пришёл и что скрывает. Он предпочитает держаться в стороне от остальных детей и проводить время в одиночестве",
        "image": "9.jpg"
    },
    {
        "id": 10,
        "name": "Мария",
        "price": 115,
        "description": "Она всегда готова взять на себя ответственность и помочь другим. Ее лидерские качества делают его отличным кандидатом на должность командира отряда",
        "image": "10.jpg"
    },
    {
        "id": 11,
        "name": "Ангелина",
        "price": 100,
        "description": "Она часто погружается в свои мысли и мечты. Ее воображение позволяет ей создавать удивительные истории и миры",
        "image": "11.jpg"
    },
    {
        "id": 12,
        "name": "Семен",
        "price": 125,
        "description": "Он умеет петь, танцевать и играть на нескольких инструментах. Его выступления на сцене становятся настоящим праздником для всего лагеря",
        "image": "12.jpg"
    },
    {
        "id": 13,
        "name": "Аркадий",
        "price": 75,
        "description": "Ему нравится изучать новые места и открывать для себя что-то новое. Его любознательность и жажда знаний делают его интересным собеседником",
        "image": "13.jpg"
    },
    {
        "id": 14,
        "name": "Игорь",
        "price": 50,
        "description": "Он любит шутить и веселиться, но иногда его шутки могут быть не совсем безобидными. Он может подшутить над друзьями или вожатыми, но делает это без злого умысла",
        "image": "14.jpg"
    },
    {
        "id": 15,
        "name": "Алексей",
        "price": 65,
        "description": "Этот ребёнок постоянно в движении. Ему сложно усидеть на месте, и он всегда ищет новые приключения. Иногда он может создавать проблемы, но его энергия и жизнерадостность делают его любимцем лагеря",
        "image": "15.jpg"
    },
    {
        "id": 16,
        "name": "Ксения",
        "price": 70,
        "description": "Он очень ответственный и организованный, всегда следует правилам и инструкциям. Иногда его педантичность может раздражать других детей, но он всегда готов помочь и поддержать",
        "image": "16.jpg"
    },
    {
        "id": 17,
        "name": "София",
        "price": 90,
        "description": "Он редко говорит и предпочитает проводить время в одиночестве. Но когда он всё же открывает рот, его слова оказываются мудрыми и глубокими. Его молчаливость создаёт вокруг него атмосферу загадочности",
        "image": "17.jpg"
    },
    {
        "id": 18,
        "name": "Иван",
        "price": 85,
        "description": "Ему нравится испытывать себя и свои возможности. Он часто участвует в экстремальных мероприятиях и соревнованиях, что вызывает восхищение у других детей. Однако его безрассудство иногда приводит к неприятностям",
        "image": "18.jpg"
    },
    {
        "id": 19,
        "name": "Максим",
        "price": 110,
        "description": "Он всегда сомневается в том, что говорят другие. Он любит задавать вопросы и искать доказательства, прежде чем поверить во что-то. Его скептицизм может быть полезным, но иногда он мешает ему наслаждаться жизнью",
        "image": "19.jpg"
    },
    {
        "id": 20,
        "name": "Руслан",
        "price": 115,
        "description": "Иногда он может делать мелкие пакости другим детям или вожатым. Он не делает этого со злым умыслом, а скорее из любопытства или желания повеселиться. Однако его действия могут вызывать раздражение у окружающих",
        "image": "20.jpg"
    },
    {
        "id": 21,
        "name": "Маргарита",
        "price": 100,
        "description": "Этот ребенок любит прятаться и играть в прятки. Его навыки маскировки поражают даже самых опытных вожатых. Он может спрятаться так, что его не найдут даже с собаками",
        "image": "21.jpg"
    },
    {
        "id": 22,
        "name": "Дарья",
        "price": 125,
        "description": "Этот ребёнок всегда выглядит сонным и уставшим. Он часто засыпает на ходу и может проспать всё самое интересное. Но когда он бодрствует, он становится очень весёлым и активным",
        "image": "22.jpg"
    },
    {
        "id": 23,
        "name": "Елизавета",
        "price": 75,
        "description": "Этого ребёнка можно назвать тёмной лошадкой, потому что никто не может предсказать, как он поведёт себя в следующий момент. Он может быть весёлым и дружелюбным, а может внезапно стать замкнутым и агрессивным. Иногда он проявляет интерес к каким-то занятиям, но быстро теряет к ним интерес. Все надеются, что со временем смогут лучше понять этого ребёнка и помочь ему раскрыться.",
        "image": "23.jpg"
    },
    {
        "id": 24,
        "name": "Лев",
        "price": 50,
        "description": "Он всегда в центре внимания и любит быть лидером. Он умеет организовывать мероприятия и вовлекать других детей в игры и развлечения. Однако иногда его активность может перерасти в навязчивость",
        "image": "24.jpg"
    },
    {
        "id": 25,
        "name": "Ростислав",
        "price": 65,
        "description": "Он часто погружается в свои мысли и мечты. Его воображение позволяет ему создавать удивительные истории и миры. Иногда он может настолько погрузиться в свои фантазии, что забывает о реальности",
        "image": "25.jpg"
    },
    {
        "id": 26,
        "name": "Евгений",
        "price": 70,
        "description": "Ему сложно ждать и терпеть. Он всегда хочет получить всё и сразу. Его нетерпение может вызывать раздражение у других детей, но его энергия и энтузиазм делают его интересным собеседником",
        "image": "26.jpg"
    },
    {
        "id": 27,
        "name": "Александр",
        "price": 90,
        "description": "Он может починить всё что угодно: от сломанного стула до неработающего телевизора. Его навыки в области техники и механики делают его незаменимым помощником для вожатых и администрации лагеря. Он всегда готов прийти на помощь и решить любую проблему",
        "image": "27.jpg"
    },
    {
        "id": 28,
        "name": "Семен",
        "price": 85,
        "description": "Этот ребёнок обожает проводить время на свежем воздухе и изучать природу. Он знает все растения и животных, которые обитают в окрестностях лагеря, и с удовольствием рассказывает о них другим детям. Его любовь к природе делает его отличным компаньоном для прогулок и походов",
        "image": "28.jpg"
    },
    {
        "id": 29,
        "name": "Яна",
        "price": 110,
        "description": "У этого ребёнка есть настоящий талант в какой-то области. Может быть, это рисование, музыка, танцы или что-то ещё. Его талант вызывает восхищение у других детей, и они с радостью наблюдают за его выступлениями и работами",
        "image": "29.jpg"
    },
    {
        "id": 30,
        "name": "Жанна",
        "price": 115,
        "description": "Никто не знает, откуда он пришёл и что скрывает. Он предпочитает держаться в стороне от остальных детей и проводить время в одиночестве. Иногда он может показаться грустным и задумчивым, но никто не знает, что происходит у него в голове",
        "image": "30.jpg"
    }
]

def update_file(team_id, new_balance, commit_message):
    print(team_id)


# Пример функции для проверки баланса
def check_balance(user_id, price):
    cursor.execute('SELECT team FROM users WHERE id = ?', (user_id,))
    team_id = cursor.fetchone()[0]
    cursor.execute('SELECT balance FROM team WHERE id = ?', (team_id,))
    bal = cursor.fetchone()[0]

    if(price <= bal):
        cursor.execute('UPDATE team SET balance = balance - ? WHERE id = ?', (price,team_id))
        conn.commit()
        return True
    else:
        return False

products_ids = {

}

async def start(update, context: ContextTypes.DEFAULT_TYPE):
    # Отправляем фото и описание по каждому продукту
    for product in products:
        with open(f'photos/{product["image"]}', 'rb') as photo_file:
            try:
                await asyncio.sleep(1)
                message = await context.bot.send_photo(
                    chat_id=update.effective_chat.id,
                    photo=photo_file,
                    message_thread_id=6,
                    caption=f"Имя: {product['name']}\nХарактеристика: {product['description']}\nСтоимость путевки: {product['price']}",
                )
            except RetryAfter as e:
                await asyncio.sleep(e.retry_after)  # Ждем указанное время
            products_ids[product['name']] = message.message_id
    await send_product_list(update, context)

message_buy_id = ''
async def send_product_list(update, context):
    keyboard = [
        [KeyboardButton(text=f"Оплатить путевку для {product['name']}")] for product in products
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    message = await context.bot.send_message(
        chat_id=update.effective_chat.id,
        message_thread_id=6,
        reply_markup=reply_markup,
        text="Выберите:",  # Ваш текст "Выберите"
    )
    message_buy_id = message.message_id  # Сохраняем идентификатор


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    product = next((p for p in products if f"Оплатить путевку для {p['name']}" in user_message), None)

    if product:
        user_id = update.message.from_user.id
        cursor.execute('SELECT team FROM users WHERE id = ?', (user_id,))
        team_id = cursor.fetchone()[0]

        if check_balance(user_id, product['price']):
            await context.bot.send_message(
                chat_id=array_message[team_id - 1],
                text=f"{product['name']} теперь в вашем отряде!.",
            )

            # Удаляем сообщение о продукте по его ID
            if product['name'] in products_ids:
                message_id = products_ids[product['name']]
                if message_id:  # Проверка на наличие идентификатора
                    await context.bot.delete_message(
                        chat_id=update.effective_chat.id,
                        message_id=message_id
                    )
                    del products_ids[product['name']]

            # Удаляем предыдущее сообщение "Выберите"
            if message_buy_id:  # Проверка на наличие идентификатора
                await context.bot.delete_message(
                    chat_id=update.effective_chat.id,
                    message_id=message_buy_id
                )
            cursor.execute('SELECT balance FROM team WHERE id = ?', (team_id,))
            bal = cursor.fetchone()[0]
            chat = array_message[team_id - 1]
            await context.bot.edit_message_text(chat_id=chat, message_id=2, text=f'Баланс вашей команды: {bal}')
            products.remove(product)
            await send_product_list(update, context)
            await context.bot.delete_message(message_id=update.message.message_id, chat_id=update.effective_chat.id)

        else:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"Недостаточно средств для покупки {product['name']}.",
            )
            await context.bot.delete_message(
                chat_id=update.effective_chat.id,
                message_id=update.message.message_id
            )


messages_storage = {}
reactions_storage = {}

async def handle_messages(update: Update, context) -> None:
    if update.message.message_thread_id == 4:
        message_id = update.message.message_id
        # Если сообщение еще не в хранилище, добавляем его
        if message_id not in messages_storage:
            messages_storage[message_id] = update.message

async def get_reactions(update: Update, context) -> None:
    if update.message_reaction:
        message_id = update.message_reaction.message_id
        user_id = update.message_reaction.user.id
        username = update.message_reaction.user.username

        # Определяем, была ли реакция добавлена или удалена
        old_reaction = update.message_reaction.old_reaction
        new_reaction = update.message_reaction.new_reaction

        if message_id in messages_storage:
            cursor.execute('SELECT team FROM users WHERE id = ?', (user_id,))
            team_id = cursor.fetchone()[0]

            if new_reaction and not old_reaction:
                # Реакция добавлена
                cursor.execute('UPDATE team SET balance = balance + 5 WHERE id = ?', (team_id,))
            elif old_reaction and not new_reaction:
                # Реакция удалена
                cursor.execute('UPDATE team SET balance = balance - 5 WHERE id = ?', (team_id,))

            conn.commit()

            chat = array_message[team_id - 1]
            cursor.execute('SELECT balance FROM team WHERE id = ?', (team_id,))
            balance = cursor.fetchone()[0]

            await context.bot.edit_message_text(chat_id=chat, message_id=2, text=f'Баланс вашей команды: {balance}')
            update_file(team_id,balance,'Update balance')

async def handle_dice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    dice = update.message.dice
    user_id = update.message.from_user.id
    user_name = update.message.from_user.username or update.message.from_user.name
    cursor.execute('SELECT team FROM users WHERE id = ?', (user_id,))
    team_id = cursor.fetchone()[0]
    cursor.execute('SELECT balance FROM team WHERE id = ?', (team_id,))
    current_balance = cursor.fetchone()[0]
    cursor.execute('SELECT last_reward_time FROM team WHERE id = ?', (team_id,))
    last_reward_time_str = cursor.fetchone()[0]
    last_reward_time = datetime.strptime(last_reward_time_str, '%Y-%m-%d %H:%M:%S') if last_reward_time_str else None

    if last_reward_time and datetime.now() - last_reward_time < timedelta(hours=4):
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text='Часики еще не дотикали')
        return

    if dice.emoji == '🎲':  # Кубик
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
        cursor.execute('UPDATE team SET balance=?,last_reward_time = ? WHERE id = ?', (new_balance,datetime.now().strftime('%Y-%m-%d %H:%M:%S'), team_id))
        conn.commit()
        chat = array_message[team_id - 1]
        await context.bot.send_message(chat_id=chat,
                                       text=mess)
        await context.bot.edit_message_text(chat_id=chat, message_id=2, text=f'Баланс вашей команды: {balance}')
        update_file(team_id, balance, 'Update balance')


async def balance(update:Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    if update.effective_chat.type != 'private':
        await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.message.message_id)
    if user_id in [391743540,390561523,6755435741,6033842569]:
        args = context.args
        if len(args) != 2:
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text='Используйте команду в формате: /balance "номер команды" "число"')
            return

        target_team = int(args[0])
        try:
            amount = int(args[1])
        except ValueError:
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text='Пожалуйста, введите корректное число.')
            return

        cursor.execute('SELECT balance FROM team WHERE id = ?', (target_team,))
        existing_user = cursor.fetchone()

        if not existing_user:
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text=f'Команда номер {target_team} не найдена в базе данных.')
            return

        cursor.execute('UPDATE team SET balance = balance + ? WHERE id = ?', (amount, target_team))
        conn.commit()
        cursor.execute('SELECT balance FROM team WHERE id = ?', (target_team,))
        bal = cursor.fetchone()[0]
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=f'Команде номер {target_team} было начислено {amount} вожиков.')
        chat = array_message[target_team - 1]
        await context.bot.edit_message_text(chat_id=chat, message_id=2, text=f'Баланс вашей команды: {bal}')
        update_file(target_team, bal, 'Update balance')

    else:
        await context.bot.send_message(chat_id=update.effective_chat.id,text="Нет доступа к этой команде!")

def main():
    application = ApplicationBuilder().token(bot_token).read_timeout(600).get_updates_read_timeout(600).write_timeout(600).get_updates_write_timeout(600).pool_timeout(600).get_updates_pool_timeout(600).connect_timeout(600).get_updates_connect_timeout(600).build()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, button_handler))

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("balance", balance))
    application.add_handler(MessageHandler(filters.Dice.ALL, handle_dice))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_messages))
    application.add_handler(MessageReactionHandler(get_reactions))

    # Сначала добавим общий обработчик для всех кнопок\
    application.run_polling(read_timeout=600, write_timeout=600, pool_timeout=600, connect_timeout=600, timeout=600)


if __name__ == '__main__':
    main()