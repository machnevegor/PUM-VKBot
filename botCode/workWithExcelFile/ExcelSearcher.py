<<<<<<< HEAD
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

# import module
import openpyxl

# the path to the branching database
excel_database_source = "workWithExcelFile/excelDatabase"


# data search and processing
def selective_data_search(excel_source, columns, extra_cells, sheet_name, start_data, end_data):
    # output variables - declaration
    global output_day_schedule
    output_day_schedule = ["Расписание на заданный день:"]
    # sending data to the terminal
    print(f"Schedule source: {excel_source}/{sheet_name}.xlsx({columns}, {extra_cells}, [{start_data}, {end_data}])")
    # searcher logic
    try:
        # open excel file
        excel_document = openpyxl.load_workbook(f"{excel_database_source}/{excel_source}/{sheet_name}.xlsx")
        # days - import data from a graph and transfer it to a separate array
        days_data_array = []
        sheet = excel_document.get_sheet_by_name(sheet_name)
        for row in sheet[f"{columns[0]}1":f"{columns[0]}{sheet.max_row}"]:
            for cell in row:
                days_data_array.append(str(cell.value))
        # lessons - import data from a graph and transfer it to a separate array
        lessons_data_array = []
        sheet = excel_document.get_sheet_by_name(sheet_name)
        for row in sheet[f"{columns[1]}1":f"{columns[1]}{sheet.max_row}"]:
            for cell in row:
                lessons_data_array.append(str(cell.value))
        # cabinets - import data from a graph and transfer it to a separate array
        cabinets_data_array = []
        sheet = excel_document.get_sheet_by_name(sheet_name)
        for row in sheet[f"{columns[2]}1":f"{columns[2]}{sheet.max_row}"]:
            for cell in row:
                cabinets_data_array.append(str(cell.value))
        # search for relevant information
        lessons_output_data_array = []
        cabinets_output_data_array = []
        for quantity_checks in range(len(days_data_array)):
            if days_data_array[quantity_checks].lower() == start_data.lower():
                for quantity_recording_data in range(len(lessons_data_array) - quantity_checks - 1 - extra_cells):
                    if lessons_data_array[
                        quantity_recording_data + quantity_checks + 1 + extra_cells].lower() == end_data.lower():
                        break
                    # writing the necessary information to separate arrays
                    lessons_output_data_array.append(
                        (lessons_data_array[quantity_recording_data + quantity_checks + 1 + extra_cells]).title())
                    if cabinets_data_array[quantity_recording_data + quantity_checks + 1 + extra_cells] == "None":
                        cabinets_output_data_array.append("Узнавать у классного руководителя")
                    else:
                        try:
                            cabinets_output_data_array.append(int(float(cabinets_data_array[
                                                                            quantity_recording_data + quantity_checks + 1 + extra_cells])))
                        except Exception as E:
                            cabinets_output_data_array.append(cabinets_data_array[
                                                                  quantity_recording_data + quantity_checks + 1 + extra_cells].title())
        # the preparation of a reply
        for quantity_transfers in range(len(lessons_output_data_array)):
            output_day_schedule.append(
                f"{quantity_transfers + 1}. {lessons_output_data_array[quantity_transfers]}({cabinets_output_data_array[quantity_transfers]})")
        if output_day_schedule == ["Расписание на заданный день:"]:
            output_day_schedule = "Кажись в этот день технопарк🙃"
        else:
            output_day_schedule = "\n".join(output_day_schedule)
    except Exception as E:
        # sending data to the terminal
        print(f"!!! ERROR: Broken user data for excel searcher !!!")
        print(f"Reason: {E}")
        output_day_schedule = "Очень странно - ты есть в базе, но некоторые данные неправильные. Напиши в основную беседу, прикрепленную к сообществу - там тебе помогут решить данную проблему😬\nhttps://vk.me/join/FhSVyJp7fYT0fM805_KTHNWPctDNa79JGsI="

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
=======
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

# import module
import openpyxl

# the path to the branching database
excel_database_source = "workWithExcelFile/excelDatabase"


# data search and processing
def selective_data_search(excel_source, columns, extra_cells, sheet_name, start_data, end_data):
    # output variables - declaration
    global output_day_schedule
    output_day_schedule = ["Расписание на заданный день:"]
    # sending data to the terminal
    print(f"Schedule source: {excel_source}/{sheet_name}.xlsx({columns}, {extra_cells}, [{start_data}, {end_data}])")
    # searcher logic
    try:
        # open excel file
        excel_document = openpyxl.load_workbook(f"{excel_database_source}/{excel_source}/{sheet_name}.xlsx")
        # days - import data from a graph and transfer it to a separate array
        days_data_array = []
        sheet = excel_document.get_sheet_by_name(sheet_name)
        for row in sheet[f"{columns[0]}1":f"{columns[0]}{sheet.max_row}"]:
            for cell in row:
                days_data_array.append(str(cell.value))
        # lessons - import data from a graph and transfer it to a separate array
        lessons_data_array = []
        sheet = excel_document.get_sheet_by_name(sheet_name)
        for row in sheet[f"{columns[1]}1":f"{columns[1]}{sheet.max_row}"]:
            for cell in row:
                lessons_data_array.append(str(cell.value))
        # cabinets - import data from a graph and transfer it to a separate array
        cabinets_data_array = []
        sheet = excel_document.get_sheet_by_name(sheet_name)
        for row in sheet[f"{columns[2]}1":f"{columns[2]}{sheet.max_row}"]:
            for cell in row:
                cabinets_data_array.append(str(cell.value))
        # search for relevant information
        lessons_output_data_array = []
        cabinets_output_data_array = []
        for quantity_checks in range(len(days_data_array)):
            if days_data_array[quantity_checks].lower() == start_data.lower():
                for quantity_recording_data in range(len(lessons_data_array) - quantity_checks - 1 - extra_cells):
                    if lessons_data_array[
                        quantity_recording_data + quantity_checks + 1 + extra_cells].lower() == end_data.lower():
                        break
                    # writing the necessary information to separate arrays
                    lessons_output_data_array.append(
                        (lessons_data_array[quantity_recording_data + quantity_checks + 1 + extra_cells]).title())
                    if cabinets_data_array[quantity_recording_data + quantity_checks + 1 + extra_cells] == "None":
                        cabinets_output_data_array.append("Узнавать у классного руководителя")
                    else:
                        try:
                            cabinets_output_data_array.append(int(float(cabinets_data_array[
                                                                            quantity_recording_data + quantity_checks + 1 + extra_cells])))
                        except Exception as E:
                            cabinets_output_data_array.append(cabinets_data_array[
                                                                  quantity_recording_data + quantity_checks + 1 + extra_cells].title())
        # the preparation of a reply
        for quantity_transfers in range(len(lessons_output_data_array)):
            output_day_schedule.append(
                f"{quantity_transfers + 1}. {lessons_output_data_array[quantity_transfers]}({cabinets_output_data_array[quantity_transfers]})")
        if output_day_schedule == ["Расписание на заданный день:"]:
            output_day_schedule = "Кажись в этот день технопарк🙃"
        else:
            output_day_schedule = "\n".join(output_day_schedule)
    except Exception as E:
        # sending data to the terminal
        print(f"!!! ERROR: Broken user data for excel searcher !!!")
        print(f"Reason: {E}")
        output_day_schedule = "Очень странно - ты есть в базе, но некоторые данные неправильные. Напиши в основную беседу, прикрепленную к сообществу - там тебе помогут решить данную проблему😬\nhttps://vk.me/join/FhSVyJp7fYT0fM805_KTHNWPctDNa79JGsI="

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
>>>>>>> a65d00396a5536dfb6175678a3199ad6c362bbca
