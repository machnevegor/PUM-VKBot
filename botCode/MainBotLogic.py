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

import vk_api
import random
import time
import json

token = '0ecle18741fd31e68fdd900a050g1bf5ee52b104f480e47297934c931eb81137689fe71a473f80e6a2345'

vk = vk_api.VkApi(token=token)

vk._auth_token()


def get_button(label, color, payload=''):
    return {
        "action": {
            'type': 'text',
            'payload': json.dumps(payload),
            'label': label

        },
        'color': color

    }


# Main menu
keyboard = {
    'one_time': False,
    'buttons': [
        [
            get_button(label='Погода', color='positive'),
            get_button(label='Уроки', color='primary')
        ]
    ]
}
keyboard1 = {
    'one_time': False,
    'buttons': [

        [get_button(label='Понедельник', color='positive'),
         get_button(label='Вторник', color='primary')],
        [get_button(label='Среда', color='primary'),
         get_button(label='Четверг', color='positive')],
        [get_button(label='Пятница', color='positive'),
         get_button(label='Суббота', color='primary')],
        [get_button(label='Назад', color='secondary')]

    ]
}
keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
keyboard = str(keyboard.decode('utf-8'))
keyboard1 = json.dumps(keyboard1, ensure_ascii=False).encode('utf-8')
keyboard1 = str(keyboard1.decode('utf-8'))
while True:
    owm = pyowm.OWM('5c1e4eb39849b5315ae8376ba2a8a44e')
    obs = owm.weather_manager().weather_at_place('Moscow')
    w = obs.weather
    temp = w.temperature('celsius')['temp']
    status = w.status

    try:

        messages = vk.method('messages.getConversations', {'offset': 0, 'count': 20, 'filter': 'unanswered'})
        if messages['count'] >= 1:
            id = messages['items'][0]['last_message']['from_id']
            body = messages['items'][0]['last_message']['text']

            if body.lower() == 'привет' or body.lower() == 'назад':
                vk.method('messages.send', {'peer_id': id, 'message': 'Дарова, епта, че надо', 'keyboard': keyboard,
                                            'random_id': random.randint(1, 231321321)})
            elif body.lower() == 'уроки':
                vk.method('messages.send', {'peer_id': id, 'message': 'ну выбирай, хуль', 'keyboard': keyboard1,
                                            'random_id': random.randint(1, 231321321)})
            elif body.lower() == 'понедельник':
                vk.method('messages.send', {'peer_id': id, 'sticker_id': 89, 'random_id': random.randint(1, 231321321)})
                vk.method('messages.send', {'peer_id': id, 'message': '''
				🌚\n1-2: Английский, каб303
				🌝\n3-4: Информатика, каб501
				🌚\n5-6: Геометрия, каб403
				🌝\n7-8: Физика, каб308 ''', 'random_id': random.randint(1, 231321321)})
            elif body.lower() == 'вторник':
                vk.method('messages.send', {'peer_id': id, 'message': 'У тебя все хорошо? Может к врачу сгоняешь?',
                                            'random_id': random.randint(1, 2312312321)})
            elif body.lower() == 'нет' or body.lower() == 'да' or 'схожу' in body.lower() or 'пойду' in body.lower():
                vk.method('messages.send',
                          {'peer_id': id, 'message': 'Ну вот и пиздуй', 'random_id': random.randint(1, 2312312321)})
            elif body.lower() == 'среда':
                vk.method('messages.send', {'peer_id': id, 'message': '''
				1-2: Литература, каб203
				🛠⚙🛠⚙🎵
				3: Химия, каб 208
				🆘u
				4-5: Алгебра, каб403
				ya 🆘y
				6-7: Геометрия, каб204
				🇺🇦🇺🇦❤🇷🇺🇷🇺
				8: ♿ Физра ♿
				''', 'random_id': random.randint(1, 2312312321)})
            elif body.lower() == 'четверг':
                vk.method('messages.send', {'peer_id': id, 'message': '''
				1: ♿Физра♿
				2: 🔞Английский🔞, каб203
				3-4:⚠Информатика⚠,\n каб501
				5: ♂ Окно ♂
				6: ❇Биология❇\n 	каб407
				7-8: ✅Алгебра✅\n 	каб403\n🅿❗🆘 for 🆓
				''', 'random_id': random.randint(1, 2312312321)})
            elif body.lower() == 'пятница':
                vk.method('messages.send', {'peer_id': id, 'message': '''
				1-2: 🤤CHILL🤤
				3-4: 🗿Русский язык🗿\n каб405
				5-6: 🆓История🆓\n каб204
			7:🤡Обществознание🤡\n каб204
				''', 'random_id': random.randint(1, 2312312321)})
            elif body.lower() == 'суббота':
                vk.method('messages.send',
                          {'peer_id': id, 'sticker_id': 163, 'random_id': random.randint(1, 2147483647)})
                vk.method('messages.send', {'peer_id': id, 'message': '''
				1. ♿Физра♿
				2. ♂ Окно ♂
				3. 📵ОБЖ📵\n каб 404
				4-5: ♂ Окно ♂
				6-7: 🌝Физика🌚\n каб308
				''', 'random_id': random.randint(1, 2147483647)})
            elif body.lower() == 'погода':
                vk.method('messages.send', {'peer_id': id,
                                            'message': 'Ну щас тут значт ♂' + str(status) + '♂, а также ' + str(
                                                round(temp)) + '°C', 'random_id': random.randint(1, 2147483647)})
            elif body.lower() == 'создатель':
                vk.method('messages.send', {'peer_id': id, 'message': '@id222338543 (♂хто я♂)',
                                            'random_id': random.randint(1, 2147483647)})
            elif body.lower() == 'звонки':
                vk.method('messages.send', {'peer_id': id, 'message': '''
				1. 9:00 - 9:45
				2. 9:50 - 10:35
				3. 10:45 - 11:30
				4. 11:50 - 12:35
				5. 12:45 - 13:30
				6. 13:40 - 14:25
				7. 14:45 - 15:30
				8. 15:40 - 16:25
				9. 16:30 - 17:15
				10. 17:20 - 18:05''', 'random_id': random.randint(1, 2147483647)})

            else:

                vk.method('messages.send',
                          {'peer_id': id, 'message': 'соси', 'random_id': random.randint(1, 2147483647)})



    except Exception as E:
        time.sleep(0.5)

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
