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

# import major modules
import requests as requests
from bs4 import BeautifulSoup as BeautifulSoup
import re as FormattingSpaces
from pycbrf import ExchangeRates as ExchangeRates
import datetime as datetime


# search for current weather
def weather_searcher(source, headers, search_tag, tag_info):
    # search for information in the source
    get_full_page = requests.get(source, headers)
    site_soup = BeautifulSoup(get_full_page.content, "html.parser")
    convert_site_soup = site_soup.findAll(search_tag, tag_info)
    # return of information result
    return f"🏮{convert_site_soup[0].text}" + f"\nПодробнее: {source}"


# search for the current currency exchange rate
def rates_searcher():
    # search for the current currency exchange rate
    rates = ExchangeRates(datetime.date.today(), locale_en=True)
    # return of information result
    return f"🗽Нынешний валютный курс:\n1$={round(float(rates['USD'].value), 2)}₽ & 1€={round(float(rates['EUR'].value), 2)}₽"


# search for news from news channels
def news_searcher(source, headers, search_tag, tag_info, quantity_news=3):
    # search for information in the source
    get_full_page = requests.get(source, headers)
    site_soup = BeautifulSoup(get_full_page.content, "html.parser")
    convert_site_soup = site_soup.findAll(search_tag, tag_info)
    # preparing a response
    find_information = []
    for content_tag in range(quantity_news):
        find_information.append(convert_site_soup[content_tag].text)
    # return of information result
    return "🌍Мировые новости на сегодня:\n📰" + "\n📰".join(find_information) + f"\nПодробнее: {source}"


# search for up-to-date information about the coronavirus
def covid_searcher(source, headers, search_tag, tag_info):
    # search for information in the source
    get_full_page = requests.get(source, headers)
    site_soup = BeautifulSoup(get_full_page.content, "html.parser")
    convert_site_soup = site_soup.findAll(search_tag, tag_info)
    # preparing a response
    site_text = []
    for letter_in_text in list(FormattingSpaces.sub(r"\s+", " ", f"🦠{convert_site_soup[0].text}")):
        site_text.append(letter_in_text)
        if letter_in_text in [".", "!", "?"]:
            break
    # return of information result
    return "".join(site_text) + f"\nПодробнее: {source}"

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
