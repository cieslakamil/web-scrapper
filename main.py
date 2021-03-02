

from product import Product
base_url = 'https://www.ceneo.pl/'
product_code = '95803673'

product = Product(product_code)
print(product.opinions[56]['positives'])
print(product.opinions[91]['negatives'])