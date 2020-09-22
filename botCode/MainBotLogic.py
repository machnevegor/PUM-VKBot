# Authors of the project:
# 1-MachnevEgor_https://vk.com/machnev_egor
# 2-SchalimovDmitriy_https://vk.com/astronaut_without_spaceship
# 3-ArsenyKarimov_https://vk.com/@id222338543
# 4-MihailMarkov_https://vk.com/mixxxxail
# Contacts in email:
# 1-meb.official.com@gmail.com
# 2-dmitriy-shalimov@yandex.ru
# 3-arseny.karimov@gmail.com
# 4-mihailmarkov2004@gmail.com

# import main modules
import vk_api as vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import json as json
from random import randint as randint
# import other modules
from configurationFile import BotConfig as BotConfig
from workWithExcelFile import ExcelSearcher as ExcelSearcher

# system arrays
groups_id_array = ["187254286"]
users_id_array = []
# excel source variable
excel_source = ""
# information about developers
about_developers = [
    "Данного бота по фану запили рандомные челики из ПУМа. Этот бот отличается от всех других тем, что импортирует всю информацию из базы данных школы, а не тупо по написанным строкам разработчиков. Бот продуман, но не идеален, поэтому все вопросы можете задавать в личку создателям, которых вы можете найти через информацию о сообществе, к которому прикреплён бот. Также хочется напомнить, что у нас есть discord сервер для разработчиков, на котором вы сможете найти себе команду для проекта, узнать что-то новое или присоединится к чье-то идеи: https://discord.gg/EmJKG5x😊"]
# array for keyboard
buttons_back = ["здравствуй", "привет", "хай", "куку", "ку", "салам", "саламалейкум", "здарова", "дыдова", "начать",
                "главное меню", "меню", "плитки", "клавиатура", "назад", "hello", "hey", "hi", "qq", "q", "start",
                "main menu", "menu", "tiles", "keyboard", "back"]
# auxiliary arrays
ru_greetings_bot = ["здравствуй", "привет", "хай", "ку", "салам", "здарова", "дыдова"]
eng_greetings_bot = ["hello", "hey", "hi", "qq", "q"]
# schedule calls
eight_nine_schedule_calls = "Расписание звонков:\n1. 9:00 - 9:45\n2. 9:50 - 10:35\n3. 10:55 - 11:40\n4. 11:50 - 12:35\n5. 12:45 - 13:30\n6. 13:50 - 14:35\n7. 14:45 - 15:30\n8. 15:40 - 16:25\n9. 16:30 - 17:15\n10. 17:20 - 18:05"
ten_eleven_schedule_calls = "Расписание звонков:\n1. 9:00 - 9:45\n2. 9:50 - 10:35\n3. 10:45 - 11:30\n4. 11:50 - 12:35\n5. 12:45 - 13:30\n6. 13:40 - 14:25\n7. 14:45 - 15:30\n8. 15:40 - 16:25\n9. 16:30 - 17:15\n10. 17:20 - 18:05"


# major fuctions
def get_button(label, color, payload=""):
    return {
        "action": {
            "type": "text",
            "payload": json.dumps(payload),
            "label": label
        },
        "color": color
    }


def write_msg(id, message, keyboard=None, sticker_id=None):
    vk.method("messages.send", {"peer_id": id, "sticker_id": sticker_id, "message": message, "keyboard": keyboard,
                                "random_id": randint(1, 100000000)})


def writeinconv(id, message, sticker_id=None):
    vk.method("messages.send", {"peer_id": id, "sticker_id": sticker_id, "message": message, "sticker_id": sticker_id,
                                "random_id": randint(1, 100000000)})


# keyboards settings
main_keyboard = {
    "one_time": False,
    "buttons": [
        [get_button(label="Учебники", color="positive"),
         get_button(label="Расписание", color="positive")],
        [get_button(label="О боте", color="primary")],
    ]
}

schedules_keyboard = {
    "one_time": False,
    "buttons": [
        [get_button(label="Звонков", color="positive"),
         get_button(label="Уроков", color="positive")],
        [get_button(label="Назад", color="secondary")],
    ]
}

select_call_class_keyboard = {
    "one_time": False,
    "buttons": [
        [get_button(label="8-9", color="positive"),
         get_button(label="10-11", color="positive")],
        [get_button(label="Назад", color="secondary")],
    ]
}

select_class_keyboard = {
    "one_time": False,
    "buttons": [
        [get_button(label="10-1", color="positive"),
         get_button(label="10-2", color="positive"),
         get_button(label="10-3", color="positive")],
        [get_button(label="Назад", color="secondary")],
    ]
}

choosing_day_of_week_keyboard = {
    "one_time": False,
    "buttons": [
        [get_button(label="Понедельник", color="positive"),
         get_button(label="Вторник", color="secondary"),
         get_button(label="Среда", color="positive")],
        [get_button(label="Четверг", color="positive"),
         get_button(label="Пятница", color="positive"),
         get_button(label="Суббота", color="positive")],
        [get_button(label="Назад", color="secondary")],
    ]
}

# vk connect
vk = vk_api.VkApi(token=f"{BotConfig.BotToken}")
vk._auth_token()
vk.get_api()

# longpoll
longpoll = VkBotLongPoll(vk, group_id=groups_id_array)

# json
main_keyboard = json.dumps(main_keyboard, ensure_ascii=False).encode("utf-8")
main_keyboard = str(main_keyboard.decode("utf-8"))
schedules_keyboard = json.dumps(schedules_keyboard, ensure_ascii=False).encode("utf-8")
schedules_keyboard = str(schedules_keyboard.decode("utf-8"))
select_call_class_keyboard = json.dumps(select_call_class_keyboard, ensure_ascii=False).encode("utf-8")
select_call_class_keyboard = str(select_call_class_keyboard.decode("utf-8"))
select_class_keyboard = json.dumps(select_class_keyboard, ensure_ascii=False).encode("utf-8")
select_class_keyboard = str(select_class_keyboard.decode("utf-8"))
choosing_day_of_week_keyboard = json.dumps(choosing_day_of_week_keyboard, ensure_ascii=False).encode("utf-8")
choosing_day_of_week_keyboard = str(choosing_day_of_week_keyboard.decode("utf-8"))

# connection information
print("-----------------------------")
print("Bot launched into the network")
print("-----------------------------")
# response logic
for event in longpoll.listen():
    # processing a new message
    if event.type == VkBotEventType.MESSAGE_NEW:
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
            elif event.object.text.lower() == "учебники":
                write_msg(event.object.peer_id,
                          "Ой, сорян, забыл предупредить - т.к. бот на бэтке, нам нужны люди, которые помогут найти все электронные сканы учебников с 8 по 11 классы, мы постепенно набираем базу, но ещё нужно время😏",
                          keyboard=main_keyboard)
            elif event.object.text.lower() == "расписание":
                write_msg(event.object.peer_id, "Ок, только выбери какое🖖", keyboard=schedules_keyboard)
            elif event.object.text.lower() == "о боте":
                write_msg(event.object.peer_id, about_developers, keyboard=main_keyboard)
            # schedules keyboard
            elif event.object.text.lower() == "звонков":
                write_msg(event.object.peer_id, "Такс, и ещё выбери свой класс🤔", keyboard=select_call_class_keyboard)
            elif event.object.text.lower() == "уроков":
                write_msg(event.object.peer_id, "Такс, и ещё выбери свой класс🤔", keyboard=select_class_keyboard)
            # select call class keyboard
            elif event.object.text.lower() == "8-9":
                write_msg(event.object.peer_id, eight_nine_schedule_calls, keyboard=main_keyboard)
            elif event.object.text.lower() == "10-11":
                write_msg(event.object.peer_id, ten_eleven_schedule_calls, keyboard=main_keyboard)
            # select class keyboard
            elif event.object.text.lower() == "10-1":
                excel_source = "excelDatabase/10class/10_1class.xlsx"
                write_msg(event.object.peer_id, "Отлично, теперь выбери день недели🗓",
                          keyboard=choosing_day_of_week_keyboard)
            elif event.object.text.lower() == "10-2":
                excel_source = "excelDatabase/10class/10_2class.xlsx"
                write_msg(event.object.peer_id, "Отлично, теперь выбери день недели🗓",
                          keyboard=choosing_day_of_week_keyboard)
            elif event.object.text.lower() == "10-3":
                excel_source = "excelDatabase/10class/10_3class.xlsx"
                write_msg(event.object.peer_id, "Отлично, теперь выбери день недели🗓",
                          keyboard=choosing_day_of_week_keyboard)
            # choosing day of week keyboard
            elif event.object.text.lower() == "понедельник":
                ExcelSearcher.selective_data_search(excel_source=excel_source, columns=["A", "B"], start_data="Понедельник",
                                                    end_data="None")
                write_msg(event.object.peer_id, ExcelSearcher.output_day_schedule, keyboard=main_keyboard)
            elif event.object.text.lower() == "вторник":
                write_msg(event.object.peer_id, "Кхм, у 10 классов сегодня технопарк, поэтому смотри сам🕶",
                          keyboard=main_keyboard)
            elif event.object.text.lower() == "среда":
                ExcelSearcher.selective_data_search(excel_source=excel_source, columns=["A", "B"], start_data="Среда",
                                                    end_data="None")
                write_msg(event.object.peer_id, ExcelSearcher.output_day_schedule, keyboard=main_keyboard)
            elif event.object.text.lower() == "четверг":
                ExcelSearcher.selective_data_search(excel_source=excel_source, columns=["A", "B"], start_data="Четверг",
                                                    end_data="None")
                write_msg(event.object.peer_id, ExcelSearcher.output_day_schedule, keyboard=main_keyboard)
            elif event.object.text.lower() == "пятница":
                ExcelSearcher.selective_data_search(excel_source=excel_source, columns=["A", "B"], start_data="Пятница",
                                                    end_data="None")
                write_msg(event.object.peer_id, ExcelSearcher.output_day_schedule, keyboard=main_keyboard)
            elif event.object.text.lower() == "суббота":
                ExcelSearcher.selective_data_search(excel_source=excel_source, columns=["A", "B"], start_data="Суббота",
                                                    end_data="None")
                write_msg(event.object.peer_id, ExcelSearcher.output_day_schedule, keyboard=main_keyboard)
            else:
                write_msg(event.object.peer_id, "Это точно команда:/", keyboard=main_keyboard)

# Authors of the project:
# 1-MachnevEgor_https://vk.com/machnev_egor
# 2-SchalimovDmitriy_https://vk.com/astronaut_without_spaceship
# 3-ArsenyKarimov_https://vk.com/@id222338543
# 4-MihailMarkov_https://vk.com/mixxxxail
# Contacts in email:
# 1-meb.official.com@gmail.com
# 2-dmitriy-shalimov@yandex.ru
# 3-arseny.karimov@gmail.com
# 4-mihailmarkov2004@gmail.com
