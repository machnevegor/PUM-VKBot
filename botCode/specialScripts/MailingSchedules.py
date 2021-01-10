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
from random import randint as randint
import time as time
import datetime as datetime
# import of other self-written modules
from configurationFile import BotConfig as BotConfig
from workWithUsersDatabase import UserSearcher as UserSearcher
from workWithExcelFile import ExcelSearcher as ExcelSearcher


# automatic function for sending the schedule for the next day
def daily_schedule_newsletter():
    # waiting for the scheduled time to send out schedules
    while True:
        # if the request is made in a suitable time interval, the mailing list starts
        if int("".join(BotConfig.daily_mailing_time.split(":")) + "00") <= int(
                "".join(str(datetime.datetime.today().time()).split(":"))[:6]) <= int(
            "".join(BotConfig.daily_mailing_time.split(":")) + str(BotConfig.reboot_time % 100 // 10) + str(
                BotConfig.reboot_time % 100 % 10)) and datetime.datetime.today().weekday() != 5:
            # work with each user individually to create the right content
            for user_id_from_shared_database in UserSearcher.get_all_user_IDs_from_database(
                    database_source="workWithUsersDatabase/UsersDatabase.txt"):
                try:
                    # checking whether notifications are enabled for the user
                    presence_user = UserSearcher.searching_user_in_database(
                        database_source="workWithUsersDatabase/UsersDatabase.txt",
                        user_id=f"id{user_id_from_shared_database}")
                    if presence_user[6] != 0:
                        # search and translate the day of the week to the next day
                        day_of_the_week = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"][
                            (datetime.datetime.today().weekday() + 1) % 7]
                        # search for the required schedule for the user for the next day
                        user_schedule = ExcelSearcher.selective_data_search(excel_source=presence_user[2],
                                                                            sheet_name=presence_user[3],
                                                                            columns=presence_user[4],
                                                                            extra_cells=presence_user[5],
                                                                            start_data=day_of_the_week, end_data="None",
                                                                            importance_of_the_error=BotConfig.error_checking_switch)
                        # generating a response and sending the received data
                        vk_session_for_mailing_schedules.method("messages.send",
                                                                {"peer_id": user_id_from_shared_database,
                                                                 "message": f"🔔Ку, сейчас около {BotConfig.daily_mailing_time}, а уже скоро {day_of_the_week.lower()}, поэтому лови своё расписание на завтра",
                                                                 "keyboard": None, "sticker_id": None,
                                                                 "attachment": None,
                                                                 "random_id": randint(1, 100000000)})
                        vk_session_for_mailing_schedules.method("messages.send",
                                                                {"peer_id": user_id_from_shared_database,
                                                                 "message": f"\n{user_schedule}",
                                                                 "keyboard": None, "sticker_id": None,
                                                                 "attachment": None,
                                                                 "random_id": randint(1, 100000000)})
                        vk_session_for_mailing_schedules.method("messages.send",
                                                                {"peer_id": user_id_from_shared_database,
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
                daily_schedule_newsletter()
            except Exception as E:
                # auto-reconnect the bot after a while
                time.sleep(BotConfig.reboot_time % 100)
    else:
        # initializing work with the vk api, launching the bot into the network
        vk_session_for_mailing_schedules = vk_api.VkApi(token=f"{BotConfig.VK_BotToken}")
        vk_session_for_mailing_schedules._auth_token()
        vk_session_for_mailing_schedules.get_api()
        # launch the main function for sending the schedule at a certain time
        daily_schedule_newsletter()

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
