from product import Product
base_url = 'https://www.ceneo.pl/'
product_code = '90654635'
product = Product(product_code)
print(product.name)
print()
print(product.opinions_count)
print(product.positives_count)
print(product.negatives_count)
print(product.average_score)


