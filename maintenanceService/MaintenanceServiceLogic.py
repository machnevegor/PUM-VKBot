# Authors of the project:
# 1-MachnevEgor_https://vk.com/machnev_egor
# 2-SchalimovDmitriy_https://vk.com/astronaut_without_spaceship
# 3-ArsenyKarimov_https://vk.com/id222338543
# 4-MihailMarkov_https://vk.com/mixxxxail
# Contacts in email:
# 1-meb.official.com@gmail.com
# 2-dmitriy-shalimov@yandex.ru
# 3-arseny.karimov@gmail.com
# 4-mihailmarkov2004@gmail.com

# import main modules
from configurationFile import BotConfig as BotConfig
import vk_api as vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import json as json
from random import randint as randint
import time as time
import datetime as datetime

# reboot time
reboot_time = 10

# information about developers
about_bot = [
    "Данного бота по фану запилили рандомные челики из ПУМа. Этот бот отличается от всех других тем, что импортирует всю информацию из базы данных школы, а не тупо по написанным строкам разработчиков. Бот продуман, но не идеален, поэтому все вопросы можете задавать в беседу, прикреплённую к сообществу бота. Также хочется напомнить, что у нас есть discord сервер для разработчиков, на котором вы сможете найти себе команду для проекта, узнать что-то новое или присоединится к чьей-то идеи:\nhttps://discord.gg/EmJKG5x😊"]
# array for keyboard
buttons_back = ["здравствуй", "привет", "хай", "куку", "ку", "салам", "саламалейкум", "здарова", "дыдова", "начать",
                "главное меню", "меню", "плитки", "клавиатура", "назад", "hello", "hey", "hi", "qq", "q", "start",
                "main menu", "menu", "tiles", "keyboard", "back"]
# auxiliary arrays
ru_greetings_bot = ["здравствуй", "привет", "хай", "ку", "салам", "здарова", "дыдова"]
eng_greetings_bot = ["hello", "hey", "hi", "qq", "q"]


# algorithm for processing user requests
def bot_processing():
    # system arrays
    global groups_id_array
    groups_id_array = ["187254286"]
    global users_id_array
    users_id_array = []
    # sources protection
    global sources_protection
    sources_protection = []

    # vk connect
    vk = vk_api.VkApi(token=f"{BotConfig.BotToken}")
    vk._auth_token()
    vk.get_api()
    # connection information
    print("-----------------------------")
    print("Bot launched into the network")
    print("-----------------------------")

    # get buttons for the VK keyboard
    def get_button(label, color, payload=""):
        return {
            "action": {
                "type": "text",
                "payload": json.dumps(payload),
                "label": label
            },
            "color": color
        }

    # keyboards settings
    main_keyboard = {
        "one_time": False,
        "buttons": [
            [get_button(label="Получить ID", color="positive"),
             get_button(label="Проверить обновления", color="positive")],
            [get_button(label="О боте", color="primary")],
        ]
    }

    # json for keyboard
    main_keyboard = json.dumps(main_keyboard, ensure_ascii=False).encode("utf-8")
    main_keyboard = str(main_keyboard.decode("utf-8"))

    # sending messages
    def write_msg(id, message, keyboard=None, sticker_id=None, attachment=None):
        # sending data to the terminal
        print(f"Responce: {''.join(message)}")
        if sticker_id != None:
            print(f"Sticker: {sticker_id}")
        if attachment != None:
            print(f"Attachment: {attachment}")
        # send the message
        vk.method("messages.send", {"peer_id": id, "message": message, "keyboard": keyboard, "sticker_id": sticker_id,
                                    "attachment": attachment, "random_id": randint(1, 100000000)})

    # longpoll
    longpoll = VkBotLongPoll(vk, group_id=groups_id_array)
    # response logic
    for event in longpoll.listen():
        # processing a new message
        if event.type == VkBotEventType.MESSAGE_NEW:
            # sending data to the terminal
            print(datetime.datetime.today())
            print(f"Message from-->https://vk.com/id{event.object.peer_id}")
            print(f"Message content: {event.object.text}")
            # if the request is from in private messages
            if event.object.peer_id == event.object.from_id:
                # if this user is not already in the database
                if event.object.peer_id not in users_id_array:
                    users_id_array.append(event.object.peer_id)
                # if the back buttons are pressed
                if event.object.text.lower() in buttons_back:
                    # greetings and jump to main menu
                    if event.object.text.lower().lower() in ru_greetings_bot:
                        response_randomizer = randint(0, len(ru_greetings_bot) - 1)
                        response_word = ru_greetings_bot[response_randomizer]
                        get_user_name = vk.method("users.get", {"user_ids": event.object.peer_id})[0]["first_name"]
                        write_msg(event.object.peer_id, f"{response_word.title()}, {str(get_user_name)}!",
                                  keyboard=main_keyboard)
                    elif event.object.text.lower().lower() in eng_greetings_bot:
                        response_randomizer = randint(0, len(eng_greetings_bot) - 1)
                        response_word = eng_greetings_bot[response_randomizer]
                        get_user_name = vk.method("users.get", {"user_ids": event.object.peer_id})[0]["first_name"]
                        write_msg(event.object.peer_id, f"{response_word.title()}, {str(get_user_name)}!",
                                  keyboard=main_keyboard)
                    # only jump to main menu
                    else:
                        write_msg(event.object.peer_id, "Главное меню👌", keyboard=main_keyboard)
                # main keyboard
                elif event.object.text.lower() == "получить id":
                    write_msg(event.object.peer_id, f"Твой персональный ID в ВК: id{event.object.peer_id}",
                              keyboard=main_keyboard)
                elif event.object.text.lower() == "проверить обновления":
                    write_msg(event.object.peer_id,
                              "На данный момент обновлений не найдено. Периодически чекай стену сообщества, чтобы узнать информацию об различных анонсах🙂",
                              keyboard=main_keyboard)
                elif event.object.text.lower() == "о боте":
                    write_msg(event.object.peer_id, about_bot, keyboard=main_keyboard)
                    write_msg(event.object.peer_id,
                              "Не забывайте, что всю актуальную информацию о боте вы можете найти на стене нашего сообщества, поэтому, если бот не отвечает, вы знаете, что делать😉",
                              keyboard=main_keyboard, attachment="photo222338543_457245618_dcd23490db181404fc")
                # easter egg
                elif event.object.text.lower() == "пасхалка":
                    write_msg(event.object.peer_id,
                              "Пасхалка?! Вау, в боте есть пасхалка! Приступим, есть шифр, указанный в пикче ниже - расшифруй его и отпишись в общую беседу сообщества(понимаем, что довольно сложно, поэтому даём две подсказки: ascii, tenet)",
                              keyboard=main_keyboard, attachment="photo222338543_457245619_81b41a6918becb0404")
                # unrecognized command
                else:
                    write_msg(event.object.peer_id, "Это точно команда:/", keyboard=main_keyboard)
                # sending data to the terminal
                print("-----------------------------")


# connect and reconnect when disconnected
if __name__ == "__main__":
    while True:
        try:
            bot_processing()
        except Exception as E:
            print("-----------------------------")
            print(datetime.datetime.today())
            print("!!!  The bot is disabled  !!!")
            print(f"Reason: {E}")
            print("-----------------------------")
            time.sleep(reboot_time)
            print("!!!    Reconnect, wait    !!!")

# Authors of the project:
# 1-MachnevEgor_https://vk.com/machnev_egor
# 2-SchalimovDmitriy_https://vk.com/astronaut_without_spaceship
# 3-ArsenyKarimov_https://vk.com/id222338543
# 4-MihailMarkov_https://vk.com/mixxxxail
# Contacts in email:
# 1-meb.official.com@gmail.com
# 2-dmitriy-shalimov@yandex.ru
# 3-arseny.karimov@gmail.com
# 4-mihailmarkov2004@gmail.com

