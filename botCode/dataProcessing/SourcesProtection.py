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

# data analysis
def analizing_sources_protection(sources_protection, user_id, limit_users_data):
    # output variables
    global new_sources_protection
    global source_for_user
    source_for_user = ""
    global columns_for_user
    columns_for_user = []
    global extra_cells
    extra_cells = 1
    global sheet_name
    sheet_name = ""
    # limit on the amount of user data stored in the array
    if len(sources_protection) >= limit_users_data:
        new_sources_protection = []
        amount_extra_data = len(sources_protection) - (limit_users_data)
        for quantity_transfers in range(limit_users_data):
            new_sources_protection.append(sources_protection[amount_extra_data + quantity_transfers])
        sources_protection = new_sources_protection
    # search for data in an array
    for quantity_checks in range(len(sources_protection)):
        if user_id == sources_protection[quantity_checks][0]:
            source_for_user = f"{sources_protection[quantity_checks][1]}"
            columns_for_user = sources_protection[quantity_checks][2]
            extra_cells = sources_protection[quantity_checks][3]
            sheet_name = sources_protection[quantity_checks][4]
            new_sources_protection = []
            for quantity_transfers in range(len(sources_protection)):
                if (quantity_transfers != quantity_checks):
                    new_sources_protection.append(sources_protection[quantity_transfers])
            break
    # sending data to the terminal
    print(f"Sources protection: {new_sources_protection}")

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