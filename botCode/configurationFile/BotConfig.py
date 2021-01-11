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

########################################################################################################################

# CONFIGURING API PARAMETERS FOR FURTHER OPERATION OF THE BOT
# tokens for messengers where the bot is used
VK_BotToken = ""
Telegram_BotToken = ""
# some parameters for the bot to work with vk
CommunityID = ["187254286"]
ConversationForDataReservationID = 2000000004
# ID of all Telegram channels from which the bot can collect statistics and various data
AllowedChannelIDs = dict({"-1001353946381": "t.me/joinchat/AAAAAFCzlQ0JK_lfHe3nuA"})

########################################################################################################################

# BASIC SYSTEM PARAMETERS FOR STABLE OPERATION OF THE BOT
# full error log output (without auto-reconnection)
error_checking_switch = False
# time to restart the bot
reboot_time = 5
# permission to distribute links for zoom conferences
permission_to_distribute_links = True

########################################################################################################################

# DICTIONARY FOR BUTTONS BACK AND GREETINGS
# array for the back button
buttons_back = ["здравствуй", "привет", "хай", "куку", "ку", "салам", "саламалейкум", "здарова", "дыдова", "начать",
                "главное меню", "меню", "плитки", "клавиатура", "назад", "hello", "hey", "hi", "qq", "q", "start",
                "main menu", "menu", "tiles", "keyboard", "back"]
# array for the welcome words
ru_greetings_bot = ["здравствуй", "привет", "хай", "ку", "салам", "здарова", "дыдова"]
eng_greetings_bot = ["hello", "hey", "hi", "qq", "q"]

########################################################################################################################

# BASIC CONTENT DICTIONARIES FOR MORE STRUCTURED AND ORDERED STORAGE
# information about developers
about_bot = [
    "Данную систему поиска актуального расписания запилили рандомные пчелики из Предуниверсария МАИ. Этот бот отличается от всех других тем, что импортирует всю информацию из базы данных школы, а не по написанным строкам разработчиков. Алгоритм продуман, но не идеален - мы держим постоянную обратную связь, поэтому ты всегда можешь принять участие в обсуждении или задать все свои вопросы в беседе, прикреплённой к сообществу🤙\nhttps://vk.me/join/FhSVyJp7fYT0fM805_KTHNWPctDNa79JGsI=",
    "Ещё хочется напомнить, что у нас есть свой сервер в Discord для разработчиков, на котором ты сможешь найти себе команду для проекта, узнать что-то новое или присоединиться к чьей-то идее:\nhttps://smtechnology.info😊",
    "Не забывай, что всю актуальную информацию ты сможешь найти на стене нашего сообщества, поэтому, если бот не отвечает, ты знаешь, что делать😉"]
# call schedule for all classes
unified_schedule_calls = [
    "🧾Расписание звонков:\n ┣ 1. 9:00 - 9:45 | 5 минут\n ┣ 2. 9:50 - 10:35 | 10 минут\n ┣ 3. 10:45 - 11:30 | 20 минут\n ┣ 4. 11:50 - 12:35 | 10 минут\n ┣ 5. 12:45 - 13:30 | 10 минут\n ┣ 6. 13:40 - 14:25 | 20 минут\n ┣ 7. 14:45 - 15:30 | 10 минут\n ┣ 8. 15:40 - 16:25 | 5 минут\n ┣ 9. 16:30 - 17:15 | 5 минут\n ┗ 10. 17:20 - 18:05"]
# links to all Zoom tables
links_to_zoom = ["https://docs.google.com/spreadsheets/d/1Mn9NvgjTzuV_58nuDSwYktbGjh0VrvmooraagtNZoPE/edit?usp=sharing",
                 "https://docs.google.com/spreadsheets/d/1AIsQ3kxxL8RjX1Gdx8UaiAZ0-mtl6-WvZ-UOm7kLJNM/edit?usp=sharing",
                 "https://docs.google.com/spreadsheets/d/14zsNfFTtXy4GrHBOFS7NZL7zyee8ERTjZtxsOcAdiyk/edit?usp=sharing",
                 "https://docs.google.com/spreadsheets/d/1BZvU8OxUxdVae4cmRayTC32cQ3YvvbZRjo5JkmWpWvA/edit?usp=sharing",
                 "https://docs.google.com/spreadsheets/d/1xKeun8QuUR3HViN6kpXOC9AP7HJWyMUwddzEXm4wSyU/edit?usp=sharing"]

########################################################################################################################

# EVERYTHING FOR GETTING DATA FROM NEWS SITES
# user agent for search engine
user_agent = {
    "User-Agent": "PUM-VKBot | Official bot for finding the schedule in the MAI pre-University: https://vk.com/pumvkbot"}
# weather search - paths
weather_source = "https://sinoptik.com.ru/погода-москва"
weather_search_tag, weather_tag_info = "div", {"class": "weather__article_description-text"}
# news search - paths
news_source = "https://preduniversariy-mai.mskobr.ru/novosti"
news_search_tag, news_tag_info = "div", {"class": "kris-news-box"}
# COVID-19 search - paths
covid_source = "https://ncov.blog/countries/ru/77/"
covid_search_tag, covid_tag_info = "div", {"itemprop": "text"}

########################################################################################################################

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
