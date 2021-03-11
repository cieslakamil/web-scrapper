import json
import csv
from dicttoxml import dicttoxml
import pandas
import xlsxwriter
# for creating a path if it does not exist

def dict_list_to_file(dict_list, file, file_extension):
    """ Write to chosen file format data from a list of dictionaries."""
    if file_extension == 'csv':
        dict_writer = csv.DictWriter(
            file, dict_list[0].keys(), lineterminator='\n')
        dict_writer.writeheader()
        dict_writer.writerows(dict_list)
    if file_extension == 'json':
        json.dump(dict_list, file, ensure_ascii=False)
    if file_extension == 'xlsx':
        data_frame = pandas.DataFrame(dict_list)
        xlsx_writer = pandas.ExcelWriter(file.name, engine='xlsxwriter')
        data_frame.to_excel(xlsx_writer, sheet_name='Sheet1')
        xlsx_writer.save()
    if file_extension == 'xml':
        file.write(str(dicttoxml(dict_list, attr_type=False), 'utf-8'))

    return file
