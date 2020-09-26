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
import vk_api as vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import json as json
from random import randint as randint
import datetime as datetime
# import other modules
from configurationFile import BotConfig as BotConfig
from dataProcessing import SourcesProtection
from workWithExcelFile import ExcelSearcher as ExcelSearcher

# system arrays
groups_id_array = ["187254286"]
users_id_array = []
# excel source variable
sources_protection = []
excel_source = ""
columns = []
# information about developers
about_bot = [
    "Данного бота по фану запилили рандомные челики из ПУМа. Этот бот отличается от всех других тем, что импортирует всю информацию из базы данных школы, а не тупо по написанным строкам разработчиков. Бот продуман, но не идеален, поэтому все вопросы можете задавать в беседу, прикреплённую к сообществу бота. Также хочется напомнить, что у нас есть discord сервер для разработчиков, на котором вы сможете найти себе команду для проекта, узнать что-то новое или присоединится к чье-то идеи:\nhttps://discord.gg/EmJKG5x😊"]
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
        [get_button(label="8-ой", color="positive"),
         get_button(label="9-ый", color="positive")],
        [get_button(label="10-ый", color="positive"),
         get_button(label="11-ый", color="positive")],
        [get_button(label="Назад", color="secondary")],
    ]
}

eight_class_keyboard = {
    "one_time": False,
    "buttons": [
        [get_button(label="8-1", color="positive"),
         get_button(label="8-2", color="positive")],
        [get_button(label="Назад", color="secondary")],
    ]
}

nine_class_keyboard = {
    "one_time": False,
    "buttons": [
        [get_button(label="9-1", color="positive"),
         get_button(label="9-2", color="positive"),
         get_button(label="9-3", color="positive")],
        [get_button(label="Назад", color="secondary")],
    ]
}

ten_class_keyboard = {
    "one_time": False,
    "buttons": [
        [get_button(label="10-1", color="positive"),
         get_button(label="10-2", color="positive"),
         get_button(label="10-3", color="positive")],
        [get_button(label="Назад", color="secondary")],
    ]
}

eleven_class_keyboard = {
    "one_time": False,
    "buttons": [
        [get_button(label="11-1", color="positive"),
         get_button(label="11-2", color="positive"),
         get_button(label="11-3", color="positive"),
         get_button(label="11-4", color="positive")],
        [get_button(label="Назад", color="secondary")],
    ]
}

choosing_day_of_week_keyboard = {
    "one_time": False,
    "buttons": [
        [get_button(label="Понедельник", color="positive"),
         get_button(label="Вторник", color="positive"),
         get_button(label="Среда", color="positive")],
        [get_button(label="Четверг", color="positive"),
         get_button(label="Пятница", color="positive"),
         get_button(label="Суббота", color="positive")],
        [get_button(label="Назад", color="secondary")],
    ]
}

# json for keyboard
main_keyboard = json.dumps(main_keyboard, ensure_ascii=False).encode("utf-8")
main_keyboard = str(main_keyboard.decode("utf-8"))
schedules_keyboard = json.dumps(schedules_keyboard, ensure_ascii=False).encode("utf-8")
schedules_keyboard = str(schedules_keyboard.decode("utf-8"))
select_call_class_keyboard = json.dumps(select_call_class_keyboard, ensure_ascii=False).encode("utf-8")
select_call_class_keyboard = str(select_call_class_keyboard.decode("utf-8"))
select_class_keyboard = json.dumps(select_class_keyboard, ensure_ascii=False).encode("utf-8")
select_class_keyboard = str(select_class_keyboard.decode("utf-8"))
eight_class_keyboard = json.dumps(eight_class_keyboard, ensure_ascii=False).encode("utf-8")
eight_class_keyboard = str(eight_class_keyboard.decode("utf-8"))
nine_class_keyboard = json.dumps(nine_class_keyboard, ensure_ascii=False).encode("utf-8")
nine_class_keyboard = str(nine_class_keyboard.decode("utf-8"))
ten_class_keyboard = json.dumps(ten_class_keyboard, ensure_ascii=False).encode("utf-8")
ten_class_keyboard = str(ten_class_keyboard.decode("utf-8"))
eleven_class_keyboard = json.dumps(eleven_class_keyboard, ensure_ascii=False).encode("utf-8")
eleven_class_keyboard = str(eleven_class_keyboard.decode("utf-8"))
choosing_day_of_week_keyboard = json.dumps(choosing_day_of_week_keyboard, ensure_ascii=False).encode("utf-8")
choosing_day_of_week_keyboard = str(choosing_day_of_week_keyboard.decode("utf-8"))


# sending messages
def write_msg(id, message, keyboard=None, sticker_id=None):
    # sending data to the terminal
    print(f"Responce: {''.join(message)}")
    if sticker_id != None:
        print(f"Sticker: {sticker_id}")
    # send the message
    vk.method("messages.send", {"peer_id": id, "sticker_id": sticker_id, "message": message, "keyboard": keyboard,
                                "random_id": randint(1, 100000000)})


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
            elif event.object.text.lower() == "учебники":
                write_msg(event.object.peer_id,
                          "Ой, сорян, забыл предупредить - т.к. бот на бэтке, нам нужны люди, которые помогут найти все электронные сканы учебников с 8 по 11 классы, мы постепенно набираем базу, но ещё нужно время😏",
                          keyboard=main_keyboard)
            elif event.object.text.lower() == "расписание":
                write_msg(event.object.peer_id, "Ок, только выбери какое🖖", keyboard=schedules_keyboard)
            elif event.object.text.lower() == "о боте":
                write_msg(event.object.peer_id, about_bot, keyboard=main_keyboard)
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
            elif event.object.text.lower() == "8-ой":
                write_msg(event.object.peer_id, "А какой из🙄", keyboard=eight_class_keyboard)
            elif event.object.text.lower() == "9-ый":
                write_msg(event.object.peer_id, "А какой из🙄", keyboard=nine_class_keyboard)
            elif event.object.text.lower() == "10-ый":
                write_msg(event.object.peer_id, "А какой из🙄", keyboard=ten_class_keyboard)
            elif event.object.text.lower() == "11-ый":
                write_msg(event.object.peer_id, "А какой из🙄", keyboard=eleven_class_keyboard)
            # 8 - assembling source
            elif event.object.text.lower() == "8-1":
                sources_protection.append(
                    [f"{event.object.peer_id}", "excelDatabase/8class/8class.xlsx", ["A", "B", "D"]])
                write_msg(event.object.peer_id, "Отлично, теперь выбери день недели🗓",
                          keyboard=choosing_day_of_week_keyboard)
            elif event.object.text.lower() == "8-2":
                sources_protection.append(
                    [f"{event.object.peer_id}", "excelDatabase/8class/8class.xlsx", ["A", "F", "H"]])
                write_msg(event.object.peer_id, "Отлично, теперь выбери день недели🗓",
                          keyboard=choosing_day_of_week_keyboard)
            # 9 - assembling source
            elif event.object.text.lower() == "9-1":
                sources_protection.append(
                    [f"{event.object.peer_id}", "excelDatabase/9class/9class.xlsx", ["A", "B", "D"]])
                write_msg(event.object.peer_id, "Отлично, теперь выбери день недели🗓",
                          keyboard=choosing_day_of_week_keyboard)
            elif event.object.text.lower() == "9-2":
                sources_protection.append(
                    [f"{event.object.peer_id}", "excelDatabase/9class/9class.xlsx", ["A", "F", "H"]])
                write_msg(event.object.peer_id, "Отлично, теперь выбери день недели🗓",
                          keyboard=choosing_day_of_week_keyboard)
            elif event.object.text.lower() == "9-3":
                sources_protection.append(
                    [f"{event.object.peer_id}", "excelDatabase/9class/9class.xlsx", ["A", "J", "L"]])
                write_msg(event.object.peer_id, "Отлично, теперь выбери день недели🗓",
                          keyboard=choosing_day_of_week_keyboard)
            # 10 - assembling source
            elif event.object.text.lower() == "10-1":
                sources_protection.append(
                    [f"{event.object.peer_id}", "excelDatabase/10class/10class.xlsx", ["A", "B", "D"]])
                write_msg(event.object.peer_id, "Отлично, теперь выбери день недели🗓",
                          keyboard=choosing_day_of_week_keyboard)
            elif event.object.text.lower() == "10-2":
                sources_protection.append(
                    [f"{event.object.peer_id}", "excelDatabase/10class/10class.xlsx", ["A", "F", "H"]])
                write_msg(event.object.peer_id, "Отлично, теперь выбери день недели🗓",
                          keyboard=choosing_day_of_week_keyboard)
            elif event.object.text.lower() == "10-3":
                sources_protection.append(
                    [f"{event.object.peer_id}", "excelDatabase/10class/10class.xlsx", ["A", "J", "L"]])
                write_msg(event.object.peer_id, "Отлично, теперь выбери день недели🗓",
                          keyboard=choosing_day_of_week_keyboard)
            # 11 - assembling source
            elif event.object.text.lower() == "11-1":
                sources_protection.append(
                    [f"{event.object.peer_id}", "excelDatabase/11class/11class.xlsx", ["A", "B", "D"]])
                write_msg(event.object.peer_id, "Отлично, теперь выбери день недели🗓",
                          keyboard=choosing_day_of_week_keyboard)
            elif event.object.text.lower() == "11-2":
                sources_protection.append(
                    [f"{event.object.peer_id}", "excelDatabase/11class/11class.xlsx", ["A", "F", "H"]])
                write_msg(event.object.peer_id, "Отлично, теперь выбери день недели🗓",
                          keyboard=choosing_day_of_week_keyboard)
            elif event.object.text.lower() == "11-3":
                sources_protection.append(
                    [f"{event.object.peer_id}", "excelDatabase/11class/11class.xlsx", ["A", "J", "L"]])
                write_msg(event.object.peer_id, "Отлично, теперь выбери день недели🗓",
                          keyboard=choosing_day_of_week_keyboard)
            elif event.object.text.lower() == "11-4":
                sources_protection.append(
                    [f"{event.object.peer_id}", "excelDatabase/11class/11class.xlsx", ["A", "N", "P"]])
                write_msg(event.object.peer_id, "Отлично, теперь выбери день недели🗓",
                          keyboard=choosing_day_of_week_keyboard)
            # choosing day of week keyboard
            elif (event.object.text.lower() == "понедельник"):
                SourcesProtection.analizing_sources_protection(sources_protection=sources_protection,
                                                               user_id=f"{event.object.peer_id}", limit_users_data=100)
                sources_protection = SourcesProtection.new_sources_protection
                ExcelSearcher.selective_data_search(excel_source=SourcesProtection.source_for_user,
                                                    columns=SourcesProtection.columns_for_user, extra_cells=1,
                                                    start_data="Понедельник", end_data="None")
                write_msg(event.object.peer_id, f"\n{ExcelSearcher.output_day_schedule}", keyboard=main_keyboard)
            elif (event.object.text.lower() == "вторник"):
                SourcesProtection.analizing_sources_protection(sources_protection=sources_protection,
                                                               user_id=f"{event.object.peer_id}", limit_users_data=100)
                sources_protection = SourcesProtection.new_sources_protection
                ExcelSearcher.selective_data_search(excel_source=SourcesProtection.source_for_user,
                                                    columns=SourcesProtection.columns_for_user, extra_cells=1,
                                                    start_data="Вторник", end_data="None")
                write_msg(event.object.peer_id, f"\n{ExcelSearcher.output_day_schedule}", keyboard=main_keyboard)
            elif (event.object.text.lower() == "среда"):
                SourcesProtection.analizing_sources_protection(sources_protection=sources_protection,
                                                               user_id=f"{event.object.peer_id}", limit_users_data=100)
                sources_protection = SourcesProtection.new_sources_protection
                ExcelSearcher.selective_data_search(excel_source=SourcesProtection.source_for_user,
                                                    columns=SourcesProtection.columns_for_user, extra_cells=1,
                                                    start_data="Среда", end_data="None")
                write_msg(event.object.peer_id, f"\n{ExcelSearcher.output_day_schedule}", keyboard=main_keyboard)
            elif (event.object.text.lower() == "четверг"):
                SourcesProtection.analizing_sources_protection(sources_protection=sources_protection,
                                                               user_id=f"{event.object.peer_id}", limit_users_data=100)
                sources_protection = SourcesProtection.new_sources_protection
                ExcelSearcher.selective_data_search(excel_source=SourcesProtection.source_for_user,
                                                    columns=SourcesProtection.columns_for_user, extra_cells=1,
                                                    start_data="Четверг", end_data="None")
                write_msg(event.object.peer_id, f"\n{ExcelSearcher.output_day_schedule}", keyboard=main_keyboard)
            elif (event.object.text.lower() == "пятница"):
                SourcesProtection.analizing_sources_protection(sources_protection=sources_protection,
                                                               user_id=f"{event.object.peer_id}", limit_users_data=100)
                sources_protection = SourcesProtection.new_sources_protection
                ExcelSearcher.selective_data_search(excel_source=SourcesProtection.source_for_user,
                                                    columns=SourcesProtection.columns_for_user, extra_cells=1,
                                                    start_data="Пятница", end_data="None")
                write_msg(event.object.peer_id, f"\n{ExcelSearcher.output_day_schedule}", keyboard=main_keyboard)
            elif (event.object.text.lower() == "суббота"):
                SourcesProtection.analizing_sources_protection(sources_protection=sources_protection,
                                                               user_id=f"{event.object.peer_id}", limit_users_data=100)
                sources_protection = SourcesProtection.new_sources_protection
                ExcelSearcher.selective_data_search(excel_source=SourcesProtection.source_for_user,
                                                    columns=SourcesProtection.columns_for_user, extra_cells=1,
                                                    start_data="Суббота", end_data="None")
                write_msg(event.object.peer_id, f"\n{ExcelSearcher.output_day_schedule}", keyboard=main_keyboard)
            else:
                write_msg(event.object.peer_id, "Это точно команда:/", keyboard=main_keyboard)
            # sending data to the terminal
            print("-----------------------------")

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
