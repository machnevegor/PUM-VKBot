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
import vk_api as vk_api
import telebot as telebot
from telebot import types as types
from random import randint as randint
import time as time
# import of other self-written modules
from configurationFile import BotConfig as BotConfig
from workWithUsersDatabase import UserSearcher as UserSearcher

# initializing about working with the telegram api
bot = telebot.TeleBot(BotConfig.Telegram_BotToken)


# processing regular requests from users
@bot.message_handler()
def working_with_messages_from_users(message):
    # reply to a person if the message is private
    if message.chat.type == "private":
        # generating a response message and a keyboard for it
        bot.send_message(message.chat.id,
                         "Я ещё не умею общаться с людьми на таком странном языке, как «Телеграм», но ты всегда мне можешь написать в ВК - там я тебя всегда пойму и смогу сразу ответить👅",
                         parse_mode="html", reply_markup=types.InlineKeyboardMarkup().add(
                types.InlineKeyboardButton(text="Начать поиск расписания🔎", url="https://vk.com/pumvkbot")))


# sending notifications about new entries in telegram channels
@bot.channel_post_handler(
    content_types=["text", "audio", "document", "photo", "sticker", "video", "video_note", "voice", "contact", "dice",
                   "poll", "venue", "location"])
def posts_from_channels(message):
    if str(message.chat.id) in BotConfig.AllowedChannelIDs.keys():
        # formatting of the post that was received by the bot
        formatted_text = ("\n— " + "\n— ".join([paragraph_in_text for paragraph_in_text in "".join(
            [str(message.text)[character_in_text] for character_in_text in range(len(str(message.text))) if
             character_in_text < 200]).split("\n") if
                                                paragraph_in_text != ""]) + "..." if message.text != None else "📺Рекомендуется полный просмотр контента")
        # work with each user individually to create the right content
        for user_id_from_shared_database in UserSearcher.get_all_user_IDs_from_database(
                database_source="workWithUsersDatabase/UsersDatabase.txt"):
            try:
                # checking whether notifications are enabled for the user
                presence_user = UserSearcher.searching_user_in_database(
                    database_source="workWithUsersDatabase/UsersDatabase.txt",
                    user_id=f"id{user_id_from_shared_database}")
                if presence_user[8] != 0:
                    # sending a message to the user about a new post in a specific telegram channel
                    vk_session_for_telegram_alerts.method("messages.send", {"peer_id": user_id_from_shared_database,
                                                                            "message": f"🔔В телеграм-канале «{message.chat.title}» появился новый пост:\n{formatted_text}\n{f'Подробнее: {BotConfig.AllowedChannelIDs[str(message.chat.id)]}' if BotConfig.AllowedChannelIDs[str(message.chat.id)] != '' else ''}",
                                                                            "keyboard": None, "sticker_id": None,
                                                                            "attachment": None,
                                                                            "random_id": randint(1, 100000000)})
                    # waiting for the end of the vk timeout for safety reasons
                    time.sleep(0.5)
            # catching an access error when sending messages to the user and sending the error to the terminal, if required
            except Exception as E:
                if BotConfig.error_checking_switch != False:
                    print(f"Error in TelegramAlerts - {E}")


# the main function for running a telegram binder is to collect statistics and some data from public channels
def working_with_the_telegram_binder():
    # declaring a global object for further work with it
    global vk_session_for_telegram_alerts
    # is automatic restart mandatory
    if BotConfig.error_checking_switch != True:
        # for a permanent bot job with auto-reconnection
        while True:
            try:
                # initializing work with the vk api, launching the bot into the network
                vk_session_for_telegram_alerts = vk_api.VkApi(token=f"{BotConfig.VK_BotToken}")
                vk_session_for_telegram_alerts._auth_token()
                vk_session_for_telegram_alerts.get_api()
                # starting the main loop for telegram requests
                bot.polling(none_stop=True)
            except Exception as E:
                # auto-reconnect the bot after a while
                time.sleep(BotConfig.reboot_time % 100)
    else:
        # initializing work with the vk api, launching the bot into the network
        vk_session_for_telegram_alerts = vk_api.VkApi(token=f"{BotConfig.VK_BotToken}")
        vk_session_for_telegram_alerts._auth_token()
        vk_session_for_telegram_alerts.get_api()
        # starting the main loop for telegram requests
        bot.polling(none_stop=True)

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
