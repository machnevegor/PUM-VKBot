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

# import module
import openpyxl


# data search and processing
def selective_data_search(excel_source, columns, start_data, end_data):
    # output variables - declaration
    global output_day_schedule
    output_day_schedule = ["Расписание на день:"]
    # open excel file
    excel_document = openpyxl.load_workbook(excel_source)
    # lessons - import data from a graph and transfer it to a separate array
    lessons_data_array = []
    sheet = excel_document.get_sheet_by_name("Лист1")
    for row in sheet[f"{columns[0]}1":f"{columns[0]}{sheet.max_row}"]:
        for cell in row:
            lessons_data_array.append(str(cell.value))
    # cabinets - import data from a graph and transfer it to a separate array
    cabinets_data_array = []
    sheet = excel_document.get_sheet_by_name("Лист1")
    for row in sheet[f"{columns[1]}1":f"{columns[1]}{sheet.max_row}"]:
        for cell in row:
            cabinets_data_array.append(str(cell.value))
    # search for relevant information
    lessons_output_data_array = []
    cabinets_output_data_array = []
    for quantity_checks in range(len(lessons_data_array)):
        if lessons_data_array[quantity_checks].lower() == start_data.lower():
            for quantity_recording_data in range(len(lessons_data_array) - quantity_checks - 1):
                if lessons_data_array[quantity_recording_data + quantity_checks + 1].lower() == end_data.lower():
                    break
                # writing the necessary information to separate arrays
                lessons_output_data_array.append(lessons_data_array[quantity_recording_data + quantity_checks + 1])
                cabinets_output_data_array.append(cabinets_data_array[quantity_recording_data + quantity_checks + 1])
    # the preparation of a reply
    for quantity_transfers in range(len(lessons_output_data_array)):
        output_day_schedule.append(
            f"{lessons_output_data_array[quantity_transfers]}({cabinets_output_data_array[quantity_transfers]})")
    output_day_schedule = "\n".join(output_day_schedule)

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
