import json
import csv
from dicttoxml import dicttoxml


def dict_list_to_json(dict_list, file_name):
    """ Write to a json file from a list of dictionaries."""
    with open(file_name, 'w', encoding='utf-8') as file:
        json.dump(dict_list, file, ensure_ascii=False)

def dict_list_to_csv(dict_list, file_name):
    """ Write to a csv file from a list of dictionaries."""
    with open(file_name, 'w', encoding='utf-8', newline='') as file:
        dict_writer = csv.DictWriter(file, dict_list[0].keys())
        dict_writer.writeheader()
        dict_writer.writerows(dict_list)

def dict_list_to_xml(dict_list, file_name):
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(str(dicttoxml(dict_list, attr_type=False), 'utf-8'))

