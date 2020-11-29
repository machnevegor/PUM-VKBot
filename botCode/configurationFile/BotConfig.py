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

# BASIC SYSTEM SETUP
# token for the bot
BotToken = "2a0137796fb9abcb4efd8640afc0727d5bc1ef5f4fe353804e705e4aaeca675d4b7195a299010bb160f03"

# community ID where the bot will be assigned
CommunityID = ["187254286"]

# talk to the reservation database
ConversationForDataReservationID = 2000000004

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

# SOME OUTPUT INFO
# information about developers
about_bot = [
    "Данную систему поиска актуального расписания запилили рандомные пчелики из ПУМ'а. Этот бот отличается от всех других тем, что импортирует всю информацию из базы данных школы, а не по написанным строкам разработчиков. Алгоритм продуман, но не идеален - мы держим постоянную обратную связь, поэтому вы можете принять участие в обсуждении или задать все свои вопросы в беседе, прикреплённой к сообществу🤙\nhttps://vk.me/join/FhSVyJp7fYT0fM805_KTHNWPctDNa79JGsI=",
    "Ещё хочется напомнить, что у нас есть Discord-сервер для разработчиков, на котором ты сможешь найти себе команду для проекта, узнать что-то новое или присоединиться к чьей-то идее:\nhttps://smtechnology.info😊",
    "Не забывай, что всю актуальную информацию ты сможешь найти на стене нашего сообщества, поэтому, если бот не отвечает, ты знаешь, что делать😉"]

# call schedule for all classes
eight_nine_schedule_calls = "Расписание звонков:\n1. 9:00 - 9:45\n2. 9:50 - 10:35\n3. 10:55 - 11:40\n4. 11:50 - 12:35\n5. 12:45 - 13:30\n6. 13:50 - 14:35\n7. 14:45 - 15:30\n8. 15:40 - 16:25\n9. 16:30 - 17:15\n10. 17:20 - 18:05"
ten_eleven_schedule_calls = "Расписание звонков:\n1. 9:00 - 9:45\n2. 9:50 - 10:35\n3. 10:45 - 11:30\n4. 11:50 - 12:35\n5. 12:45 - 13:30\n6. 13:40 - 14:25\n7. 14:45 - 15:30\n8. 15:40 - 16:25\n9. 16:30 - 17:15\n10. 17:20 - 18:05"

########################################################################################################################

# ALL CLASSES AND TEACHERS LISTED IN THE DATABASE
# all groups for all classes of the MAI pre-University
EightClassGroups = ["М-8-1-1, Ф-8-1", "М-8-1-2, Ф-8-1", "М-8-1-2, Ф-8-2", "М-8-2-1, Ф-8-1", "М-8-2-1, Ф-8-2",
                    "М-8-2-2, Ф-8-2"]

NineClassGroups = ["М-9-1, Ф-9-1, Р-9-1-2", "М-9-1, Ф-9-1, Р-9-2-1", "М-9-1, Ф-9-1, Р-9-3-1", "М-9-1, Ф-9-1, Р-9-3-2",
                   "М-9-1, Ф-9-2, Р-9-1-2", "М-9-1, Ф-9-2, Р-9-2-1", "М-9-1, Ф-9-2, Р-9-2-2", "М-9-1, Ф-9-2, Р-9-3-1",
                   "М-9-1, Ф-9-2, Р-9-3-2", "М-9-2, Ф-9-1, Р-9-1-2", "М-9-2, Ф-9-1, Р-9-2-1", "М-9-2, Ф-9-1, Р-9-3-1",
                   "М-9-2, Ф-9-1, Р-9-3-2", "М-9-2, Ф-9-2, Р-9-1-1", "М-9-2, Ф-9-2, Р-9-1-2", "М-9-2, Ф-9-2, Р-9-2-2",
                   "М-9-2, Ф-9-2, Р-9-3-1", "М-9-2, Ф-9-2, Р-9-3-2", "М-9-3, Ф-9-3, Р-9-1-1", "М-9-3, Ф-9-3, Р-9-1-2",
                   "М-9-3, Ф-9-3, Р-9-2-1", "М-9-3, Ф-9-3, Р-9-2-2", "М-9-3, Ф-9-3, Р-9-3-2"]

TenClassGroups = ["М-10-1, А-10-1", "М-10-1, А-10-2", "М-10-1, А-10-3", "М-10-2, А-10-1", "М-10-2, А-10-2",
                  "М-10-2, А-10-3", "М-10-3, А-10-1", "М-10-3, А-10-2", "М-10-3, А-10-3"]

ElevenClassGroups = ["М1, Ф1, М-1-1, Р-1-4, Л3", "М1, Ф1, М-1-1, Р-1-4, Л4", "М1, Ф1, М-1-1, Р-3, Л-3",
                     "М1, Ф1, М-2-1, Р1, Л3", "М1, Ф1, М-3-1, Р1, Л3", "М1, Ф1, М-3-1, Р-2, Л3",
                     "М1, Ф1, М-3-1, Р-3, Л3", "М1, Ф4, М-2-1, Р1, Л3", "М1, Ф4, М-3-1, Р1, Л3",
                     "М2, Ф2, М-2-1, Р1, Л2", "М2, Ф2, М-2-1, Р-3, Л2", "М2, Ф2, М-2-1, Р-3, Л3",
                     "М2, Ф2, М-2-1, Р4, Л4", "М2, Ф2, М-3-1, Р1, Л1", "М2, Ф2, М-3-1, Р1, Л2", "М2, Ф2, М-3-1, Р2, Л2",
                     "М2, Ф2, М-3-1, Р4, Л4", "М3, Ф1, М-1-1, Р4, Л4", "М3, Ф1, М-2-1, Р-1, Л3",
                     "М3, Ф1, М-2-1, Р3, Л3", "М3, Ф1, М-2-1, Р4, Л4", "М3, Ф1, М-3-1, Р1, Л2", "М3, Ф1, М-3-1, Р2, Л1",
                     "М3, Ф1, М-3-1, Р4, Л4", "М3, Ф4, М-1-1, Р4, Л4", "М3, Ф4, М-2-1, Р3, Л2", "М3, Ф4, М-2-1, Р4, Л4",
                     "М3, Ф4, М-3-1, Р1, Л2", "М3, Ф4, М-3-1, Р4, Л4", "М4, Ф1, М-4-1, Р2, Л1", "М4, Ф1, М-4-1, Р4, Л4",
                     "М4, Ф1, М-4-2, Р2, Л1", "М4, Ф1, М-4-2, Р4, Л4", "М4, Ф4, М-4-1, Р1, Л1", "М4, Ф4, М-4-1, Р2, Л1",
                     "М4, Ф4, М-4-1, Р3, Л1", "М4, Ф4, М-4-1, Р4, Л4", "М4, Ф4, М-4-2, Р1, Л1", "М4, Ф4, М-4-2, Р2, Л3",
                     "М4, Ф4, М-4-2, Р4, Л4"]

# all teachers of the MAI pre-University
TeachersCodifiers = []

########################################################################################################################

# EVERYTHING FOR GETTING DATA FROM NEWS SITES
# user agent for search engine
user_agent = {
    "User-Agent": "PUM-VKBot | Official bot for finding the schedule in the MAI pre-University: https://vk.com/pumvkbot"}

# weather search - paths
weather_source = "https://sinoptik.com.ru/погода-москва"
weather_search_tag, weather_tag_info = "div", {"class": "weather__article_description-text"}

# news search - paths
news_source = "https://ria.ru"
news_search_tag, news_tag_info = "a", {"class": "cell-list__item-link color-font-hover-only"}

# COVID-19 search - paths
covid_source = "https://ncov.blog/countries/ru/77/"
covid_search_tag, covid_tag_info = "p", {"class": "mt-0"}

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
