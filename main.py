from product import Product
from data_conversion import dict_list_to_json, dict_list_to_csv, dict_list_to_xml
base_url = 'https://www.ceneo.pl/'
product_code = '90654635'
product = Product(product_code)
print(product.name)
print()
print(product.opinions_count)
print(product.positives_count)
print(product.negatives_count)
print(product.average_score)
dict_list_to_json(product.opinions, 'opinions.json')
dict_list_to_csv(product.opinions, 'opinions.csv')
dict_list_to_xml(product.opinions, 'opinions.xml')



