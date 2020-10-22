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
import requests as requests
from random import randint as randint
import time as time
import datetime as datetime
# import other modules
from configurationFile import BotConfig as BotConfig
from workWithUsersDatabase import UserSearcher
from workWithExcelFile import ExcelSearcher as ExcelSearcher

# full error log output(without auto-reconnection)
error_checking_switch = False
# time to restart the bot
reboot_time = 5

# system array
community_id = ["187254286"]
# talk to the reservation database
conversation_for_data_reservation_id = 2000000004

# all groups for all classes of the Mai pre-University
eight_class_groups = ["М-8-1-1, Ф-8-1", "М-8-1-2, Ф-8-1", "М-8-1-2, Ф-8-2", "М-8-2-1, Ф-8-1", "М-8-2-1, Ф-8-2",
                      "М-8-2-2, Ф-8-2"]
nine_class_groups = ["М-9-1, Ф-9-1, Р-9-1-2", "М-9-1, Ф-9-1, Р-9-2-1", "М-9-1, Ф-9-1, Р-9-3-1", "М-9-1, Ф-9-1, Р-9-3-2",
                     "М-9-1, Ф-9-2, Р-9-1-1", "М-9-1, Ф-9-2, Р-9-1-2", "М-9-1, Ф-9-2, Р-9-2-1", "М-9-1, Ф-9-2, Р-9-2-2",
                     "М-9-1, Ф-9-2, Р-9-3-1", "М-9-1, Ф-9-2, Р-9-3-2", "М-9-2, Ф-9-1, Р-9-1-2", "М-9-2, Ф-9-1, Р-9-2-1",
                     "М-9-2, Ф-9-1, Р-9-3-1", "М-9-2, Ф-9-1, Р-9-3-2", "М-9-2, Ф-9-2, Р-9-1-1", "М-9-2, Ф-9-2, Р-9-1-2",
                     "М-9-2, Ф-9-2, Р-9-2-2", "М-9-2, Ф-9-2, Р-9-3-1", "М-9-2, Ф-9-2, Р-9-3-2", "М-9-3, Ф-9-3, Р-9-1-1",
                     "М-9-3, Ф-9-3, Р-9-1-2", "М-9-3, Ф-9-3, Р-9-2-1", "М-9-3, Ф-9-3, Р-9-2-2", "М-9-3, Ф-9-3, Р-9-3-2"]
ten_class_groups = ["М-10-1, А-10-1", "М-10-1, А-10-2", "М-10-1, А-10-3", "М-10-2, А-10-1", "М-10-2, А-10-2",
                    "М-10-2, А-10-3", "М-10-3, А-10-1", "М-10-3, А-10-2", "М-10-3, А-10-3"]
eleven_class_groups = ["М1, Ф1, М-1-1, Р-1-4, Л3", "М1, Ф1, М-1-1, Р-1-4, Л4", "М1, Ф1, М-1-1, Р-3, Л-3",
                       "М1, Ф1, М-2-1, Р1, Л3", "М1, Ф1, М-3-1, Р1, Л3", "М1, Ф1, М-3-1, Р-2, Л3",
                       "М1, Ф1, М-3-1, Р-3, Л3", "М1, Ф4, М-2-1, Р1, Л3", "М1, Ф4, М-3-1, Р1, Л3",
                       "М2, Ф2, М-2-1, Р1, Л2", "М2, Ф2, М-2-1, Р-3, Л2", "М2, Ф2, М-2-1, Р-3, Л3",
                       "М2, Ф2, М-2-1, Р4, Л4", "М2, Ф2, М-3-1, Р1, Л1", "М2, Ф2, М-3-1, Р1, Л2",
                       "М2, Ф2, М-3-1, Р2, Л2", "М2, Ф2, М-3-1, Р4, Л4", "М3, Ф1, М-1-1, Р4, Л4",
                       "М3, Ф1, М-2-1, Р-1, Л3", "М3, Ф1, М-2-1, Р3, Л2", "М3, Ф1, М-2-1, Р3, Л3",
                       "М3, Ф1, М-2-1, Р4, Л4", "М3, Ф1, М-3-1, Р1, Л2", "М3, Ф1, М-3-1, Р2, Л1",
                       "М3, Ф1, М-3-1, Р4, Л4", "М3, Ф4, М-1-1, Р1, Л1", "М3, Ф4, М-1-1, Р4, Л4",
                       "М3, Ф4, М-2-1, Р1, Л1", "М3, Ф4, М-2-1, Р3, Л2", "М3, Ф4, М-2-1, Р4, Л4",
                       "М3, Ф4, М-3-1, Р1, Л2", "М3, Ф4, М-3-1, Р3, Л2", "М3, Ф4, М-3-1, Р4, Л4",
                       "М4, Ф1, М-4-1, Р1, Л1", "М4, Ф1, М-4-1, Р2, Л1", "М4, Ф1, М-4-1, Р4, Л4",
                       "М4, Ф1, М-4-2, Р2, Л1", "М4, Ф1, М-4-2, Р4, Л4", "М4, Ф4, М-4-1, Р1, Л1",
                       "М4, Ф4, М-4-1, Р2, Л1", "М4, Ф4, М-4-1, Р3, Л1", "М4, Ф4, М-4-1, Р3, Л1",
                       "М4, Ф4, М-4-1, Р4, Л4", "М4, Ф4, М-4-2, Р1, Л1", "М4, Ф4, М-4-2, Р2, Л1",
                       "М4, Ф4, М-4-2, Р2, Л3", "М4, Ф4, М-4-2, Р4, Л4"]

# array for the back button and welcome words
buttons_back = ["здравствуй", "привет", "хай", "куку", "ку", "салам", "саламалейкум", "здарова", "дыдова", "начать",
                "главное меню", "меню", "плитки", "клавиатура", "назад", "hello", "hey", "hi", "qq", "q", "start",
                "main menu", "menu", "tiles", "keyboard", "back"]
ru_greetings_bot = ["здравствуй", "привет", "хай", "ку", "салам", "здарова", "дыдова"]
eng_greetings_bot = ["hello", "hey", "hi", "qq", "q"]

# information about developers
about_bot = [
    "Данного бота по фану запилили рандомные челики из ПУМа. Этот бот отличается от всех других тем, что импортирует всю информацию из базы данных школы, а не тупо по написанным строкам разработчиков. Бот продуман, но не идеален, поэтому все вопросы можете задавать в беседу, прикреплённую к сообществу бота. Также хочется напомнить, что у нас есть discord сервер для разработчиков, на котором вы сможете найти себе команду для проекта, узнать что-то новое или присоединится к чьей-то идеи:\nhttps://smtechnology.info😊",
    "Не забывайте, что всю актуальную информацию о боте вы можете найти на стене нашего сообщества, поэтому, если бот не отвечает, вы знаете, что делать😉"]
# schedule calls
eight_nine_schedule_calls = "Расписание звонков:\n1. 9:00 - 9:45\n2. 9:50 - 10:35\n3. 10:55 - 11:40\n4. 11:50 - 12:35\n5. 12:45 - 13:30\n6. 13:50 - 14:35\n7. 14:45 - 15:30\n8. 15:40 - 16:25\n9. 16:30 - 17:15\n10. 17:20 - 18:05"
ten_eleven_schedule_calls = "Расписание звонков:\n1. 9:00 - 9:45\n2. 9:50 - 10:35\n3. 10:45 - 11:30\n4. 11:50 - 12:35\n5. 12:45 - 13:30\n6. 13:40 - 14:25\n7. 14:45 - 15:30\n8. 15:40 - 16:25\n9. 16:30 - 17:15\n10. 17:20 - 18:05"


# algorithm for processing user requests
def bot_processing():
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
            [get_button(label="Помощь", color="primary"),
             get_button(label="О боте", color="primary")],
        ]
    }

    before_registration_keyboard = {
        "one_time": False,
        "buttons": [
            [get_button(label="Регистрация", color="positive")],
            [get_button(label="Помощь", color="primary"),
             get_button(label="О боте", color="primary")],
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
    before_registration_keyboard = json.dumps(before_registration_keyboard, ensure_ascii=False).encode("utf-8")
    before_registration_keyboard = str(before_registration_keyboard.decode("utf-8"))
    schedules_keyboard = json.dumps(schedules_keyboard, ensure_ascii=False).encode("utf-8")
    schedules_keyboard = str(schedules_keyboard.decode("utf-8"))
    select_call_class_keyboard = json.dumps(select_call_class_keyboard, ensure_ascii=False).encode("utf-8")
    select_call_class_keyboard = str(select_call_class_keyboard.decode("utf-8"))
    choosing_day_of_week_keyboard = json.dumps(choosing_day_of_week_keyboard, ensure_ascii=False).encode("utf-8")
    choosing_day_of_week_keyboard = str(choosing_day_of_week_keyboard.decode("utf-8"))

    # sending messages
    def write_msg(user_id, message, keyboard=None, sticker_id=None, attachment=None):
        # sending data to the terminal
        print("Responce:", "".join(message))
        if sticker_id != None:
            print(f"Sticker: {sticker_id}")
        if attachment != None:
            print(f"Attachment: {attachment}")
        # keyboard if the person is not registered yet
        if keyboard == main_keyboard:
            UserSearcher.searching_user_in_database(database_source="workWithUsersDatabase/UsersDatabase.txt",
                                                    user_id=f"id{user_id}")
            if UserSearcher.presence_user == []:
                keyboard = before_registration_keyboard
        # send the message
        vk.method("messages.send",
                  {"peer_id": user_id, "message": message, "keyboard": keyboard, "sticker_id": sticker_id,
                   "attachment": attachment, "random_id": randint(1, 100000000)})

    # sending a database from a conversation to reserve data
    def sending_and_reserving_database(conversation_id, database_source, message):
        # sending data to the terminal
        print(f"Sending and reserving a database...({conversation_id}, {database_source})")
        # sending and reserving data
        get_serverAccess = vk.method("docs.getMessagesUploadServer", {"type": "doc", "peer_id": conversation_id})
        get_serverLink = requests.post(get_serverAccess["upload_url"],
                                       files={"file": open(database_source, "rb")}).json()
        save_docFile = vk.method("docs.save", {"file": get_serverLink["file"]})["doc"]
        attachment = "doc{}_{}".format(save_docFile["owner_id"], save_docFile["id"])
        vk.method("messages.send",
                  {"peer_id": conversation_for_data_reservation_id, "message": message, "attachment": attachment,
                   "random_id": randint(1, 10000000)})

    # longpoll
    longpoll = VkBotLongPoll(vk, group_id=community_id)
    # response logic
    for event in longpoll.listen():
        # processing a new message
        if (event.type == VkBotEventType.MESSAGE_NEW) and (event.object.peer_id == event.object.from_id):
            # sending data to the terminal
            print(datetime.datetime.today())
            print(f"Message from-->https://vk.com/id{event.object.peer_id}")
            print(f"Message content: {event.object.text}")
            # if the request is from in private messages
            if event.object.peer_id == event.object.from_id:
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
                elif event.object.text.lower() == "помощь":
                    write_msg(event.object.peer_id,
                              "У тебя есть вопросы? - не волнуйся, ведь ты их всегда можешь задать в беседе, прикреплённой к сообществу🎯\nhttps://vk.me/join/FhSVyJp7fYT0fM805_KTHNWPctDNa79JGsI=",
                              keyboard=main_keyboard)
                elif event.object.text.lower() == "о боте":
                    write_msg(event.object.peer_id, about_bot[0], keyboard=main_keyboard)
                    write_msg(event.object.peer_id, about_bot[1], keyboard=main_keyboard,
                              attachment="photo222338543_457245836_657bc0cfbecac6a616")
                # schedules keyboard
                elif event.object.text.lower() == "звонков":
                    write_msg(event.object.peer_id, "Такс, и ещё выбери для каких классов🤔",
                              keyboard=select_call_class_keyboard)
                elif event.object.text.lower() == "уроков":
                    write_msg(event.object.peer_id,
                              "Хмм, теперь выбери день😼\nКста, держи график занятий во время очно-дистанционного обучения:",
                              keyboard=choosing_day_of_week_keyboard,
                              attachment="photo222338543_457245837_c353f13b4997d1ff78")
                # select call class keyboard
                elif event.object.text.lower() == "8-9":
                    write_msg(event.object.peer_id, eight_nine_schedule_calls, keyboard=main_keyboard)
                elif event.object.text.lower() == "10-11":
                    write_msg(event.object.peer_id, ten_eleven_schedule_calls, keyboard=main_keyboard)
                # choosing day of week keyboard
                elif event.object.text.lower() == "понедельник":
                    UserSearcher.searching_user_in_database(database_source="workWithUsersDatabase/UsersDatabase.txt",
                                                            user_id=f"id{event.object.peer_id}")
                    if UserSearcher.presence_user == []:
                        write_msg(event.object.peer_id,
                                  "Такс, тебя же нет в базе. Нажми на плитку -Регистрация- в главном меню, чтобы занести свои данные для выдачи расписания📖",
                                  keyboard=main_keyboard)
                    else:
                        write_msg(event.object.peer_id, "Поиск актуального расписания для тебя🔎",
                                  keyboard=main_keyboard)
                        vk.method('messages.setActivity', {'peer_id': event.object.peer_id, 'type': 'typing'})
                        ExcelSearcher.selective_data_search(excel_source=UserSearcher.presence_user[2],
                                                            sheet_name=UserSearcher.presence_user[3],
                                                            columns=UserSearcher.presence_user[4],
                                                            extra_cells=UserSearcher.presence_user[5],
                                                            start_data="Понедельник", end_data="None")
                        write_msg(event.object.peer_id, f"\n{ExcelSearcher.output_day_schedule}",
                                  keyboard=main_keyboard)
                elif event.object.text.lower() == "вторник":
                    UserSearcher.searching_user_in_database(database_source="workWithUsersDatabase/UsersDatabase.txt",
                                                            user_id=f"id{event.object.peer_id}")
                    if UserSearcher.presence_user == []:
                        write_msg(event.object.peer_id,
                                  "Такс, тебя же нет в базе. Нажми на плитку -Регистрация- в главном меню, чтобы занести свои данные для выдачи расписания📖",
                                  keyboard=main_keyboard)
                    else:
                        write_msg(event.object.peer_id, "Поиск актуального расписания для тебя🔎",
                                  keyboard=main_keyboard)
                        vk.method('messages.setActivity', {'peer_id': event.object.peer_id, 'type': 'typing'})
                        ExcelSearcher.selective_data_search(excel_source=UserSearcher.presence_user[2],
                                                            sheet_name=UserSearcher.presence_user[3],
                                                            columns=UserSearcher.presence_user[4],
                                                            extra_cells=UserSearcher.presence_user[5],
                                                            start_data="Вторник", end_data="None")
                        write_msg(event.object.peer_id, f"\n{ExcelSearcher.output_day_schedule}",
                                  keyboard=main_keyboard)
                elif event.object.text.lower() == "среда":
                    UserSearcher.searching_user_in_database(database_source="workWithUsersDatabase/UsersDatabase.txt",
                                                            user_id=f"id{event.object.peer_id}")
                    if UserSearcher.presence_user == []:
                        write_msg(event.object.peer_id,
                                  "Такс, тебя же нет в базе. Нажми на плитку -Регистрация- в главном меню, чтобы занести свои данные для выдачи расписания📖",
                                  keyboard=main_keyboard)
                    else:
                        write_msg(event.object.peer_id, "Поиск актуального расписания для тебя🔎",
                                  keyboard=main_keyboard)
                        vk.method('messages.setActivity', {'peer_id': event.object.peer_id, 'type': 'typing'})
                        ExcelSearcher.selective_data_search(excel_source=UserSearcher.presence_user[2],
                                                            sheet_name=UserSearcher.presence_user[3],
                                                            columns=UserSearcher.presence_user[4],
                                                            extra_cells=UserSearcher.presence_user[5],
                                                            start_data="Среда", end_data="None")
                        write_msg(event.object.peer_id, f"\n{ExcelSearcher.output_day_schedule}",
                                  keyboard=main_keyboard)
                elif event.object.text.lower() == "четверг":
                    UserSearcher.searching_user_in_database(database_source="workWithUsersDatabase/UsersDatabase.txt",
                                                            user_id=f"id{event.object.peer_id}")
                    if UserSearcher.presence_user == []:
                        write_msg(event.object.peer_id,
                                  "Такс, тебя же нет в базе. Нажми на плитку -Регистрация- в главном меню, чтобы занести свои данные для выдачи расписания📖",
                                  keyboard=main_keyboard)
                    else:
                        write_msg(event.object.peer_id, "Поиск актуального расписания для тебя🔎",
                                  keyboard=main_keyboard)
                        vk.method('messages.setActivity', {'peer_id': event.object.peer_id, 'type': 'typing'})
                        ExcelSearcher.selective_data_search(excel_source=UserSearcher.presence_user[2],
                                                            sheet_name=UserSearcher.presence_user[3],
                                                            columns=UserSearcher.presence_user[4],
                                                            extra_cells=UserSearcher.presence_user[5],
                                                            start_data="Четверг", end_data="None")
                        write_msg(event.object.peer_id, f"\n{ExcelSearcher.output_day_schedule}",
                                  keyboard=main_keyboard)
                elif event.object.text.lower() == "пятница":
                    UserSearcher.searching_user_in_database(database_source="workWithUsersDatabase/UsersDatabase.txt",
                                                            user_id=f"id{event.object.peer_id}")
                    if UserSearcher.presence_user == []:
                        write_msg(event.object.peer_id,
                                  "Такс, тебя же нет в базе. Нажми на плитку -Регистрация- в главном меню, чтобы занести свои данные для выдачи расписания📖",
                                  keyboard=main_keyboard)
                    else:
                        write_msg(event.object.peer_id, "Поиск актуального расписания для тебя🔎",
                                  keyboard=main_keyboard)
                        vk.method('messages.setActivity', {'peer_id': event.object.peer_id, 'type': 'typing'})
                        ExcelSearcher.selective_data_search(excel_source=UserSearcher.presence_user[2],
                                                            sheet_name=UserSearcher.presence_user[3],
                                                            columns=UserSearcher.presence_user[4],
                                                            extra_cells=UserSearcher.presence_user[5],
                                                            start_data="Пятница", end_data="None")
                        write_msg(event.object.peer_id, f"\n{ExcelSearcher.output_day_schedule}",
                                  keyboard=main_keyboard)
                elif event.object.text.lower() == "суббота":
                    UserSearcher.searching_user_in_database(database_source="workWithUsersDatabase/UsersDatabase.txt",
                                                            user_id=f"id{event.object.peer_id}")
                    if UserSearcher.presence_user == []:
                        write_msg(event.object.peer_id,
                                  "Такс, тебя же нет в базе. Нажми на плитку -Регистрация- в главном меню, чтобы занести свои данные для выдачи расписания📖",
                                  keyboard=main_keyboard)
                    else:
                        write_msg(event.object.peer_id, "Поиск актуального расписания для тебя🔎",
                                  keyboard=main_keyboard)
                        vk.method('messages.setActivity', {'peer_id': event.object.peer_id, 'type': 'typing'})
                        ExcelSearcher.selective_data_search(excel_source=UserSearcher.presence_user[2],
                                                            sheet_name=UserSearcher.presence_user[3],
                                                            columns=UserSearcher.presence_user[4],
                                                            extra_cells=UserSearcher.presence_user[5],
                                                            start_data="Суббота", end_data="None")
                        write_msg(event.object.peer_id, f"\n{ExcelSearcher.output_day_schedule}",
                                  keyboard=main_keyboard)
                # registration - instruction
                elif event.object.text.lower() == "регистрация":
                    UserSearcher.searching_user_in_database(database_source="workWithUsersDatabase/UsersDatabase.txt",
                                                            user_id=f"id{event.object.peer_id}")
                    if UserSearcher.presence_user == []:
                        write_msg(event.object.peer_id,
                                  f"Теперь ты можешь осуществить регистрацию прямо в боте! Для этого тебе просто нужно написать свою группу, которая указана в индивидуальном расписании(название группы обязательно вводить русскими символами, если у тебя не получится ввести номер группы с первого раза - попробуй ещё раз)😜\nДля удобства вывожу тебе список всех групп в школе:\n8️⃣Класс: {'; '.join(eight_class_groups)}\n9️⃣Класс: {'; '.join(nine_class_groups)}\n1️⃣0️⃣Класс: {'; '.join(ten_class_groups)}\n1️⃣1️⃣Класс: {'; '.join(eleven_class_groups)}\nЕсли нужна помощь, то пиши в беседу, прикрепленную к сообществу:\nhttps://vk.me/join/FhSVyJp7fYT0fM805_KTHNWPctDNa79JGsI=",
                                  keyboard=main_keyboard)
                    else:
                        write_msg(event.object.peer_id,
                                  f"Ты уже зарегистрирован - если всё работает отлично, то ты также можешь продолжать пользоваться ботом. Если же у тебя есть какие-либо вопросы или ты сменил группу, то пиши в беседу, прикреплённую к сообществу⚙\nhttps://vk.me/join/FhSVyJp7fYT0fM805_KTHNWPctDNa79JGsI=",
                                  keyboard=main_keyboard)
                # registration - the process of entering users in the database
                elif (event.object.text.upper() in eight_class_groups) or (
                        event.object.text.upper() in nine_class_groups) or (
                        event.object.text.upper() in ten_class_groups) or (
                        event.object.text.upper() in eleven_class_groups):
                    UserSearcher.searching_user_in_database(database_source="workWithUsersDatabase/UsersDatabase.txt",
                                                            user_id=f"id{event.object.peer_id}")
                    if UserSearcher.presence_user == []:
                        get_last_name = vk.method("users.get", {"user_ids": event.object.peer_id})[0]["last_name"]
                        get_first_name = vk.method("users.get", {"user_ids": event.object.peer_id})[0]["first_name"]
                        if event.object.text.upper() in eight_class_groups:
                            UserSearcher.adding_user_in_database(
                                database_source="workWithUsersDatabase/UsersDatabase.txt",
                                full_name=f"{get_last_name} {get_first_name}", user_id=f"id{event.object.peer_id}",
                                source_for_user="8class", sheet_name=event.object.text.upper(),
                                columns_for_user=['A', 'B', 'D', 'E'], extra_cells=1)
                            sending_and_reserving_database(conversation_id=event.object.from_id,
                                                           database_source="workWithUsersDatabase/UsersDatabase.txt",
                                                           message=f"К нам присоединился новый пользователь - {get_last_name} {get_first_name}(id{event.object.peer_id} | 8class | {event.object.text.upper()})🚀")
                            write_msg(event.object.peer_id, "Поздравляю! Регистрация прошла успешно✅",
                                      keyboard=main_keyboard)
                        elif event.object.text.upper() in nine_class_groups:
                            UserSearcher.adding_user_in_database(
                                database_source="workWithUsersDatabase/UsersDatabase.txt",
                                full_name=f"{get_last_name} {get_first_name}", user_id=f"id{event.object.peer_id}",
                                source_for_user="9class", sheet_name=event.object.text.upper(),
                                columns_for_user=['A', 'B', 'D', 'E'], extra_cells=1)
                            sending_and_reserving_database(conversation_id=event.object.from_id,
                                                           database_source="workWithUsersDatabase/UsersDatabase.txt",
                                                           message=f"К нам присоединился новый пользователь - {get_last_name} {get_first_name}(id{event.object.peer_id} | 9class | {event.object.text.upper()})🚀")
                            write_msg(event.object.peer_id, "Поздравляю! Регистрация прошла успешно✅",
                                      keyboard=main_keyboard)
                        elif event.object.text.upper() in ten_class_groups:
                            UserSearcher.adding_user_in_database(
                                database_source="workWithUsersDatabase/UsersDatabase.txt",
                                full_name=f"{get_last_name} {get_first_name}", user_id=f"id{event.object.peer_id}",
                                source_for_user="10class", sheet_name=event.object.text.upper(),
                                columns_for_user=['A', 'B', 'D', 'E'], extra_cells=1)
                            sending_and_reserving_database(conversation_id=event.object.from_id,
                                                           database_source="workWithUsersDatabase/UsersDatabase.txt",
                                                           message=f"К нам присоединился новый пользователь - {get_last_name} {get_first_name}(id{event.object.peer_id} | 10class | {event.object.text.upper()})🚀")
                            write_msg(event.object.peer_id, "Поздравляю! Регистрация прошла успешно✅",
                                      keyboard=main_keyboard)
                        elif event.object.text.upper() in eleven_class_groups:
                            UserSearcher.adding_user_in_database(
                                database_source="workWithUsersDatabase/UsersDatabase.txt",
                                full_name=f"{get_last_name} {get_first_name}", user_id=f"id{event.object.peer_id}",
                                source_for_user="11class", sheet_name=event.object.text.upper(),
                                columns_for_user=['A', 'B', 'D', 'E'], extra_cells=1)
                            sending_and_reserving_database(conversation_id=event.object.from_id,
                                                           database_source="workWithUsersDatabase/UsersDatabase.txt",
                                                           message=f"К нам присоединился новый пользователь - {get_last_name} {get_first_name}(id{event.object.peer_id} | 11class | {event.object.text.upper()})🚀")
                            write_msg(event.object.peer_id, "Поздравляю! Регистрация прошла успешно✅",
                                      keyboard=main_keyboard)
                    else:
                        if event.object.text.upper() == UserSearcher.presence_user[3]:
                            write_msg(event.object.peer_id,
                                      "Да-да, всё внесено верно - ты есть в базе. Если есть какие-то вопросы, то пиши в беседу, прикреплённую к сообществу🗿\nhttps://vk.me/join/FhSVyJp7fYT0fM805_KTHNWPctDNa79JGsI=",
                                      keyboard=main_keyboard)
                        else:
                            write_msg(event.object.peer_id,
                                      f"Ого - похоже ты хочешь изменить группу! Напиши в беседу, прикреплённую к сообществу, чтобы мы редактировали твои данные✍\nhttps://vk.me/join/FhSVyJp7fYT0fM805_KTHNWPctDNa79JGsI=",
                                      keyboard=main_keyboard)
                # get your data from the database
                elif event.object.text.lower() in ["я", "кто я", "хто я", "мои данные"]:
                    UserSearcher.searching_user_in_database(database_source="workWithUsersDatabase/UsersDatabase.txt",
                                                            user_id=f"id{event.object.peer_id}")
                    if UserSearcher.presence_user != []:
                        write_msg(event.object.peer_id,
                                  f"Вот твои данные, которые ты внёс при регистрации: {UserSearcher.presence_user[0]} | {UserSearcher.presence_user[1]} | {UserSearcher.presence_user[2]} | {UserSearcher.presence_user[3]}💾",
                                  keyboard=main_keyboard)
                    else:
                        write_msg(event.object.peer_id,
                                  f"Ты ещё не зарегистрировался, бот пока знает про тебя только это: id{event.object.peer_id}📡",
                                  keyboard=main_keyboard)
                # 3301 - easter egg
                elif event.object.text.lower() == "пасхалка":
                    write_msg(event.object.peer_id,
                              "Пасхалка?! Вау, в боте есть пасхалка! Приступим, есть шифр, указанный в пикче ниже - расшифруй его и отпишись в общую беседу сообщества(понимаем, что довольно сложно, поэтому даём две подсказки: ascii, tenet)",
                              keyboard=main_keyboard, attachment="photo222338543_457245838_d3e257103e69dd2d75")
                # check for updates
                elif event.object.text.lower() == "проверить обновления":
                    write_msg(event.object.peer_id,
                              "Оооу да - а вот и долгожданное обновление! Мы славно поработали и надеемся, что тебе всё понравится😎",
                              keyboard=main_keyboard)
                # unrecognized command
                else:
                    write_msg(event.object.peer_id, "По-моему ты вводишь что-то не так, попробуй ещё раз😕",
                              keyboard=main_keyboard)
                # sending data to the terminal
                print("-----------------------------")


# starting the bot logic
if __name__ == "__main__":
    if error_checking_switch != True:
        # for a permanent bot job with auto-reconnection
        while True:
            try:
                bot_processing()
            except Exception as E:
                # sending data to the terminal
                print("-----------------------------")
                print(datetime.datetime.today())
                print("!!!  The bot is disabled  !!!")
                print(f"Reason: {E}")
                print("-----------------------------")
                time.sleep(reboot_time)
                print("!!!    Reconnect, wait    !!!")
    else:
        # starting with the log output of the error
        bot_processing()

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
