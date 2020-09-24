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

# data analysis
def analizing_sources_protection(sources_protection, user_id, limit_users_data):
    # output variables
    global new_sources_protection
    global source_for_user
    source_for_user = ""
    global columns_for_user
    columns_for_user = []
    # limit on the amount of user data stored in the array
    if len(sources_protection) >= limit_users_data * 3:
        new_sources_protection = []
        amount_extra_data = len(sources_protection) - (limit_users_data * 3)
        for quantity_transfers in range(limit_users_data * 3):
            new_sources_protection.append(sources_protection[amount_extra_data + quantity_transfers])
        sources_protection = new_sources_protection
    # search for data in an array
    for quantity_checks in range(len(sources_protection) // 3):
        if user_id == sources_protection[quantity_checks * 3]:
            source_for_user = f"{sources_protection[quantity_checks * 3 + 1]}"
            columns_for_user = sources_protection[quantity_checks * 3 + 2]
            new_sources_protection = []
            for quantity_transfers in range(len(sources_protection)):
                print(quantity_transfers)
                if (quantity_transfers != quantity_checks * 3) and (quantity_transfers != quantity_checks * 3 + 1) and (
                        quantity_transfers != quantity_checks * 3 + 2):
                    new_sources_protection.append(sources_protection[quantity_transfers])
            break

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
