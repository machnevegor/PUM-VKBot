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
import time as time
import datetime as datetime
# import other modules
from configurationFile import BotConfig as BotConfig
from workWithUsersDatabase import UserSearcher
from workWithExcelFile import ExcelSearcher as ExcelSearcher

# reboot time
reboot_time = 5
# system array
groups_id_array = ["187254286"]

# information about developers
about_bot = [
    "Данного бота по фану запилили рандомные челики из ПУМа. Этот бот отличается от всех других тем, что импортирует всю информацию из базы данных школы, а не тупо по написанным строкам разработчиков. Бот продуман, но не идеален, поэтому все вопросы можете задавать в беседу, прикреплённую к сообществу бота. Также хочется напомнить, что у нас есть discord сервер для разработчиков, на котором вы сможете найти себе команду для проекта, узнать что-то новое или присоединится к чьей-то идеи:\nhttps://smtechnology.info😊"]
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
            [get_button(label="Получить ID", color="primary"),
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
    schedules_keyboard = json.dumps(schedules_keyboard, ensure_ascii=False).encode("utf-8")
    schedules_keyboard = str(schedules_keyboard.decode("utf-8"))
    select_call_class_keyboard = json.dumps(select_call_class_keyboard, ensure_ascii=False).encode("utf-8")
    select_call_class_keyboard = str(select_call_class_keyboard.decode("utf-8"))
    choosing_day_of_week_keyboard = json.dumps(choosing_day_of_week_keyboard, ensure_ascii=False).encode("utf-8")
    choosing_day_of_week_keyboard = str(choosing_day_of_week_keyboard.decode("utf-8"))

    # sending messages
    def write_msg(id, message, keyboard=None, sticker_id=None, attachment=None):
        # sending data to the terminal
        print("Responce:", "".join(message))
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
                    write_msg(event.object.peer_id,
                              "Не забывайте, что всю актуальную информацию о боте вы можете найти на стене нашего сообщества, поэтому, если бот не отвечает, вы знаете, что делать😉",
                              keyboard=main_keyboard, attachment="photo222338543_457245710_4c9cbdcfb8eba61348")
                # schedules keyboard
                elif event.object.text.lower() == "звонков":
                    write_msg(event.object.peer_id, "Такс, и ещё выбери для каких классов🤔",
                              keyboard=select_call_class_keyboard)
                elif event.object.text.lower() == "уроков":
                    write_msg(event.object.peer_id, "Хмм, теперь выбери день😼", keyboard=choosing_day_of_week_keyboard)
                # select call class keyboard
                elif event.object.text.lower() == "8-9":
                    write_msg(event.object.peer_id, eight_nine_schedule_calls, keyboard=main_keyboard)
                elif event.object.text.lower() == "10-11":
                    write_msg(event.object.peer_id, ten_eleven_schedule_calls, keyboard=main_keyboard)
                # choosing day of week keyboard
                elif (event.object.text.lower() == "понедельник"):
                    UserSearcher.searching_user_in_database(database_source="workWithUsersDatabase/UsersDatabase.txt",
                                                            user_id=f"id{event.object.peer_id}")
                    if UserSearcher.presence_user == []:
                        write_msg(event.object.peer_id,
                                  f"Такс, тебя же нет в базе. Лови свой VK-ID(id{event.object.peer_id}) и пиши в основную беседу, прикрепленную к сообществу - там тебе помогут решить данную проблему✌",
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
                elif (event.object.text.lower() == "вторник"):
                    UserSearcher.searching_user_in_database(database_source="workWithUsersDatabase/UsersDatabase.txt",
                                                            user_id=f"id{event.object.peer_id}")
                    if UserSearcher.presence_user == []:
                        write_msg(event.object.peer_id,
                                  f"Такс, тебя же нет в базе. Лови свой VK-ID(id{event.object.peer_id}) и пиши в основную беседу, прикрепленную к сообществу - там тебе помогут решить данную проблему✌",
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
                elif (event.object.text.lower() == "среда"):
                    UserSearcher.searching_user_in_database(database_source="workWithUsersDatabase/UsersDatabase.txt",
                                                            user_id=f"id{event.object.peer_id}")
                    if UserSearcher.presence_user == []:
                        write_msg(event.object.peer_id,
                                  f"Такс, тебя же нет в базе. Лови свой VK-ID(id{event.object.peer_id}) и пиши в основную беседу, прикрепленную к сообществу - там тебе помогут решить данную проблему✌",
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
                elif (event.object.text.lower() == "четверг"):
                    UserSearcher.searching_user_in_database(database_source="workWithUsersDatabase/UsersDatabase.txt",
                                                            user_id=f"id{event.object.peer_id}")
                    if UserSearcher.presence_user == []:
                        write_msg(event.object.peer_id,
                                  f"Такс, тебя же нет в базе. Лови свой VK-ID(id{event.object.peer_id}) и пиши в основную беседу, прикрепленную к сообществу - там тебе помогут решить данную проблему✌",
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
                elif (event.object.text.lower() == "пятница"):
                    UserSearcher.searching_user_in_database(database_source="workWithUsersDatabase/UsersDatabase.txt",
                                                            user_id=f"id{event.object.peer_id}")
                    if UserSearcher.presence_user == []:
                        write_msg(event.object.peer_id,
                                  f"Такс, тебя же нет в базе. Лови свой VK-ID(id{event.object.peer_id}) и пиши в основную беседу, прикрепленную к сообществу - там тебе помогут решить данную проблему✌",
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
                elif (event.object.text.lower() == "суббота"):
                    UserSearcher.searching_user_in_database(database_source="workWithUsersDatabase/UsersDatabase.txt",
                                                            user_id=f"id{event.object.peer_id}")
                    if UserSearcher.presence_user == []:
                        write_msg(event.object.peer_id,
                                  f"Такс, тебя же нет в базе. Лови свой VK-ID(id{event.object.peer_id}) и пиши в основную беседу, прикрепленную к сообществу - там тебе помогут решить данную проблему✌",
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
                # easter egg
                elif event.object.text.lower() == "пасхалка":
                    write_msg(event.object.peer_id,
                              "Пасхалка?! Вау, в боте есть пасхалка! Приступим, есть шифр, указанный в пикче ниже - расшифруй его и отпишись в общую беседу сообщества(понимаем, что довольно сложно, поэтому даём две подсказки: ascii, tenet)",
                              keyboard=main_keyboard, attachment="photo222338543_457245709_c2475e60dc624529c3")
                # check for updates
                elif event.object.text.lower() == "проверить обновления":
                    write_msg(event.object.peer_id,
                              "Оооу да - а вот и долгожданное обновление! Мы славно поработали и надеемся, что тебе всё понравится😎",
                              keyboard=main_keyboard)
                # get VK-ID
                elif event.object.text.lower() == "получить id":
                    write_msg(event.object.peer_id, f"Твой персональный ID в ВК: id{event.object.peer_id}",
                              keyboard=main_keyboard)
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
