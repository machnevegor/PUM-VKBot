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

# databases settings
authors_comments = ["# Authors of the project:", "# 1-MachnevEgor_https://vk.com/machnev_egor",
                    "# 2-SchalimovDmitriy_https://vk.com/astronaut_without_spaceship",
                    "# 3-ArsenyKarimov_https://vk.com/id222338543", "# 4-MihailMarkov_https://vk.com/mixxxxail",
                    "# Contacts in email:", "# 1-meb.official.com@gmail.com", "# 2-dmitriy-shalimov@yandex.ru",
                    "# 3-arseny.karimov@gmail.com", "# 4-mihailmarkov2004@gmail.com"]
cell_separator = " | "


# standardizing the database if it is empty
def standardization_users_database(database_source):
    # opening the database
    data_memory = open(database_source, "r+", encoding="UTF-8")
    file_lines_array = list(data_memory.readlines())
    # standardization of the database, correction of failures
    if len(file_lines_array) < len(authors_comments):
        # sending data to the terminal
        print("!!! ERROR: Users database - BROKEN !!!")
        print("Solution: Return to the initial form")
        # clear file data
        data_memory.truncate(0)
        data_memory.seek(0)
        # recording a layout
        data_memory.write("\n".join(authors_comments))
    # closing the database
    data_memory.close()


# adding a user to a specific database
def adding_user_in_database(database_source, full_name, user_id, source_for_user, sheet_name, columns_for_user,
                            extra_cells, daily_schedule, telegram_alerts):
    # opening the database
    data_memory = open(database_source, "r+", encoding="UTF-8")
    file_lines_array = list(data_memory.readlines())
    # clear file data
    data_memory.truncate(0)
    data_memory.seek(0)
    # entering user data into the database and rewriting last data
    data_memory.write(
        "".join(file_lines_array) + "\n" + str(full_name) + cell_separator + str(user_id) + cell_separator + str(
            source_for_user) + cell_separator + str(sheet_name) + cell_separator + str(
            columns_for_user) + cell_separator + str(extra_cells) + cell_separator + str(
            daily_schedule) + cell_separator + str(telegram_alerts))
    # closing the database
    data_memory.close()
    print("".join(
        f"New user: {full_name} - {user_id} [{source_for_user}, {sheet_name}, {columns_for_user}, {extra_cells}] {daily_schedule}, {telegram_alerts}".split(
            "\n")))


# editing user data in a shared database
def editing_user_in_database(database_source, full_name, user_id, source_for_user, sheet_name, columns_for_user,
                             extra_cells, daily_schedule, telegram_alerts):
    # opening the database and moving all rows to a single array
    data_memory = open(database_source, "r+", encoding="UTF-8")
    file_lines_array = list(data_memory.readlines())
    data_memory.close()
    # creating an array with all user data
    all_users_data = []
    for user_data_line_number in range(len(file_lines_array) - len(authors_comments)):
        cells_array = list(file_lines_array[len(authors_comments) + user_data_line_number].split(cell_separator))
        all_users_data.append(cells_array)
    # search for the presence of a user in the database
    if len(all_users_data) == 0:
        # sending data to the terminal
        print("!!! ERROR: Users database is empty !!!")
    else:
        try:
            for user_data_cell in range(len(all_users_data)):
                # user found in the database
                if user_id == all_users_data[user_data_cell][1]:
                    # sending data to the terminal
                    print("".join(
                        f"Old data from the user: {all_users_data[user_data_cell][0]} - {all_users_data[user_data_cell][1]} [{all_users_data[user_data_cell][2]}, {all_users_data[user_data_cell][3]}, {all_users_data[user_data_cell][4]}, {all_users_data[user_data_cell][5]}] {all_users_data[user_data_cell][6]}, {all_users_data[user_data_cell][7]}".split(
                            "\n")))
                    # analysis for the presence of a line break at the end of a data line
                    end_of_the_data_line = True if len(all_users_data[user_data_cell][-1].split("\n")) >= 2 else False
                    # editing user data
                    all_users_data[user_data_cell][0] = str(full_name)
                    all_users_data[user_data_cell][1] = str(user_id)
                    all_users_data[user_data_cell][2] = str(source_for_user)
                    all_users_data[user_data_cell][3] = str(sheet_name)
                    all_users_data[user_data_cell][4] = str(columns_for_user)
                    all_users_data[user_data_cell][5] = str(extra_cells)
                    all_users_data[user_data_cell][6] = str(daily_schedule)
                    all_users_data[user_data_cell][7] = str(telegram_alerts)
                    # adding a line break to the end of the data line, if there was one
                    all_users_data[user_data_cell][-1] = str(all_users_data[user_data_cell][-1]) + str(
                        "\n" if end_of_the_data_line != False else "")
                    # creating a new database structure
                    for line_number in range(len(all_users_data)):
                        all_users_data[line_number] = str(cell_separator.join(all_users_data[line_number]))
                    # entering user data into the database and rewriting last data
                    data_memory = open(database_source, "r+", encoding="UTF-8")
                    data_memory.write("\n".join(authors_comments) + "\n" + "".join(all_users_data))
                    data_memory.close()
                    # sending data to the terminal
                    print("".join(
                        f"New data from the user: {full_name} - {user_id} [{source_for_user}, {sheet_name}, {columns_for_user}, {extra_cells}] {daily_schedule}, {telegram_alerts}".split(
                            "\n")))
                    # finish the work cycle because everything is done
                    break
        except Exception as E:
            # sending data to the terminal
            print("!!! ERROR: Users database - BROKEN !!!")
            print(f"Reason: {E}")


# opening a database and transferring data to an array
def searching_user_in_database(database_source, user_id):
    # standardization of data
    standardization_users_database(database_source=database_source)
    # opening the database and moving all rows to a single array
    data_memory = open(database_source, "r+", encoding="UTF-8")
    file_lines_array = list(data_memory.readlines())
    data_memory.close()
    # creating an array with all user data
    all_users_data = []
    for user_data_line_number in range(len(file_lines_array) - len(authors_comments)):
        cells_array = list(file_lines_array[len(authors_comments) + user_data_line_number].split(cell_separator))
        all_users_data.append(cells_array)
    # creating an output variable
    presence_user = []
    # search for the presence of a user in the database
    if len(all_users_data) == 0:
        # sending data to the terminal
        print("!!! ERROR: Users database is empty !!!")
    else:
        try:
            for user_data_cell in range(len(all_users_data)):
                # user found in the database
                if user_id == all_users_data[user_data_cell][1]:
                    # data record
                    presence_user.append(str(all_users_data[user_data_cell][0]))
                    presence_user.append(str(all_users_data[user_data_cell][1]))
                    presence_user.append(str(all_users_data[user_data_cell][2]))
                    presence_user.append(str(all_users_data[user_data_cell][3]))
                    # simple data type converter and data record
                    array_data = []
                    str_element = 0
                    while str_element != len(list(all_users_data[user_data_cell][4])):
                        if list(all_users_data[user_data_cell][4])[str_element] not in ["[", "'", ",", " ", "]"]:
                            array_cell = []
                            quantity_checks = str_element
                            while quantity_checks != len(list(all_users_data[user_data_cell][4])):
                                if list(all_users_data[user_data_cell][4])[quantity_checks] not in ["[", "'", ",", " ",
                                                                                                    "]"]:
                                    array_cell.append(list(all_users_data[user_data_cell][4])[quantity_checks])
                                else:
                                    array_data.append("".join(array_cell))
                                    str_element = quantity_checks
                                    # finish the work cycle because everything is done
                                    break
                                quantity_checks += 1
                        str_element += 1
                    presence_user.append(array_data)
                    # data record
                    presence_user.append(int(all_users_data[user_data_cell][5]))
                    presence_user.append(int(all_users_data[user_data_cell][6]))
                    presence_user.append(int(all_users_data[user_data_cell][7]))
                    # finish the work cycle because everything is done
                    break
        except Exception as E:
            # sending data to the terminal
            print("!!! ERROR: Users database - BROKEN !!!")
            print(f"Reason: {E}")
    # returning the final result
    return presence_user


# get a complete list of users from the database
def get_all_user_IDs_from_database(database_source):
    # standardization of data
    standardization_users_database(database_source=database_source)
    # opening the database and moving all rows to a single array
    data_memory = open(database_source, "r+", encoding="UTF-8")
    file_lines_array = list(data_memory.readlines())
    data_memory.close()
    # search, compile and return a complete list of all users
    user_IDs_list = []
    for user_data_line_number in range(len(file_lines_array) - len(authors_comments)):
        if file_lines_array[len(authors_comments) + user_data_line_number].split(cell_separator)[2] != "GUESTS":
            user_IDs_list.append(
                file_lines_array[len(authors_comments) + user_data_line_number].split(cell_separator)[1][2:])
    # returning the final result
    return user_IDs_list

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
