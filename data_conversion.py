import json
import csv
from dicttoxml import dicttoxml
import pandas
import xlsxwriter
# for creating a path if it does not exist
import os


def dict_list_to_file(dict_list, file_path, file_name, file_format):
    """ Write to chosen file format data from a list of dictionaries."""
    os.makedirs(file_path, exist_ok=True)
    if file_format == 'csv':
        with open(file_path+'/'+file_name, 'w', encoding='utf-8', newline='') as file:
            dict_writer = csv.DictWriter(file, dict_list[0].keys())
            dict_writer.writeheader()
            dict_writer.writerows(dict_list)
    if file_format == 'json':
        with open(file_path+'/'+file_name, 'w', encoding='utf-8') as file:
            json.dump(dict_list, file, ensure_ascii=False)
    if file_format == 'xlsx':
        data_frame = pandas.DataFrame(dict_list)
        xlsx_writer = pandas.ExcelWriter(
            file_path+'/'+file_name, engine='xlsxwriter')
        data_frame.to_excel(xlsx_writer, sheet_name='Sheet1')
        xlsx_writer.save()

    if file_format == 'xml':
        with open(file_path+'/'+file_name, 'w', encoding='utf-8') as file:
            file.write(str(dicttoxml(dict_list, attr_type=False), 'utf-8'))
