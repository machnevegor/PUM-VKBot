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
id_array = []
buttons_back = ["здравствуй", "привет", "хай", "куку", "ку", "салам", "саламалейкум", "здарова", "дыдова", "начать",
                "главное меню", "меню", "плитки", "клавиатура", "назад", "hello", "hey", "hi", "qq", "q", "start",
                "main menu", "menu", "tiles", "keyboard", "back"]
# auxiliary arrays
ru_greetings_bot = ["Здравствуй", "Привет", "Хай", "Ку", "Салам", "Здарова", "Дыдова"]
eng_greetings_bot = ["Hello", "Hey", "Hi", "Qq", "Q"]


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
         get_button(label="Расписание", color="positive")]
    ]
}

schedules_keyboard = {
    "one_time": False,
    "buttons": [
        [get_button(label="Звонков", color="primary"),
         get_button(label="Уроков", color="positive")],
    ]
}

lessons_keyboard = {
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

# vk connect
vk = vk_api.VkApi(token=BotConfig.BotToken)
vk._auth_token()
vk.get_api()

# json
main_keyboard = json.dumps(main_keyboard, ensure_ascii=False).encode("utf-8")
main_keyboard = str(main_keyboard.decode("utf-8"))
schedules_keyboard = json.dumps(schedules_keyboard, ensure_ascii=False).encode("utf-8")
schedules_keyboard = str(schedules_keyboard.decode("utf-8"))
lessons_keyboard = json.dumps(lessons_keyboard, ensure_ascii=False).encode("utf-8")
lessons_keyboard = str(lessons_keyboard.decode("utf-8"))

# response logic
for event in longpoll.listen():
    # processing a new message
    if event.type == VkBotEventType.MESSAGE_NEW:
        # if the request is from in private messages
        if event.object.peer_id == event.object.from_id:
            # if this user is not already in the database
            if event.object.peer_id not in id_array:
                id_array.append(event.object.peer_id)
            # if the back buttons are pressed
            if event.object.text.lower() in buttons_back:
                # greetings and jump to main menu
                if event.object.text.lower() in ru_greetings_bot:
                    response_randomizer = randint(0, len(VariationPhrases.ru_greetings_bot) - 1)
                    response_word = VariationPhrases.ru_greetings_bot[response_randomizer]
                    get_user_name = vk.method("users.get", {"user_ids": event.object.peer_id})[0]["first_name"]
                    write_msg(event.object.peer_id, f"{response_word}, {str(get_user_name)}!", keyboard=main_keyboard)
                elif event.object.text.lower() in ["hello", "hey", "hi", "qq", "q"]:
                    response_randomizer = randint(0, len(VariationPhrases.eng_greetings_bot) - 1)
                    response_word = VariationPhrases.eng_greetings_bot[response_randomizer]
                    get_user_name = vk.method("users.get", {"user_ids": event.object.peer_id})[0]["first_name"]
                    write_msg(event.object.peer_id, f"{response_word}, {str(get_user_name)}!", keyboard=main_keyboard)
                # only jump to main menu
                else:
                    write_msg(event.object.peer_id, "Главное меню👌", keyboard=main_keyboard)
            # processing tile clicks
            elif event.object.text.lower() == "расписание":
                write_msg(event.object.peer_id, 'Ок, только выбери какое🖖', keyboard=schedules_keyboard)
            elif event.object.text.lower() == "звонков":
                write_msg(event.object.peer_id,
                          "Расписание звонков:\n1. 9:00 - 9:45\n2. 9:50 - 10:35\n3. 10:45 - 11:30\n4. 11:50 - 12:35\n5. 12:45 - 13:30\n6. 13:40 - 14:25\n7. 14:45 - 15:30\n8. 15:40 - 16:25\n9. 16:30 - 17:15\n10. 17:20 - 18:05")
            elif event.object.text.lower() == "уроков":
                write_msg(event.object.peer_id, 'Такс, выбери день🗓', keyboard=lessons_keyboard)
            elif event.object.text.lower() == "понедельник":
                ExcelSearcher.selective_data_search(excel_source="excelDatabase/10class/10_3class.xlsx",
                                                    columns=["A", "B"],
                                                    start_data="Понедельник", end_data="None")
                write_msg(event.object.peer_id, ExcelSearcher.output_day_schedule, keyboard=main_keyboard)
            elif event.object.text.lower() == "вторник":
                write_msg(event.object.peer_id, "Кхм, у 10 классов сегодня технопарк, поэтому смотри сам🕶",
                          keyboard=main_keyboard)
            elif event.object.text.lower() == "среда":
                ExcelSearcher.selective_data_search(excel_source="excelDatabase/10class/10_3class.xlsx",
                                                    columns=["A", "B"],
                                                    start_data="Среда", end_data="None")
                write_msg(event.object.peer_id, ExcelSearcher.output_day_schedule, keyboard=main_keyboard)
            elif event.object.text.lower() == "четверг":
                ExcelSearcher.selective_data_search(excel_source="excelDatabase/10class/10_3class.xlsx",
                                                    columns=["A", "B"],
                                                    start_data="Четверг", end_data="None")
                write_msg(event.object.peer_id, ExcelSearcher.output_day_schedule, keyboard=main_keyboard)
            elif event.object.text.lower() == "пятница":
                ExcelSearcher.selective_data_search(excel_source="excelDatabase/10class/10_3class.xlsx",
                                                    columns=["A", "B"],
                                                    start_data="Пятница", end_data="None")
                write_msg(event.object.peer_id, ExcelSearcher.output_day_schedule, keyboard=main_keyboard)
            elif event.object.text.lower() == "суббота":
                ExcelSearcher.selective_data_search(excel_source="excelDatabase/10class/10_3class.xlsx",
                                                    columns=["A", "B"],
                                                    start_data="Суббота", end_data="None")
                write_msg(event.object.peer_id, ExcelSearcher.output_day_schedule, keyboard=main_keyboard)
            else:
                write_msg(event.object.peer_id, "Ты точно команду написал:/", keyboard=main_keyboard)

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
