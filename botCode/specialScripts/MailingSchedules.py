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
from random import randint as randint
import time as time
import datetime as datetime
# import of other self-written modules
from configurationFile import BotConfig as BotConfig
from workWithUsersDatabase import UserSearcher as UserSearcher
from workWithExcelFile import ExcelSearcher as ExcelSearcher


# sending out an individual schedule at a certain time
def sending_out_a_daily_schedule(time_of_mailing, users_data_for_mailing_schedules):
    # working with each user in turn, sending up-to-date data
    for user_data in users_data_for_mailing_schedules:
        try:
            # search for the required schedule for the user at a certain point in time
            user_schedule = ExcelSearcher.selective_data_search(excel_source=user_data[1][0],
                                                                sheet_name=user_data[1][1], columns=user_data[1][2],
                                                                extra_cells=user_data[1][3], start_data=
                                                                ["Понедельник", "Вторник", "Среда", "Четверг",
                                                                 "Пятница", "Суббота"][(
                                                                                               datetime.datetime.today().weekday() + (
                                                                                           0 if 0 <= int("".join(
                                                                                               time_of_mailing.split(
                                                                                                   ":"))) < 1200 else 1)) % 7],
                                                                end_data="None",
                                                                importance_of_the_error=BotConfig.error_checking_switch)
            # generating a response and sending the received data
            vk_session_for_mailing_schedules.method("messages.send", {"peer_id": user_data[0],
                                                                      "message": f"🔔Ку, сейчас {time_of_mailing}, а {'сегодня уже' if 0 <= int(''.join(time_of_mailing.split(':'))) < 1200 else 'уже скоро'} {['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота'][(datetime.datetime.today().weekday() + (0 if 0 <= int(''.join(time_of_mailing.split(':'))) < 1200 else 1)) % 7]} - начинаю поиск актуального расписания для тебя на {'текущий день' if 0 <= int(''.join(time_of_mailing.split(':'))) < 1200 else 'завтра'}",
                                                                      "keyboard": None, "sticker_id": None,
                                                                      "attachment": None,
                                                                      "random_id": randint(1, 100000000)})
            vk_session_for_mailing_schedules.method("messages.send", {"peer_id": user_data[0], "message": user_schedule,
                                                                      "keyboard": None, "sticker_id": None,
                                                                      "attachment": None,
                                                                      "random_id": randint(1, 100000000)})
            vk_session_for_mailing_schedules.method("messages.send", {"peer_id": user_data[0],
                                                                      "message": BotConfig.unified_schedule_calls[0],
                                                                      "keyboard": None, "sticker_id": None,
                                                                      "attachment": None,
                                                                      "random_id": randint(1, 100000000)})
            # waiting for the end of the vk timeout for safety reasons
            time.sleep(0.5)
        # catching an access error when sending messages to the user and sending the error to the terminal, if required
        except Exception as E:
            if BotConfig.error_checking_switch != False:
                print(f"Error in MailingSchedules - {E}")


# automatic function for sending the schedule for the next day
def daily_mailing_time_handler():
    # checking for the time to send the daily schedule later
    while True:
        # getting up-to-date data and subsequent time processing
        users_data_for_mailing_schedules = UserSearcher.data_about_daily_mailings_of_the_schedule(
            database_source="workWithUsersDatabase/UsersDatabase.txt")
        for time_of_mailing in users_data_for_mailing_schedules.keys():
            # analysis for the relevance of the time period
            if int("".join(time_of_mailing.split(":")) + "00") <= int(
                    "".join(str(datetime.datetime.today().time()).split(":"))[:6]) < int(
                    "".join(time_of_mailing.split(":")) + str(BotConfig.reboot_time % 100 // 10) + str(
                            BotConfig.reboot_time % 100 % 10)) and (datetime.datetime.today().weekday() + (
            0 if 0 <= int("".join(time_of_mailing.split(":"))) < 1200 else 1)) % 7 != 6:
                # start of distribution by parallel execution
                Thread(target=sending_out_a_daily_schedule,
                       args=(time_of_mailing, users_data_for_mailing_schedules[time_of_mailing])).start()
        # waiting until the next request
        time.sleep(BotConfig.reboot_time % 100)


# the main function for running a telegram binder is to collect statistics and some data from public channels
def working_with_the_telegram_binder():
    # declaring a global object for further work with it
    global vk_session_for_mailing_schedules
    # is automatic restart mandatory
    if BotConfig.error_checking_switch != True:
        # for a permanent bot job with auto-reconnection
        while True:
            try:
                # initializing work with the vk api, launching the bot into the network
                vk_session_for_mailing_schedules = vk_api.VkApi(token=f"{BotConfig.VK_BotToken}")
                vk_session_for_mailing_schedules._auth_token()
                vk_session_for_mailing_schedules.get_api()
                # launch the main function for sending the schedule at a certain time
                daily_mailing_time_handler()
            except Exception as E:
                # auto-reconnect the bot after a while
                time.sleep(BotConfig.reboot_time % 100)
    else:
        # initializing work with the vk api, launching the bot into the network
        vk_session_for_mailing_schedules = vk_api.VkApi(token=f"{BotConfig.VK_BotToken}")
        vk_session_for_mailing_schedules._auth_token()
        vk_session_for_mailing_schedules.get_api()
        # launch the main function for sending the schedule at a certain time
        daily_mailing_time_handler()

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
