# "5891865424:AAEt3gQePcxS3iPZKvc-6KljHDnIzuPvmmM"
import time

import telebot
from telebot import types

from Tamogochi_Database import write_data_database, delete_data_database, update_pets_from_database
from Tamogochi import Pet

bot = telebot.TeleBot("5891865424:AAEt3gQePcxS3iPZKvc-6KljHDnIzuPvmmM")

pets = {}
pets_inv = {}  # <- зберігання об'эктів петів

x = 0

hatico_img = open("C:\\Users\\davidik07\\Downloads\\Hatico.jpg", 'rb')
hatico_img2 = open("C:\\Users\\davidik07\\Downloads\\Хатико 2.jpg", 'rb')


# /start
@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Почати грати в гру Tamogotchi')
    markup.add(item1)
    bot.send_message(chat_id, f'Привет {message.from_user.first_name}', reply_markup=markup)
    with hatico_img as img:
        bot.send_photo(chat_id, img)
    bot.send_message(chat_id, "Щоб почати грати, натисніть на кнопку")
    bot.register_next_step_handler(message, create_pet_command)


def create_pet(message):
    chat_id = message.chat.id
    pet_name = message.text

    pet = Pet(pet_name)
    write_data_database(pet_name)
    pets_inv[pet_name] = '0'

    pets[chat_id] = pet

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('🍕Покормити')
    item2 = types.KeyboardButton('⚽Играти')
    item3 = types.KeyboardButton('🛌Спати')
    item4 = types.KeyboardButton('👨‍⚕️Статус')
    item5 = types.KeyboardButton('🏅Iвент 1')
    item6 = types.KeyboardButton('👋Выйти')
    item7 = types.KeyboardButton('Поменяти пета')
    item8 = types.KeyboardButton("Создать пета")
    markup.add(item1, item2, item3, item4, item5, item6, item7, item8)
    bot.send_message(chat_id, f"Вітаю, ви створили пета з ім'ям {pet_name}!", reply_markup=markup)

    bot.register_next_step_handler(message, pet_commands)


@bot.message_handler(commands=['text'])
def create_pet_command(message):
    chat_id = message.chat.id

    if message.chat.type == 'private':
        if message.text == 'Почати грати в гру Tamogotchi':
            bot.send_message(chat_id, "Введи ім'я свого пета:")
            bot.register_next_step_handler(message, create_pet)


@bot.message_handler(content_types=['text'])
def pet_commands(message):
    chat_id = message.chat.id

    if chat_id not in pets:
        bot.send_message(chat_id, "Спочатку створіть пета за допомогою команди /start.")
        return
    if message.chat.type == 'private':
        if message.text == '🍕Покормити':
            pet = pets[chat_id]
            with open("C:\\Users\\davidik07\\Downloads\\Hatico.jpg", 'rb') as hatico_img:
                bot.send_photo(chat_id, hatico_img)
            bot.send_message(chat_id, "Дякую, що погодував мене")
            pet.feed(bot, chat_id)
            pet._update()
            pet.update_database()
        elif message.text == '⚽Играти':
            pet = pets[chat_id]
            with open("C:\\Users\\davidik07\\Downloads\\Hatico.jpg", 'rb') as img:
                bot.send_photo(chat_id, img)
            bot.send_message(chat_id, "Ця гра була чудовою")
            pet.play(bot, chat_id)
            pet._update()
            pet.update_database()
        elif message.text == '🛌Спати':
            pet = pets[chat_id]
            bot.send_message(chat_id, "Скільки годин ви спали?")
            bot.register_next_step_handler(message, sleep_hours_handler)
        elif message.text == '👨‍⚕️Статус':
            pet = pets[chat_id]
            with open("C:\\Users\\davidik07\\Downloads\\Хатико 2.jpg", 'rb') as img:
                bot.send_photo(chat_id, img)
            pet.check_statuts(bot, chat_id)
        elif message.text == 'Создать пета':
            bot.send_message(chat_id, "Як звати вашого пета:")
            bot.register_next_step_handler(message, create)
        elif message.text == 'Поменяти пета':
            bot.send_message(chat_id, 'Ось усі ваші пети, які ви створювали: ' + str(pets_inv))
            bot.send_message(chat_id, 'Який пета ви хочете поміняти?')
            bot.register_next_step_handler(message, change_pet_handler)
        elif message.text == '🏅Iвент 1':
            pet = pets[chat_id]

            bot.send_message(chat_id, 'Вам выпал ивент "Угадай число от Бота". Введите число от 0 до 100:')
            bot.send_message(chat_id, 'Якщо ви вгадайте число від + 20 балів до вас на кишеню. У вас 1 спроба')
            bot.send_message(chat_id, "Бот загадав число спробуй вгадати число")
            bot.send_message(chat_id, "Введiть число: ")

            bot.register_next_step_handler(message, event_1_handler)
        elif message.text == '👋Выйти':
            del pets[chat_id]  # Удалить питомца из словаря
            delete_data_database()
            bot.send_message(chat_id, "Ви пішли з гри. Гра завершилась. Всі ваші пети видались з База Данних!")
            bot.send_message(chat_id, "Пока👋")

        else:
            bot.send_message(chat_id, "Невідома команда.")

        # pet.update_database()


def change_pet_handler(message):
    chat_id = message.chat.id
    choice_pet = message.text

    if choice_pet not in pets_inv:
        delete_data_database()
        bot.send_message(chat_id, "З таким ім’ям Пета немає в базі даних, яку ви створювали.")

    else:
        for j in pets_inv.keys():
            if choice_pet == j:
                data_scores, data_eat, data_health, data_mood, data_sleep, data_hygiena = update_pets_from_database(
                    choice_pet)
                pet = Pet(j, data_scores, data_eat, data_health, data_mood, data_sleep, data_hygiena)
                pets[chat_id] = pet
                bot.send_message(chat_id, f"Ви змінили пета на {j}.")
                break


def create(message):
    chat_id = message.chat.id
    ch = message.text
    pets_inv[ch] = f'{chat_id + 1}'
    write_data_database(ch)
    pet = Pet(ch)
    pets[chat_id] = pet
    bot.send_message(chat_id, 'Ви создали пета')


def event_1_handler(message):
    chat_id = message.chat.id

    user_input = message.text
    pet = pets[chat_id]

    with open("C:\\Users\\davidik07\\Downloads\\Хатико 2.jpg", 'rb') as img:
        bot.send_photo(chat_id, img)
    bot.send_message(chat_id, "Наступного разу я обов'язково виграю")

    pet.event_1(bot, chat_id, user_input)
    pet._update()
    pet.update_database()


def sleep_hours_handler(message):
    chat_id = message.chat.id
    hours = message.text

    if chat_id in pets:
        pet = pets[chat_id]

        with open("C:\\Users\\davidik07\\Downloads\\Хатико 2.jpg", 'rb') as img:
            bot.send_photo(chat_id, img)
        bot.send_message(chat_id, "Я поспав")

        pet.sleeping(bot, chat_id, hours)
        pet._update()
        pet.update_database()


bot.polling(none_stop=True)
