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
from specialScripts import CompilationNews as CompilationNews

# full error log output(without auto-reconnection)
error_checking_switch = False
# time to restart the bot
reboot_time = 5


# MAIN BOT LOGIC
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
            [get_button(label="Новости", color="positive"),
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
             get_button(label="Звонки", color="primary"),
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
                  {"peer_id": BotConfig.ConversationForDataReservationID, "message": message, "attachment": attachment,
                   "random_id": randint(1, 10000000)})

    # getting attachments for photos
    def update_attachment_id(img_source):
        get_serverAccess = vk.method("photos.getMessagesUploadServer",
                                     {"album_id": 268631098, "group_id": BotConfig.CommunityID})
        get_serverLink = requests.post(get_serverAccess["upload_url"],
                                       files={"file": open(f"botAttachments/{img_source}", "rb")}).json()
        save_attachmentFile = vk.method("photos.saveMessagesPhoto",
                                        {"photo": get_serverLink["photo"], "server": get_serverLink["server"],
                                         "hash": get_serverLink["hash"]})[0]
        return f"photo{save_attachmentFile['owner_id']}_{save_attachmentFile['id']}"

    # longpoll
    longpoll = VkBotLongPoll(vk, group_id=BotConfig.CommunityID)
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
                if event.object.text.lower() in BotConfig.buttons_back:
                    # greetings and jump to main menu
                    if event.object.text.lower().lower() in BotConfig.ru_greetings_bot:
                        response_randomizer = randint(0, len(BotConfig.ru_greetings_bot) - 1)
                        response_word = BotConfig.ru_greetings_bot[response_randomizer]
                        get_user_name = vk.method("users.get", {"user_ids": event.object.peer_id})[0]["first_name"]
                        write_msg(user_id=event.object.peer_id, keyboard=main_keyboard,
                                  message=f"{response_word.title()}, {str(get_user_name)}!")
                    elif event.object.text.lower().lower() in BotConfig.eng_greetings_bot:
                        response_randomizer = randint(0, len(BotConfig.eng_greetings_bot) - 1)
                        response_word = BotConfig.eng_greetings_bot[response_randomizer]
                        get_user_name = vk.method("users.get", {"user_ids": event.object.peer_id})[0]["first_name"]
                        write_msg(user_id=event.object.peer_id, keyboard=main_keyboard,
                                  message=f"{response_word.title()}, {str(get_user_name)}!")
                    # only jump to main menu
                    else:
                        write_msg(user_id=event.object.peer_id, keyboard=main_keyboard, message="Главное меню👌")
                # main keyboard
                elif event.object.text.lower() == "новости":
                    vk.method("messages.setActivity", {"peer_id": event.object.peer_id, "type": "typing"})
                    write_msg(user_id=event.object.peer_id, keyboard=main_keyboard,
                              message=CompilationNews.weather_searcher(source=BotConfig.weather_source,
                                                                       search_tag=BotConfig.weather_search_tag,
                                                                       tag_info=BotConfig.weather_tag_info,
                                                                       headers=BotConfig.user_agent))
                    write_msg(event.object.peer_id, CompilationNews.rates_searcher(), keyboard=main_keyboard)
                    write_msg(user_id=event.object.peer_id, keyboard=main_keyboard,
                              message="🔥Мы рекомендуем:\nЦитаты - @buildmesomerockets\nМемы - @pumpodslushano\n🤡Контента нет, просто место заполнить для галочки:\nМемы - @predmemetika")
                    write_msg(user_id=event.object.peer_id, keyboard=main_keyboard,
                              message=CompilationNews.news_searcher(source=BotConfig.news_source,
                                                                    search_tag=BotConfig.news_search_tag,
                                                                    tag_info=BotConfig.news_tag_info,
                                                                    headers=BotConfig.user_agent))
                    write_msg(user_id=event.object.peer_id, keyboard=main_keyboard,
                              message=CompilationNews.covid_searcher(source=BotConfig.covid_source,
                                                                     search_tag=BotConfig.covid_search_tag,
                                                                     tag_info=BotConfig.covid_tag_info,
                                                                     headers=BotConfig.user_agent))
                elif event.object.text.lower() == "расписание":
                    write_msg(user_id=event.object.peer_id, keyboard=schedules_keyboard,
                              message="Ок, только выбери какое🖖")
                elif event.object.text.lower() == "помощь":
                    write_msg(user_id=event.object.peer_id, keyboard=main_keyboard,
                              message="У тебя есть вопросы? - не волнуйся, ведь ты их всегда можешь задать в беседе, прикреплённой к сообществу🎯\nhttps://vk.me/join/FhSVyJp7fYT0fM805_KTHNWPctDNa79JGsI=")
                elif event.object.text.lower() == "о боте":
                    write_msg(user_id=event.object.peer_id, keyboard=main_keyboard, message=BotConfig.about_bot[0])
                    write_msg(user_id=event.object.peer_id, keyboard=main_keyboard, message=BotConfig.about_bot[1])
                    write_msg(user_id=event.object.peer_id, keyboard=main_keyboard, message=BotConfig.about_bot[2],
                              attachment=update_attachment_id(img_source="AboutBot.png"))
                # schedules keyboard
                elif event.object.text.lower() in ["звонков", "звонки"]:
                    write_msg(user_id=event.object.peer_id, keyboard=main_keyboard,
                              message=BotConfig.unified_schedule_calls)
                elif event.object.text.lower() == "уроков":
                    write_msg(user_id=event.object.peer_id, keyboard=choosing_day_of_week_keyboard,
                              message="Хмм, теперь выбери день😼\nКста, в целях защиты против коронавирусной инфекции не забывай надевать маску и перчатки😷")
                # choosing day of week keyboard
                elif event.object.text.lower() == "понедельник":
                    UserSearcher.searching_user_in_database(database_source="workWithUsersDatabase/UsersDatabase.txt",
                                                            user_id=f"id{event.object.peer_id}")
                    if UserSearcher.presence_user == []:
                        write_msg(user_id=event.object.peer_id, keyboard=main_keyboard,
                                  message="Такс, тебя же нет в базе. Нажми на плитку -Регистрация- в главном меню, чтобы занести свои данные для выдачи расписания📖")
                    else:
                        write_msg(user_id=event.object.peer_id, keyboard=main_keyboard,
                                  message="Поиск актуального расписания для тебя🔎")
                        vk.method("messages.setActivity", {"peer_id": event.object.peer_id, "type": "typing"})
                        ExcelSearcher.selective_data_search(excel_source=UserSearcher.presence_user[2],
                                                            sheet_name=UserSearcher.presence_user[3],
                                                            columns=UserSearcher.presence_user[4],
                                                            extra_cells=UserSearcher.presence_user[5],
                                                            start_data="Понедельник", end_data="None")
                        write_msg(user_id=event.object.peer_id, keyboard=main_keyboard,
                                  message=f"\n{ExcelSearcher.output_day_schedule}")
                elif event.object.text.lower() == "вторник":
                    UserSearcher.searching_user_in_database(database_source="workWithUsersDatabase/UsersDatabase.txt",
                                                            user_id=f"id{event.object.peer_id}")
                    if UserSearcher.presence_user == []:
                        write_msg(user_id=event.object.peer_id, keyboard=main_keyboard,
                                  message="Такс, тебя же нет в базе. Нажми на плитку -Регистрация- в главном меню, чтобы занести свои данные для выдачи расписания📖")
                    else:
                        write_msg(user_id=event.object.peer_id, keyboard=main_keyboard,
                                  message="Поиск актуального расписания для тебя🔎")
                        vk.method("messages.setActivity", {"peer_id": event.object.peer_id, "type": "typing"})
                        ExcelSearcher.selective_data_search(excel_source=UserSearcher.presence_user[2],
                                                            sheet_name=UserSearcher.presence_user[3],
                                                            columns=UserSearcher.presence_user[4],
                                                            extra_cells=UserSearcher.presence_user[5],
                                                            start_data="Вторник", end_data="None")
                        write_msg(user_id=event.object.peer_id, keyboard=main_keyboard,
                                  message=f"\n{ExcelSearcher.output_day_schedule}")
                elif event.object.text.lower() == "среда":
                    UserSearcher.searching_user_in_database(database_source="workWithUsersDatabase/UsersDatabase.txt",
                                                            user_id=f"id{event.object.peer_id}")
                    if UserSearcher.presence_user == []:
                        write_msg(user_id=event.object.peer_id, keyboard=main_keyboard,
                                  message="Такс, тебя же нет в базе. Нажми на плитку -Регистрация- в главном меню, чтобы занести свои данные для выдачи расписания📖")
                    else:
                        write_msg(user_id=event.object.peer_id, keyboard=main_keyboard,
                                  message="Поиск актуального расписания для тебя🔎")
                        vk.method("messages.setActivity", {"peer_id": event.object.peer_id, "type": "typing"})
                        ExcelSearcher.selective_data_search(excel_source=UserSearcher.presence_user[2],
                                                            sheet_name=UserSearcher.presence_user[3],
                                                            columns=UserSearcher.presence_user[4],
                                                            extra_cells=UserSearcher.presence_user[5],
                                                            start_data="Среда", end_data="None")
                        write_msg(user_id=event.object.peer_id, keyboard=main_keyboard,
                                  message=f"\n{ExcelSearcher.output_day_schedule}")
                elif event.object.text.lower() == "четверг":
                    UserSearcher.searching_user_in_database(database_source="workWithUsersDatabase/UsersDatabase.txt",
                                                            user_id=f"id{event.object.peer_id}")
                    if UserSearcher.presence_user == []:
                        write_msg(user_id=event.object.peer_id, keyboard=main_keyboard,
                                  message="Такс, тебя же нет в базе. Нажми на плитку -Регистрация- в главном меню, чтобы занести свои данные для выдачи расписания📖")
                    else:
                        write_msg(user_id=event.object.peer_id, keyboard=main_keyboard,
                                  message="Поиск актуального расписания для тебя🔎")
                        vk.method("messages.setActivity", {"peer_id": event.object.peer_id, "type": "typing"})
                        ExcelSearcher.selective_data_search(excel_source=UserSearcher.presence_user[2],
                                                            sheet_name=UserSearcher.presence_user[3],
                                                            columns=UserSearcher.presence_user[4],
                                                            extra_cells=UserSearcher.presence_user[5],
                                                            start_data="Четверг", end_data="None")
                        write_msg(user_id=event.object.peer_id, keyboard=main_keyboard,
                                  message=f"\n{ExcelSearcher.output_day_schedule}")
                elif event.object.text.lower() == "пятница":
                    UserSearcher.searching_user_in_database(database_source="workWithUsersDatabase/UsersDatabase.txt",
                                                            user_id=f"id{event.object.peer_id}")
                    if UserSearcher.presence_user == []:
                        write_msg(user_id=event.object.peer_id, keyboard=main_keyboard,
                                  message="Такс, тебя же нет в базе. Нажми на плитку -Регистрация- в главном меню, чтобы занести свои данные для выдачи расписания📖")
                    else:
                        write_msg(user_id=event.object.peer_id, keyboard=main_keyboard,
                                  message="Поиск актуального расписания для тебя🔎")
                        vk.method("messages.setActivity", {"peer_id": event.object.peer_id, "type": "typing"})
                        ExcelSearcher.selective_data_search(excel_source=UserSearcher.presence_user[2],
                                                            sheet_name=UserSearcher.presence_user[3],
                                                            columns=UserSearcher.presence_user[4],
                                                            extra_cells=UserSearcher.presence_user[5],
                                                            start_data="Пятница", end_data="None")
                        write_msg(user_id=event.object.peer_id, keyboard=main_keyboard,
                                  message=f"\n{ExcelSearcher.output_day_schedule}")
                elif event.object.text.lower() == "суббота":
                    UserSearcher.searching_user_in_database(database_source="workWithUsersDatabase/UsersDatabase.txt",
                                                            user_id=f"id{event.object.peer_id}")
                    if UserSearcher.presence_user == []:
                        write_msg(user_id=event.object.peer_id, keyboard=main_keyboard,
                                  message="Такс, тебя же нет в базе. Нажми на плитку -Регистрация- в главном меню, чтобы занести свои данные для выдачи расписания📖")
                    else:
                        write_msg(user_id=event.object.peer_id, keyboard=main_keyboard,
                                  message="Поиск актуального расписания для тебя🔎")
                        vk.method("messages.setActivity", {"peer_id": event.object.peer_id, "type": "typing"})
                        ExcelSearcher.selective_data_search(excel_source=UserSearcher.presence_user[2],
                                                            sheet_name=UserSearcher.presence_user[3],
                                                            columns=UserSearcher.presence_user[4],
                                                            extra_cells=UserSearcher.presence_user[5],
                                                            start_data="Суббота", end_data="None")
                        write_msg(user_id=event.object.peer_id, keyboard=main_keyboard,
                                  message=f"\n{ExcelSearcher.output_day_schedule}")
                # registration - instruction
                elif event.object.text.lower() == "регистрация":
                    UserSearcher.searching_user_in_database(database_source="workWithUsersDatabase/UsersDatabase.txt",
                                                            user_id=f"id{event.object.peer_id}")
                    if UserSearcher.presence_user == []:
                        write_msg(user_id=event.object.peer_id, keyboard=main_keyboard,
                                  message=f"Теперь регистрацию можно осуществить прямо тут - для этого введи название своей группы русскими символами (если не получиться с первого раза - попробуй ещё раз)😜\nВот список всех существующих групп в Предуниверсарии МАИ:\n8️⃣Класс: {'; '.join(BotConfig.EightClassGroups)}\n9️⃣Класс: {'; '.join(BotConfig.NineClassGroups)}\n1️⃣0️⃣Класс: {'; '.join(BotConfig.TenClassGroups)}\n1️⃣1️⃣Класс: {'; '.join(BotConfig.ElevenClassGroups)}\nЕсли ты не можешь найти свою группу или тебе нужна помощь, то пиши в беседу, прикреплённую к сообществу:\nhttps://vk.me/join/FhSVyJp7fYT0fM805_KTHNWPctDNa79JGsI=")
                    else:
                        write_msg(user_id=event.object.peer_id, keyboard=main_keyboard,
                                  message=f"Ты уже зарегистрирован - если всё работает отлично, то ты также можешь продолжать пользоваться ботом. Если же у тебя есть какие-либо вопросы или ты сменил группу, то пиши в беседу, прикреплённую к сообществу⚙\nhttps://vk.me/join/FhSVyJp7fYT0fM805_KTHNWPctDNa79JGsI=")
                # registration - the process of entering users in the database
                elif (event.object.text.upper() in BotConfig.EightClassGroups) or (
                        event.object.text.upper() in BotConfig.NineClassGroups) or (
                        event.object.text.upper() in BotConfig.TenClassGroups) or (
                        event.object.text.upper() in BotConfig.ElevenClassGroups) or (
                        event.object.text.upper() in ["ГОСТЬ", "ТЕСТ", "GUEST", "TEST"]) or (
                        event.object.text.upper() in BotConfig.TeachersCodifiers):
                    UserSearcher.searching_user_in_database(database_source="workWithUsersDatabase/UsersDatabase.txt",
                                                            user_id=f"id{event.object.peer_id}")
                    if UserSearcher.presence_user == []:
                        get_last_name = vk.method("users.get", {"user_ids": event.object.peer_id})[0]["last_name"]
                        get_first_name = vk.method("users.get", {"user_ids": event.object.peer_id})[0]["first_name"]
                        if event.object.text.upper() in BotConfig.EightClassGroups:
                            UserSearcher.adding_user_in_database(
                                database_source="workWithUsersDatabase/UsersDatabase.txt",
                                full_name=f"{get_last_name} {get_first_name}", user_id=f"id{event.object.peer_id}",
                                source_for_user="8class", sheet_name=event.object.text.upper(),
                                columns_for_user=['A', 'B', 'D', 'E', 'F'], extra_cells=1)
                            sending_and_reserving_database(conversation_id=event.object.from_id,
                                                           database_source="workWithUsersDatabase/UsersDatabase.txt",
                                                           message=f"#JOIN К нам присоединился новый пользователь - {get_last_name} {get_first_name}(id{event.object.peer_id} | 8class | {event.object.text.upper()})🚀")
                            write_msg(user_id=event.object.peer_id, keyboard=main_keyboard,
                                      message="Поздравляю! Регистрация прошла успешно✅")
                        elif event.object.text.upper() in BotConfig.NineClassGroups:
                            UserSearcher.adding_user_in_database(
                                database_source="workWithUsersDatabase/UsersDatabase.txt",
                                full_name=f"{get_last_name} {get_first_name}", user_id=f"id{event.object.peer_id}",
                                source_for_user="9class", sheet_name=event.object.text.upper(),
                                columns_for_user=['A', 'B', 'D', 'E', 'F'], extra_cells=1)
                            sending_and_reserving_database(conversation_id=event.object.from_id,
                                                           database_source="workWithUsersDatabase/UsersDatabase.txt",
                                                           message=f"#JOIN К нам присоединился новый пользователь - {get_last_name} {get_first_name}(id{event.object.peer_id} | 9class | {event.object.text.upper()})🚀")
                            write_msg(user_id=event.object.peer_id, keyboard=main_keyboard,
                                      message="Поздравляю! Регистрация прошла успешно✅")
                        elif event.object.text.upper() in BotConfig.TenClassGroups:
                            UserSearcher.adding_user_in_database(
                                database_source="workWithUsersDatabase/UsersDatabase.txt",
                                full_name=f"{get_last_name} {get_first_name}", user_id=f"id{event.object.peer_id}",
                                source_for_user="10class", sheet_name=event.object.text.upper(),
                                columns_for_user=['A', 'B', 'D', 'E', 'F'], extra_cells=1)
                            sending_and_reserving_database(conversation_id=event.object.from_id,
                                                           database_source="workWithUsersDatabase/UsersDatabase.txt",
                                                           message=f"#JOIN К нам присоединился новый пользователь - {get_last_name} {get_first_name}(id{event.object.peer_id} | 10class | {event.object.text.upper()})🚀")
                            write_msg(user_id=event.object.peer_id, keyboard=main_keyboard,
                                      message="Поздравляю! Регистрация прошла успешно✅")
                        elif event.object.text.upper() in BotConfig.ElevenClassGroups:
                            UserSearcher.adding_user_in_database(
                                database_source="workWithUsersDatabase/UsersDatabase.txt",
                                full_name=f"{get_last_name} {get_first_name}", user_id=f"id{event.object.peer_id}",
                                source_for_user="11class", sheet_name=event.object.text.upper(),
                                columns_for_user=['A', 'B', 'D', 'E', 'F'], extra_cells=1)
                            sending_and_reserving_database(conversation_id=event.object.from_id,
                                                           database_source="workWithUsersDatabase/UsersDatabase.txt",
                                                           message=f"#JOIN К нам присоединился новый пользователь - {get_last_name} {get_first_name}(id{event.object.peer_id} | 11class | {event.object.text.upper()})🚀")
                            write_msg(user_id=event.object.peer_id, keyboard=main_keyboard,
                                      message="Поздравляю! Регистрация прошла успешно✅")
                        elif event.object.text.upper() in ["ГОСТЬ", "ТЕСТ", "GUEST", "TEST"]:
                            UserSearcher.adding_user_in_database(
                                database_source="workWithUsersDatabase/UsersDatabase.txt",
                                full_name=f"{get_last_name} {get_first_name}", user_id=f"id{event.object.peer_id}",
                                source_for_user="GUESTS", sheet_name="ГОСТЬ",
                                columns_for_user=['A', 'B', 'D', 'E', 'F'], extra_cells=0)
                            sending_and_reserving_database(conversation_id=event.object.from_id,
                                                           database_source="workWithUsersDatabase/UsersDatabase.txt",
                                                           message=f"#JOIN Кто-то захотел протестировать бота - {get_last_name} {get_first_name}(id{event.object.peer_id} | GUESTS | ГОСТЬ)🔭")
                            write_msg(user_id=event.object.peer_id, keyboard=main_keyboard,
                                      message="Поздравляем! Регистрация прошла успешно✅")
                            write_msg(user_id=event.object.peer_id, keyboard=main_keyboard,
                                      message="Теперь вы имеете абсолютно все возможности, чтобы полноценно протестировать нашего бота🎳")
                        elif event.object.text in BotConfig.TeachersCodifiers:
                            UserSearcher.adding_user_in_database(
                                database_source="workWithUsersDatabase/UsersDatabase.txt",
                                full_name=f"{get_last_name} {get_first_name}", user_id=f"id{event.object.peer_id}",
                                source_for_user="TEACHERS", sheet_name=event.object.text.upper(),
                                columns_for_user=['A', 'B', 'D', 'E', 'F'], extra_cells=0)
                            sending_and_reserving_database(conversation_id=event.object.from_id,
                                                           database_source="workWithUsersDatabase/UsersDatabase.txt",
                                                           message=f"#JOIN К нам присоединился новый педагог - {get_last_name} {get_first_name}(id{event.object.peer_id} | TEACHERS | {event.object.text.upper()})🎓")
                            write_msg(user_id=event.object.peer_id, keyboard=main_keyboard,
                                      message="Поздравляю! Регистрация прошла успешно✅")
                    else:
                        if event.object.text.upper() == UserSearcher.presence_user[3]:
                            write_msg(user_id=event.object.peer_id, keyboard=main_keyboard,
                                      message="Да-да, всё внесено верно - ты есть в базе. Если есть какие-то вопросы, то пиши в беседу, прикреплённую к сообществу🗿\nhttps://vk.me/join/FhSVyJp7fYT0fM805_KTHNWPctDNa79JGsI=")
                        else:
                            write_msg(user_id=event.object.peer_id, keyboard=main_keyboard,
                                      message=f"Ого - похоже ты хочешь изменить группу! Напиши в беседу, прикреплённую к сообществу, чтобы мы редактировали твои данные✍\nhttps://vk.me/join/FhSVyJp7fYT0fM805_KTHNWPctDNa79JGsI=")
                # get your data from the database
                elif event.object.text.lower() in ["я", "кто я", "хто я", "мои данные"]:
                    UserSearcher.searching_user_in_database(database_source="workWithUsersDatabase/UsersDatabase.txt",
                                                            user_id=f"id{event.object.peer_id}")
                    if UserSearcher.presence_user != []:
                        write_msg(user_id=event.object.peer_id, keyboard=main_keyboard,
                                  message=f"Вот твои данные, которые ты внёс при регистрации: {UserSearcher.presence_user[0]} | {UserSearcher.presence_user[1]} | {UserSearcher.presence_user[2]} | {UserSearcher.presence_user[3]}💾")
                    else:
                        write_msg(user_id=event.object.peer_id, keyboard=main_keyboard,
                                  message=f"Ты ещё не зарегистрировался, бот пока знает про тебя только это: id{event.object.peer_id}📡")
                # 3301 - easter egg
                elif event.object.text.lower() == "пасхалка":
                    write_msg(user_id=event.object.peer_id, keyboard=main_keyboard,
                              message="Пасхалка?! Вау, в боте есть пасхалка! Приступим, есть шифр, указанный в пикче ниже - расшифруй его и отпишись в общую беседу сообщества(понимаем, что довольно сложно, поэтому даём две подсказки: ascii, tenet)",
                              attachment=update_attachment_id(img_source="EasterEgg.png"))
                # check for updates
                elif event.object.text.lower() == "проверить обновления":
                    write_msg(user_id=event.object.peer_id, keyboard=main_keyboard,
                              message="Оооу да - а вот и долгожданное обновление! Мы славно поработали и надеемся, что тебе всё понравится😎")
                # unrecognized command
                else:
                    write_msg(user_id=event.object.peer_id, keyboard=main_keyboard,
                              message="По-моему ты вводишь что-то не так, попробуй ещё раз😕")
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
