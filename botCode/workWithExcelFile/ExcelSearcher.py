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

# set main sheet name
sheet_name = "Лист1"


# data search and processing
def selective_data_search(excel_source, columns, extra_cells, start_data, end_data):
    # output variables - declaration
    global output_day_schedule
    output_day_schedule = ["Расписание на день:"]
    if (excel_source == "") or (columns == []):
        # sending data to the terminal
        print(f"!!!ERROR: The source is not specified!!!")
        output_day_schedule = "Расписание не найдено - попробуй заново😳"
    else:
        # sending data to the terminal
        print(f"Schedule source: {excel_source}({columns}, {extra_cells}, {start_data}, {end_data})")
        # open excel file
        excel_document = openpyxl.load_workbook(excel_source)
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
                        lessons_data_array[quantity_recording_data + quantity_checks + 1 + extra_cells])
                    if cabinets_data_array[quantity_recording_data + quantity_checks + 1 + extra_cells] == "None":
                        cabinets_output_data_array.append("Узнавать у классного руководителя")
                    else:
                        cabinets_output_data_array.append(
                            cabinets_data_array[quantity_recording_data + quantity_checks + 1 + extra_cells])
        # the preparation of a reply
        for quantity_transfers in range(len(lessons_output_data_array)):
            output_day_schedule.append(
                f"{quantity_transfers + 1}. {lessons_output_data_array[quantity_transfers]}({cabinets_output_data_array[quantity_transfers]})")
        if output_day_schedule == ["Расписание на день:"]:
            output_day_schedule = "Кажись в этот день технпарк🙃"
        else:
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
