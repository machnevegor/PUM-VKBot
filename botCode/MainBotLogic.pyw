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

# import the main modules for the bot
from threading import Thread as Thread
import vk_api as vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import telebot as telebot
from telebot import types as types
import json as json
import requests as requests
from random import randint as randint
import time as time
import datetime as datetime
import os as os
# import of other self-written modules
from specialScripts import MailingSchedules as MailingSchedules
from specialScripts import TelegramAlerts as TelegramAlerts
from configurationFile import BotConfig as BotConfig
from workWithUsersDatabase import UserSearcher as UserSearcher
from workWithExcelFile import ExcelSearcher as ExcelSearcher
from specialScripts import CompilationNews as CompilationNews


# the main logic of the vk bot: response to messages, mailing
def work_of_the_main_VK_bot():
    # initializing work with the vk api, launching the bot into the network
    global main_vk_session
    main_vk_session = vk_api.VkApi(token=f"{BotConfig.VK_BotToken}")
    main_vk_session._auth_token()
    main_vk_session.get_api()
    # sending data to the terminal about connecting the bot to the network
    print("-----------------------------")
    print("Bot launched into the network")
    print("-----------------------------")

    # creating a button object in a shared keyboard
    def get_button(label, color, payload=""):
        return {
            "action": {
                "type": "text",
                "payload": json.dumps(payload),
                "label": label
            },
            "color": color
        }

    # creating a dynamic keyboard with settings for the user
    def create_settings_keyboard(keyboard_user_id):
        presence_user = UserSearcher.searching_user_in_database(
            database_source="workWithUsersDatabase/UsersDatabase.txt", user_id=keyboard_user_id)
        settings_keyboard = {
            "one_time": False,
            "buttons": [
                [get_button(label="Автоматическая рассылка расписания",
                            color=("positive" if presence_user[6] != 0 else "negative"))],
                [get_button(label="Посты от администрации из Telegram",
                            color=("positive" if presence_user[8] != 0 else "negative"))],
                [get_button(label="Назад", color="secondary"),
                 get_button(label="Помощь", color="secondary")]
            ]
        }
        return str(json.dumps(settings_keyboard, ensure_ascii=False).encode("utf-8").decode("utf-8"))

    # create all static keyboards that will be provided to users
    main_keyboard = {
        "one_time": False,
        "buttons": [
            [get_button(label="Новости", color="positive"),
             get_button(label="Расписание", color="positive")],
            [get_button(label="Настройки", color="primary"),
             get_button(label="О боте", color="primary")]
        ]
    }

    before_registration_keyboard = {
        "one_time": False,
        "buttons": [
            [get_button(label="Регистрация", color="positive")],
            [get_button(label="Помощь", color="primary"),
             get_button(label="Звонки", color="primary"),
             get_button(label="О боте", color="primary")]
        ]
    }

    schedules_keyboard = {
        "one_time": False,
        "buttons": [
            [get_button(label="Звонков", color="positive"),
             get_button(label="Уроков", color="positive")],
            [get_button(label="Назад", color="secondary")]
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
            [get_button(label="Назад", color="secondary")]
        ]
    }

    # passing keyboards and creating their json objects
    main_keyboard = json.dumps(main_keyboard, ensure_ascii=False).encode("utf-8")
    main_keyboard = str(main_keyboard.decode("utf-8"))
    before_registration_keyboard = json.dumps(before_registration_keyboard, ensure_ascii=False).encode("utf-8")
    before_registration_keyboard = str(before_registration_keyboard.decode("utf-8"))
    schedules_keyboard = json.dumps(schedules_keyboard, ensure_ascii=False).encode("utf-8")
    schedules_keyboard = str(schedules_keyboard.decode("utf-8"))
    choosing_day_of_week_keyboard = json.dumps(choosing_day_of_week_keyboard, ensure_ascii=False).encode("utf-8")
    choosing_day_of_week_keyboard = str(choosing_day_of_week_keyboard.decode("utf-8"))

    # function for sending ready-made messages to the user
    def write_msg(user_id, message, keyboard=None, sticker_id=None, attachment=None):
        # sending some data to the terminal about ready response parameters
        print("Responce:", "".join(message))
        if sticker_id != None:
            print(f"Sticker: {sticker_id}")
        if attachment != None:
            print(f"Attachment: {attachment}")
        # intercept the main keyboard if the user is not yet registered
        if keyboard == main_keyboard:
            presence_user = UserSearcher.searching_user_in_database(
                database_source="workWithUsersDatabase/UsersDatabase.txt", user_id=f"id{user_id}")
            if presence_user == []:
                keyboard = before_registration_keyboard
        # sending the message itself to the user in the VK
        main_vk_session.method("messages.send",
                               {"peer_id": user_id, "message": message, "keyboard": keyboard, "sticker_id": sticker_id,
                                "attachment": attachment, "random_id": randint(1, 100000000)})

    # function for updating the id of the transmitted file in the message
    def update_attachment_id(file_source):
        # checking for files with photos (for better display in messages)
        if list(file_source.split("."))[-1] in ["png"]:
            get_serverAccess = main_vk_session.method("photos.getMessagesUploadServer",
                                                      {"album_id": 268631098, "group_id": BotConfig.CommunityID})
            get_serverLink = requests.post(get_serverAccess["upload_url"],
                                           files={"file": open(f"botAttachments/{file_source}", "rb+")}).json()
            save_photoFile = main_vk_session.method("photos.saveMessagesPhoto", {"photo": get_serverLink["photo"],
                                                                                 "server": get_serverLink["server"],
                                                                                 "hash": get_serverLink["hash"]})[0]
            return f"photo{save_photoFile['owner_id']}_{save_photoFile['id']}"
        # other file extensions that are passed as regular files
        else:
            get_serverAccess = main_vk_session.method("docs.getMessagesUploadServer",
                                                      {"type": "doc", "peer_id": event.object.peer_id})
            get_serverLink = requests.post(get_serverAccess["upload_url"],
                                           files={"file": open(f"botAttachments/{file_source}", "rb+")}).json()
            save_specificFile = main_vk_session.method("docs.save", {"file": get_serverLink["file"]})["doc"]
            return f"doc{save_specificFile['owner_id']}_{save_specificFile['id']}"

    # function for sending a backup copy of the database to the administration conversation
    def sending_and_reserving_database(conversation_id, database_source, message):
        # sending data to the terminal
        print(f"Sending and reserving a database...({conversation_id}, {database_source})")
        # sending and reserving data
        get_serverAccess = main_vk_session.method("docs.getMessagesUploadServer",
                                                  {"type": "doc", "peer_id": conversation_id})
        get_serverLink = requests.post(get_serverAccess["upload_url"],
                                       files={"file": open(database_source, "rb+")}).json()
        save_docFile = main_vk_session.method("docs.save", {"file": get_serverLink["file"]})["doc"]
        attachment = f"doc{save_docFile['owner_id']}_{save_docFile['id']}"
        main_vk_session.method("messages.send",
                               {"peer_id": BotConfig.ConversationForDataReservationID, "message": message,
                                "attachment": attachment, "random_id": randint(1, 10000000)})

    # function for identifying existing groups in a shared database with a schedule
    def list_of_groups_in_the_class(name_of_the_scanned_folder, database_source="workWithExcelFile/excelDatabase"):
        try:
            # search for files and separate the name from the extension
            return ["".join(file_name.split(".xlsx")) for file_name in
                    os.listdir(f"{database_source}/{name_of_the_scanned_folder}")]
        except Exception as E:
            # sending data to the terminal if the storage does not exist
            print(f"!!! ERROR: Broken folder with the files or incorrect path !!!")
            print(f"The specified path to the files: {database_source}/{name_of_the_scanned_folder}")
            print(f"Reason: {E}")
            # returns an empty array in case of failure
            return []

    # getting a longpoll for further work on the response to users
    longpoll = VkBotLongPoll(main_vk_session, group_id=BotConfig.CommunityID)
    # the main cycle of responding to user messages
    for event in longpoll.listen():
        # checking the correctness of the user and chat for further processing of the request
        if (event.type == VkBotEventType.MESSAGE_NEW) and (event.object.peer_id == event.object.from_id):
            # sending data to the terminal about the user who made the request
            print(datetime.datetime.today())
            print(f"Message from-->https://vk.com/id{event.object.peer_id}")
            print(f"Message content: {event.object.text}")
            # working with back-buttons to return to the start menu
            if event.object.text.lower() in BotConfig.buttons_back:
                # greeting with the user if certain buttons were used
                if event.object.text.lower() in BotConfig.ru_greetings_bot:
                    response_randomizer = randint(0, len(BotConfig.ru_greetings_bot) - 1)
                    response_word = BotConfig.ru_greetings_bot[response_randomizer]
                    get_user_name = main_vk_session.method("users.get", {"user_ids": event.object.peer_id})[0][
                        "first_name"]
                    write_msg(user_id=event.object.peer_id, keyboard=main_keyboard,
                              message=f"{response_word.title()}, {str(get_user_name)}!")
                elif event.object.text.lower() in BotConfig.eng_greetings_bot:
                    response_randomizer = randint(0, len(BotConfig.eng_greetings_bot) - 1)
                    response_word = BotConfig.eng_greetings_bot[response_randomizer]
                    get_user_name = main_vk_session.method("users.get", {"user_ids": event.object.peer_id})[0][
                        "first_name"]
                    write_msg(user_id=event.object.peer_id, keyboard=main_keyboard,
                              message=f"{response_word.title()}, {str(get_user_name)}!")
                # go to the main menu if only a transition is required
                else:
                    write_msg(user_id=event.object.peer_id, keyboard=main_keyboard, message="Главное меню👌")
            # main_keyboard - working with commands of this level
            elif event.object.text.lower() == "новости":
                main_vk_session.method("messages.setActivity", {"peer_id": event.object.peer_id, "type": "typing"})
                write_msg(user_id=event.object.peer_id, keyboard=main_keyboard,
                          message=CompilationNews.weather_searcher(source=BotConfig.weather_source,
                                                                   search_tag=BotConfig.weather_search_tag,
                                                                   tag_info=BotConfig.weather_tag_info,
                                                                   headers=BotConfig.user_agent))
                write_msg(user_id=event.object.peer_id, keyboard=main_keyboard,
                          message=CompilationNews.rates_searcher())
                write_msg(user_id=event.object.peer_id, keyboard=main_keyboard,
                          message="🔥Мы рекомендуем:\nДискорд - smtechnology.info\nЦитаты - @buildmesomerockets\nМемы - @pumpodslushano\n📝Не понимаешь математику или физику? - вот тг-канал, который может тебе помочь: t.me/sunz_trained")
                write_msg(user_id=event.object.peer_id, keyboard=main_keyboard,
                          message=CompilationNews.news_searcher(source=BotConfig.news_source,
                                                                search_tag=BotConfig.news_search_tag,
                                                                tag_info=BotConfig.news_tag_info,
                                                                headers=BotConfig.user_agent, quantity_news=1))
                write_msg(user_id=event.object.peer_id, keyboard=main_keyboard,
                          message=CompilationNews.covid_searcher(source=BotConfig.covid_source,
                                                                 search_tag=BotConfig.covid_search_tag,
                                                                 tag_info=BotConfig.covid_tag_info,
                                                                 headers=BotConfig.user_agent))
            elif event.object.text.lower() == "расписание":
                write_msg(user_id=event.object.peer_id, keyboard=schedules_keyboard,
                          message="Ок, только выбери какое🖖")
            elif event.object.text.lower() == "настройки":
                presence_user = UserSearcher.searching_user_in_database(
                    database_source="workWithUsersDatabase/UsersDatabase.txt", user_id=f"id{event.object.peer_id}")
                if presence_user != []:
                    write_msg(user_id=event.object.peer_id,
                              keyboard=create_settings_keyboard(keyboard_user_id=f"id{event.object.peer_id}"),
                              message="Это раздел настроек уведомлений - если плитка зелёная, то функция включена, если же красная, то выключена. Чтобы изменить один из перечисленных параметров, тебе просто следует нажать на необходимый пункт🤗")
                    write_msg(user_id=event.object.peer_id,
                              keyboard=create_settings_keyboard(keyboard_user_id=f"id{event.object.peer_id}"),
                              message="Кстати, время, когда будет происходить автоматическая рассылка расписания, можно отредактировать🤫\nФормат изменения: 08:00")
                else:
                    write_msg(user_id=event.object.peer_id, keyboard=main_keyboard,
                              message="Такс, тебя же нет в базе. Нажми на плитку -Регистрация- в главном меню, чтобы занести свои данные для выдачи расписания📖")
            elif event.object.text.lower() == "о боте":
                write_msg(user_id=event.object.peer_id, keyboard=main_keyboard, message=BotConfig.about_bot[0])
                write_msg(user_id=event.object.peer_id, keyboard=main_keyboard, message=BotConfig.about_bot[1])
                write_msg(user_id=event.object.peer_id, keyboard=main_keyboard, message=BotConfig.about_bot[2],
                          attachment=update_attachment_id(file_source="AboutBot.png"))
            # settings_keyboard - working with commands of this level
            elif event.object.text.lower() == "автоматическая рассылка расписания":
                presence_user = UserSearcher.searching_user_in_database(
                    database_source="workWithUsersDatabase/UsersDatabase.txt", user_id=f"id{event.object.peer_id}")
                if presence_user != []:
                    main_vk_session.method("messages.setActivity", {"peer_id": event.object.peer_id, "type": "typing"})
                    UserSearcher.editing_user_in_database(database_source="workWithUsersDatabase/UsersDatabase.txt",
                                                          full_name=presence_user[0], user_id=presence_user[1],
                                                          source_for_user=presence_user[2], sheet_name=presence_user[3],
                                                          columns_for_user=presence_user[4],
                                                          extra_cells=presence_user[5],
                                                          daily_schedule=(0 if presence_user[6] != 0 else 1),
                                                          time_of_mailing=presence_user[7],
                                                          telegram_alerts=presence_user[8])
                    sending_and_reserving_database(conversation_id=event.object.from_id,
                                                   database_source="workWithUsersDatabase/UsersDatabase.txt",
                                                   message=f"#DUMP {presence_user[0]} (id{event.object.peer_id}) внёс некоторые изменения в своих настройках, подробнее:\nAвтоматическая рассылка расписания была успешно {'отключена' if presence_user[6] != 0 else 'включена'}⚙")
                    write_msg(user_id=event.object.peer_id,
                              keyboard=create_settings_keyboard(keyboard_user_id=f"id{event.object.peer_id}"),
                              message=f"Параметр был успешно {'выключен' if presence_user[6] != 0 else 'включен'}. Не забывай, что его в любой момент можно здесь {'включить' if presence_user[6] != 0 else 'выключить'}🤔")
                else:
                    write_msg(user_id=event.object.peer_id, keyboard=main_keyboard,
                              message="Такс, тебя же нет в базе. Нажми на плитку -Регистрация- в главном меню, чтобы занести свои данные для выдачи расписания📖")
            elif event.object.text.lower() in [f"{hour // 10}{hour % 10}:{minute // 10}{minute % 10}" for hour in
                                               range(24) for minute in range(60)]:
                presence_user = UserSearcher.searching_user_in_database(
                    database_source="workWithUsersDatabase/UsersDatabase.txt", user_id=f"id{event.object.peer_id}")
                if presence_user != []:
                    if event.object.text.lower() != presence_user[7]:
                        main_vk_session.method("messages.setActivity",
                                               {"peer_id": event.object.peer_id, "type": "typing"})
                        UserSearcher.editing_user_in_database(database_source="workWithUsersDatabase/UsersDatabase.txt",
                                                              full_name=presence_user[0], user_id=presence_user[1],
                                                              source_for_user=presence_user[2],
                                                              sheet_name=presence_user[3],
                                                              columns_for_user=presence_user[4],
                                                              extra_cells=presence_user[5],
                                                              daily_schedule=presence_user[6],
                                                              time_of_mailing=event.object.text.lower(),
                                                              telegram_alerts=presence_user[8])
                        sending_and_reserving_database(conversation_id=event.object.from_id,
                                                       database_source="workWithUsersDatabase/UsersDatabase.txt",
                                                       message=f"#DUMP {presence_user[0]} (id{event.object.peer_id}) внёс некоторые изменения в своих настройках, подробнее:\nВремя автоматической рассылки расписания было успешно изменено с {presence_user[7]} на {event.object.text.lower()}⚙")
                        write_msg(user_id=event.object.peer_id,
                                  keyboard=create_settings_keyboard(keyboard_user_id=f"id{event.object.peer_id}"),
                                  message=f"Aвтоматическая рассылка расписания была успешно изменена с {presence_user[7]} на {event.object.text.lower()}🤔")
                    else:
                        write_msg(user_id=event.object.peer_id,
                                  keyboard=create_settings_keyboard(keyboard_user_id=f"id{event.object.peer_id}"),
                                  message=f"Ты указал то же самое время, что и было раньше🤔")
                else:
                    write_msg(user_id=event.object.peer_id, keyboard=main_keyboard,
                              message="Такс, тебя же нет в базе. Нажми на плитку -Регистрация- в главном меню, чтобы занести свои данные для выдачи расписания📖")
            elif event.object.text.lower() == "посты от администрации из telegram":
                presence_user = UserSearcher.searching_user_in_database(
                    database_source="workWithUsersDatabase/UsersDatabase.txt", user_id=f"id{event.object.peer_id}")
                if presence_user != []:
                    main_vk_session.method("messages.setActivity", {"peer_id": event.object.peer_id, "type": "typing"})
                    UserSearcher.editing_user_in_database(database_source="workWithUsersDatabase/UsersDatabase.txt",
                                                          full_name=presence_user[0], user_id=presence_user[1],
                                                          source_for_user=presence_user[2], sheet_name=presence_user[3],
                                                          columns_for_user=presence_user[4],
                                                          extra_cells=presence_user[5], daily_schedule=presence_user[6],
                                                          time_of_mailing=presence_user[7],
                                                          telegram_alerts=(0 if presence_user[8] != 0 else 1))
                    sending_and_reserving_database(conversation_id=event.object.from_id,
                                                   database_source="workWithUsersDatabase/UsersDatabase.txt",
                                                   message=f"#DUMP {presence_user[0]} (id{event.object.peer_id}) внёс некоторые изменения в своих настройках, подробнее:\nПосты от администрации из Telegram были успешно {'отключены' if presence_user[8] != 0 else 'включены'}⚙")
                    write_msg(user_id=event.object.peer_id,
                              keyboard=create_settings_keyboard(keyboard_user_id=f"id{event.object.peer_id}"),
                              message=f"Параметр был успешно {'выключен' if presence_user[8] != 0 else 'включен'}. Не забывай, что его в любой момент можно здесь {'включить' if presence_user[8] != 0 else 'выключить'}🤔")
                else:
                    write_msg(user_id=event.object.peer_id, keyboard=main_keyboard,
                              message="Такс, тебя же нет в базе. Нажми на плитку -Регистрация- в главном меню, чтобы занести свои данные для выдачи расписания📖")
            elif event.object.text.lower() == "помощь":
                write_msg(user_id=event.object.peer_id, keyboard=main_keyboard,
                          message="У тебя есть вопросы? - не волнуйся, ведь ты их всегда можешь задать в беседе, прикреплённой к сообществу🎯\nhttps://vk.me/join/FhSVyJp7fYT0fM805_KTHNWPctDNa79JGsI=")
            # schedules_keyboard - working with commands of this level
            elif event.object.text.lower() in ["звонков", "звонки"]:
                write_msg(user_id=event.object.peer_id, keyboard=main_keyboard,
                          message=BotConfig.unified_schedule_calls[0])
            elif event.object.text.lower() == "уроков":
                write_msg(user_id=event.object.peer_id, keyboard=choosing_day_of_week_keyboard,
                          message="Хмм, теперь выбери день😼\nКста, в целях защиты против коронавирусной инфекции не забывай надевать маску и перчатки😷")
            # choosing_day_of_week_keyboard - working with commands of this level
            elif event.object.text.lower() == "понедельник":
                presence_user = UserSearcher.searching_user_in_database(
                    database_source="workWithUsersDatabase/UsersDatabase.txt", user_id=f"id{event.object.peer_id}")
                if presence_user != []:
                    write_msg(user_id=event.object.peer_id, keyboard=main_keyboard,
                              message="Поиск актуального расписания для тебя🔎")
                    main_vk_session.method("messages.setActivity", {"peer_id": event.object.peer_id, "type": "typing"})
                    user_schedule = ExcelSearcher.selective_data_search(excel_source=presence_user[2],
                                                                        sheet_name=presence_user[3],
                                                                        columns=presence_user[4],
                                                                        extra_cells=presence_user[5],
                                                                        start_data="Понедельник", end_data="None")
                    write_msg(user_id=event.object.peer_id, keyboard=main_keyboard, message=user_schedule)
                else:
                    write_msg(user_id=event.object.peer_id, keyboard=main_keyboard,
                              message="Такс, тебя же нет в базе. Нажми на плитку -Регистрация- в главном меню, чтобы занести свои данные для выдачи расписания📖")
            elif event.object.text.lower() == "вторник":
                presence_user = UserSearcher.searching_user_in_database(
                    database_source="workWithUsersDatabase/UsersDatabase.txt", user_id=f"id{event.object.peer_id}")
                if presence_user != []:
                    write_msg(user_id=event.object.peer_id, keyboard=main_keyboard,
                              message="Поиск актуального расписания для тебя🔎")
                    main_vk_session.method("messages.setActivity", {"peer_id": event.object.peer_id, "type": "typing"})
                    user_schedule = ExcelSearcher.selective_data_search(excel_source=presence_user[2],
                                                                        sheet_name=presence_user[3],
                                                                        columns=presence_user[4],
                                                                        extra_cells=presence_user[5],
                                                                        start_data="Вторник", end_data="None")
                    write_msg(user_id=event.object.peer_id, keyboard=main_keyboard, message=user_schedule)
                else:
                    write_msg(user_id=event.object.peer_id, keyboard=main_keyboard,
                              message="Такс, тебя же нет в базе. Нажми на плитку -Регистрация- в главном меню, чтобы занести свои данные для выдачи расписания📖")
            elif event.object.text.lower() == "среда":
                presence_user = UserSearcher.searching_user_in_database(
                    database_source="workWithUsersDatabase/UsersDatabase.txt", user_id=f"id{event.object.peer_id}")
                if presence_user != []:
                    write_msg(user_id=event.object.peer_id, keyboard=main_keyboard,
                              message="Поиск актуального расписания для тебя🔎")
                    main_vk_session.method("messages.setActivity", {"peer_id": event.object.peer_id, "type": "typing"})
                    user_schedule = ExcelSearcher.selective_data_search(excel_source=presence_user[2],
                                                                        sheet_name=presence_user[3],
                                                                        columns=presence_user[4],
                                                                        extra_cells=presence_user[5],
                                                                        start_data="Среда", end_data="None")
                    write_msg(user_id=event.object.peer_id, keyboard=main_keyboard, message=user_schedule)
                else:
                    write_msg(user_id=event.object.peer_id, keyboard=main_keyboard,
                              message="Такс, тебя же нет в базе. Нажми на плитку -Регистрация- в главном меню, чтобы занести свои данные для выдачи расписания📖")
            elif event.object.text.lower() == "четверг":
                presence_user = UserSearcher.searching_user_in_database(
                    database_source="workWithUsersDatabase/UsersDatabase.txt", user_id=f"id{event.object.peer_id}")
                if presence_user != []:
                    write_msg(user_id=event.object.peer_id, keyboard=main_keyboard,
                              message="Поиск актуального расписания для тебя🔎")
                    main_vk_session.method("messages.setActivity", {"peer_id": event.object.peer_id, "type": "typing"})
                    user_schedule = ExcelSearcher.selective_data_search(excel_source=presence_user[2],
                                                                        sheet_name=presence_user[3],
                                                                        columns=presence_user[4],
                                                                        extra_cells=presence_user[5],
                                                                        start_data="Четверг", end_data="None")
                    write_msg(user_id=event.object.peer_id, keyboard=main_keyboard, message=user_schedule)
                else:
                    write_msg(user_id=event.object.peer_id, keyboard=main_keyboard,
                              message="Такс, тебя же нет в базе. Нажми на плитку -Регистрация- в главном меню, чтобы занести свои данные для выдачи расписания📖")
            elif event.object.text.lower() == "пятница":
                presence_user = UserSearcher.searching_user_in_database(
                    database_source="workWithUsersDatabase/UsersDatabase.txt", user_id=f"id{event.object.peer_id}")
                if presence_user != []:
                    write_msg(user_id=event.object.peer_id, keyboard=main_keyboard,
                              message="Поиск актуального расписания для тебя🔎")
                    main_vk_session.method("messages.setActivity", {"peer_id": event.object.peer_id, "type": "typing"})
                    user_schedule = ExcelSearcher.selective_data_search(excel_source=presence_user[2],
                                                                        sheet_name=presence_user[3],
                                                                        columns=presence_user[4],
                                                                        extra_cells=presence_user[5],
                                                                        start_data="Пятница", end_data="None")
                    write_msg(user_id=event.object.peer_id, keyboard=main_keyboard, message=user_schedule)
                else:
                    write_msg(user_id=event.object.peer_id, keyboard=main_keyboard,
                              message="Такс, тебя же нет в базе. Нажми на плитку -Регистрация- в главном меню, чтобы занести свои данные для выдачи расписания📖")
            elif event.object.text.lower() == "суббота":
                presence_user = UserSearcher.searching_user_in_database(
                    database_source="workWithUsersDatabase/UsersDatabase.txt", user_id=f"id{event.object.peer_id}")
                if presence_user != []:
                    write_msg(user_id=event.object.peer_id, keyboard=main_keyboard,
                              message="Поиск актуального расписания для тебя🔎")
                    main_vk_session.method("messages.setActivity", {"peer_id": event.object.peer_id, "type": "typing"})
                    user_schedule = ExcelSearcher.selective_data_search(excel_source=presence_user[2],
                                                                        sheet_name=presence_user[3],
                                                                        columns=presence_user[4],
                                                                        extra_cells=presence_user[5],
                                                                        start_data="Суббота", end_data="None")
                    write_msg(user_id=event.object.peer_id, keyboard=main_keyboard, message=user_schedule)
                else:
                    write_msg(user_id=event.object.peer_id, keyboard=main_keyboard,
                              message="Такс, тебя же нет в базе. Нажми на плитку -Регистрация- в главном меню, чтобы занести свои данные для выдачи расписания📖")

            # registering new users in the bot's main database
            elif event.object.text.lower() == "регистрация":
                presence_user = UserSearcher.searching_user_in_database(
                    database_source="workWithUsersDatabase/UsersDatabase.txt", user_id=f"id{event.object.peer_id}")
                if presence_user != []:
                    write_msg(user_id=event.object.peer_id, keyboard=main_keyboard,
                              message=f"Ты уже зарегистрирован - если всё работает отлично, то ты также можешь продолжать пользоваться ботом. Если же у тебя есть какие-либо вопросы или ты сменил группу, то пиши в беседу, прикреплённую к сообществу⚙\nhttps://vk.me/join/FhSVyJp7fYT0fM805_KTHNWPctDNa79JGsI=")
                else:
                    write_msg(user_id=event.object.peer_id, keyboard=main_keyboard,
                              message=f"Теперь регистрацию можно осуществить прямо тут - для этого введи название своей группы русскими символами (если не получиться с первого раза - попробуй ещё раз)😜\nВот список всех существующих групп в Предуниверсарии МАИ:\n8️⃣Класс: {'; '.join(list_of_groups_in_the_class('8class'))}\n9️⃣Класс: {'; '.join(list_of_groups_in_the_class('9class'))}\n1️⃣0️⃣Класс: {'; '.join(list_of_groups_in_the_class('10class'))}\n1️⃣1️⃣Класс: {'; '.join(list_of_groups_in_the_class('11class'))}\nЕсли ты не можешь найти свою группу или тебе нужна помощь, то пиши в беседу, прикреплённую к сообществу:\nhttps://vk.me/join/FhSVyJp7fYT0fM805_KTHNWPctDNa79JGsI=")
            elif (event.object.text.upper() in list_of_groups_in_the_class("8class")) or (
                    event.object.text.upper() in list_of_groups_in_the_class("9class")) or (
                    event.object.text.upper() in list_of_groups_in_the_class("10class")) or (
                    event.object.text.upper() in list_of_groups_in_the_class("11class")) or (
                    event.object.text in ["ГОСТЬ", "ТЕСТ", "GUEST", "TEST"]) or (
                    event.object.text in list_of_groups_in_the_class("TEACHERS")):
                main_vk_session.method("messages.setActivity", {"peer_id": event.object.peer_id, "type": "typing"})
                get_last_name = main_vk_session.method("users.get", {"user_ids": event.object.peer_id})[0]["last_name"]
                get_first_name = main_vk_session.method("users.get", {"user_ids": event.object.peer_id})[0][
                    "first_name"]
                presence_user = UserSearcher.searching_user_in_database(
                    database_source="workWithUsersDatabase/UsersDatabase.txt", user_id=f"id{event.object.peer_id}")
                if presence_user != []:
                    if event.object.text.upper() == presence_user[3]:
                        write_msg(user_id=event.object.peer_id, keyboard=main_keyboard,
                                  message="Да-да, всё внесено верно - ты есть в базе. Если есть какие-то вопросы, то пиши в беседу, прикреплённую к сообществу🗿\nhttps://vk.me/join/FhSVyJp7fYT0fM805_KTHNWPctDNa79JGsI=")
                    else:
                        write_msg(user_id=event.object.peer_id, keyboard=main_keyboard,
                                  message=f"Ого - похоже ты хочешь изменить группу! Напиши в беседу, прикреплённую к сообществу, чтобы мы редактировали твои данные✍\nhttps://vk.me/join/FhSVyJp7fYT0fM805_KTHNWPctDNa79JGsI=")
                else:
                    if event.object.text.upper() in list_of_groups_in_the_class("8class"):
                        UserSearcher.adding_user_in_database(database_source="workWithUsersDatabase/UsersDatabase.txt",
                                                             full_name=f"{get_last_name} {get_first_name}",
                                                             user_id=f"id{event.object.peer_id}",
                                                             source_for_user="8class",
                                                             sheet_name=event.object.text.upper(),
                                                             columns_for_user=['A', 'B', 'D', 'E', 'F'], extra_cells=1,
                                                             daily_schedule=1, time_of_mailing="19:00",
                                                             telegram_alerts=1)
                        sending_and_reserving_database(conversation_id=event.object.from_id,
                                                       database_source="workWithUsersDatabase/UsersDatabase.txt",
                                                       message=f"#DUMP К нам присоединился новый пользователь - {get_last_name} {get_first_name}(id{event.object.peer_id} | 8class | {event.object.text.upper()})🚀")
                        write_msg(user_id=event.object.peer_id, keyboard=main_keyboard,
                                  message="Поздравляю! Регистрация прошла успешно✅")
                    elif event.object.text.upper() in list_of_groups_in_the_class("9class"):
                        UserSearcher.adding_user_in_database(database_source="workWithUsersDatabase/UsersDatabase.txt",
                                                             full_name=f"{get_last_name} {get_first_name}",
                                                             user_id=f"id{event.object.peer_id}",
                                                             source_for_user="9class",
                                                             sheet_name=event.object.text.upper(),
                                                             columns_for_user=['A', 'B', 'D', 'E', 'F'], extra_cells=1,
                                                             daily_schedule=1, time_of_mailing="19:00",
                                                             telegram_alerts=1)
                        sending_and_reserving_database(conversation_id=event.object.from_id,
                                                       database_source="workWithUsersDatabase/UsersDatabase.txt",
                                                       message=f"#DUMP К нам присоединился новый пользователь - {get_last_name} {get_first_name}(id{event.object.peer_id} | 9class | {event.object.text.upper()})🚀")
                        write_msg(user_id=event.object.peer_id, keyboard=main_keyboard,
                                  message="Поздравляю! Регистрация прошла успешно✅")
                    elif event.object.text.upper() in list_of_groups_in_the_class("10class"):
                        UserSearcher.adding_user_in_database(database_source="workWithUsersDatabase/UsersDatabase.txt",
                                                             full_name=f"{get_last_name} {get_first_name}",
                                                             user_id=f"id{event.object.peer_id}",
                                                             source_for_user="10class",
                                                             sheet_name=event.object.text.upper(),
                                                             columns_for_user=['A', 'B', 'D', 'E', 'F'], extra_cells=1,
                                                             daily_schedule=1, time_of_mailing="19:00",
                                                             telegram_alerts=1)
                        sending_and_reserving_database(conversation_id=event.object.from_id,
                                                       database_source="workWithUsersDatabase/UsersDatabase.txt",
                                                       message=f"#DUMP К нам присоединился новый пользователь - {get_last_name} {get_first_name}(id{event.object.peer_id} | 10class | {event.object.text.upper()})🚀")
                        write_msg(user_id=event.object.peer_id, keyboard=main_keyboard,
                                  message="Поздравляю! Регистрация прошла успешно✅")
                    elif event.object.text.upper() in list_of_groups_in_the_class("11class"):
                        UserSearcher.adding_user_in_database(database_source="workWithUsersDatabase/UsersDatabase.txt",
                                                             full_name=f"{get_last_name} {get_first_name}",
                                                             user_id=f"id{event.object.peer_id}",
                                                             source_for_user="11class",
                                                             sheet_name=event.object.text.upper(),
                                                             columns_for_user=['A', 'B', 'D', 'E', 'F'], extra_cells=1,
                                                             daily_schedule=1, time_of_mailing="19:00",
                                                             telegram_alerts=1)
                        sending_and_reserving_database(conversation_id=event.object.from_id,
                                                       database_source="workWithUsersDatabase/UsersDatabase.txt",
                                                       message=f"#DUMP К нам присоединился новый пользователь - {get_last_name} {get_first_name}(id{event.object.peer_id} | 11class | {event.object.text.upper()})🚀")
                        write_msg(user_id=event.object.peer_id, keyboard=main_keyboard,
                                  message="Поздравляю! Регистрация прошла успешно✅")
                    elif event.object.text in ["ГОСТЬ", "ТЕСТ", "GUEST", "TEST"]:
                        UserSearcher.adding_user_in_database(database_source="workWithUsersDatabase/UsersDatabase.txt",
                                                             full_name=f"{get_last_name} {get_first_name}",
                                                             user_id=f"id{event.object.peer_id}",
                                                             source_for_user="GUESTS", sheet_name="ГОСТЬ",
                                                             columns_for_user=['A', 'B', 'D', 'E', 'F'], extra_cells=0,
                                                             daily_schedule=1, time_of_mailing="19:00",
                                                             telegram_alerts=1)
                        sending_and_reserving_database(conversation_id=event.object.from_id,
                                                       database_source="workWithUsersDatabase/UsersDatabase.txt",
                                                       message=f"#DUMP Кто-то захотел протестировать бота - {get_last_name} {get_first_name}(id{event.object.peer_id} | GUESTS | ГОСТЬ)🔭")
                        write_msg(user_id=event.object.peer_id, keyboard=main_keyboard,
                                  message="Поздравляем! Регистрация прошла успешно✅")
                        write_msg(user_id=event.object.peer_id, keyboard=main_keyboard,
                                  message="Теперь ты имеешь абсолютно все возможности, чтобы полноценно протестировать нашего бота🎳")
                    elif event.object.text in list_of_groups_in_the_class("TEACHERS"):
                        UserSearcher.adding_user_in_database(database_source="workWithUsersDatabase/UsersDatabase.txt",
                                                             full_name=f"{get_last_name} {get_first_name}",
                                                             user_id=f"id{event.object.peer_id}",
                                                             source_for_user="TEACHERS",
                                                             sheet_name=event.object.text.upper(),
                                                             columns_for_user=['A', 'B', 'C', 'D', 'F'], extra_cells=0,
                                                             daily_schedule=1, time_of_mailing="19:00",
                                                             telegram_alerts=1)
                        sending_and_reserving_database(conversation_id=event.object.from_id,
                                                       database_source="workWithUsersDatabase/UsersDatabase.txt",
                                                       message=f"#DUMP К нам присоединился новый педагог - {get_last_name} {get_first_name}(id{event.object.peer_id} | TEACHERS | {event.object.text.upper()})🎓")
                        write_msg(user_id=event.object.peer_id, keyboard=main_keyboard,
                                  message="Поздравляю! Регистрация прошла успешно✅")
            # links to Zoom tables depending on the class number and other parameters
            elif event.object.text.lower() in ["zoom", "зум",
                                               "ссылки"] and BotConfig.permission_to_distribute_links != False:
                presence_user = UserSearcher.searching_user_in_database(
                    database_source="workWithUsersDatabase/UsersDatabase.txt", user_id=f"id{event.object.peer_id}")
                if presence_user != []:
                    if presence_user[3] in list_of_groups_in_the_class("8class"):
                        write_msg(user_id=event.object.peer_id, keyboard=main_keyboard,
                                  message=f"Старайся не отключать камеру с микрофоном на уроке, ведь это не даёт учителю ощущения, что он разговаривает только сам с собой🤪\n{BotConfig.links_to_zoom[0]}")
                    elif presence_user[3] in list_of_groups_in_the_class("9class"):
                        write_msg(user_id=event.object.peer_id, keyboard=main_keyboard,
                                  message=f"Старайся не отключать камеру с микрофоном на уроке, ведь это не даёт учителю ощущения, что он разговаривает только сам с собой🤪\n{BotConfig.links_to_zoom[1]}")
                    elif presence_user[3] in list_of_groups_in_the_class("10class"):
                        write_msg(user_id=event.object.peer_id, keyboard=main_keyboard,
                                  message=f"Старайся не отключать камеру с микрофоном на уроке, ведь это не даёт учителю ощущения, что он разговаривает только сам с собой🤪\n{BotConfig.links_to_zoom[2]}")
                    elif presence_user[3] in list_of_groups_in_the_class("11class"):
                        write_msg(user_id=event.object.peer_id, keyboard=main_keyboard,
                                  message=f"Старайся не отключать камеру с микрофоном на уроке, ведь это не даёт учителю ощущения, что он разговаривает только сам с собой🤪\n{BotConfig.links_to_zoom[3]}")
                    elif presence_user[3] in list_of_groups_in_the_class("TEACHERS"):
                        write_msg(user_id=event.object.peer_id, keyboard=main_keyboard,
                                  message=f"Вот ссылка на полную таблицу со всеми ссылками, хороших и продуктивных уроков🙂\n{BotConfig.links_to_zoom[4]}")
                    else:
                        write_msg(user_id=event.object.peer_id, keyboard=main_keyboard,
                                  message=f"Прости, но у тебя нет доступа к таблице со школьными ссылками на платформу Zoom для Предуниверсария МАИ🙄")
                else:
                    write_msg(user_id=event.object.peer_id, keyboard=main_keyboard,
                              message="Такс, тебя же нет в базе. Нажми на плитку -Регистрация- в главном меню, чтобы занести свои данные для выдачи расписания📖")
            # output of data that the user entered during registration
            elif event.object.text.lower() in ["я", "кто я", "хто я", "данные", "мои данные"]:
                presence_user = UserSearcher.searching_user_in_database(
                    database_source="workWithUsersDatabase/UsersDatabase.txt", user_id=f"id{event.object.peer_id}")
                if presence_user != []:
                    write_msg(user_id=event.object.peer_id, keyboard=main_keyboard,
                              message=f"Вот твои данные, которые ты внёс при регистрации: {presence_user[0]} | {presence_user[1]} | {presence_user[2]} | {presence_user[3]}💾")
                else:
                    write_msg(user_id=event.object.peer_id, keyboard=main_keyboard,
                              message=f"Ты ещё не зарегистрировался, бот пока знает про тебя только это: id{event.object.peer_id}📡")
            # 3301 - easter egg
            elif event.object.text.lower() in ["3301", "цикада", "цикада 3301", "пасхалка", "загадка", "секрет", "жак",
                                               "фреско", "жак фреско"]:
                write_msg(user_id=event.object.peer_id, keyboard=main_keyboard,
                          message="Ничего себе, ещё одна пасхалка?! Приступим, мы нашли очень интересную фотокарточку из семейного архива Жака Фреско. Задача заключается в нахождении и расшифровании спрятанного кода в этой картинке (при получении ответа - отпишись в общую беседу сообщества)",
                          attachment=update_attachment_id(
                              file_source="riddlesByJacquesFresco/photo_from_the_family_archive.jpg"))
            # checking for new updates in the bot (technical problems or expectations keyboard)
            elif event.object.text.lower() == "проверить обновления":
                write_msg(user_id=event.object.peer_id, keyboard=main_keyboard,
                          message="Оооу да - а вот и долгожданное обновление! Мы славно поработали и надеемся, что тебе всё понравится😎")
            # expression of gratitude to the developers, cute gif
            elif [word_of_thanks for word_of_thanks in
                  ["ура", "спасибо", "благодарю", "благодарствую", "молодец", "молодец", "красавчик", "красавчики",
                   "красавец", "красавцы", "красава", "красавы"] if word_of_thanks in event.object.text.lower()] != []:
                write_msg(user_id=event.object.peer_id, keyboard=main_keyboard, message="",
                          attachment=update_attachment_id(file_source="thanksToTheBot.gif"))
            # if not one of the commands was not found with the message
            else:
                write_msg(user_id=event.object.peer_id, keyboard=main_keyboard,
                          message="По-моему ты вводишь что-то не так, попробуй ещё раз😕")
            # sending data to the terminal about the end of the analysis
            print("-----------------------------")
            # waiting for the end of the vk timeout for safety reasons
            time.sleep(0.5)


# starting the bot logic
if __name__ == "__main__":
    # calling all major parallel tasks
    Thread(target=TelegramAlerts.working_with_the_telegram_binder).start()
    Thread(target=MailingSchedules.working_with_the_telegram_binder).start()
    # is automatic restart mandatory
    if BotConfig.error_checking_switch != True:
        # for a permanent bot job with auto-reconnection
        while True:
            try:
                work_of_the_main_VK_bot()
            except Exception as E:
                # sending data to the terminal about an error, then waiting for a reboot
                print("-----------------------------")
                print(datetime.datetime.today())
                print("!!!  The bot is disabled  !!!")
                print(f"Reason: {E}")
                print("-----------------------------")
                time.sleep(BotConfig.reboot_time % 100)
                print("!!!    Reconnect, wait    !!!")
    else:
        # starting with the log output of the error
        work_of_the_main_VK_bot()

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
