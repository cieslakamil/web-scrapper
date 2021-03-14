from flask import Flask, render_template, url_for, request, redirect, send_file, jsonify
from livereload import Server
import pymongo
from pymongo import MongoClient

from product import Product
from data_conversion import dict_list_to_file
import tempfile
import os
import random
import string
import threading
import time

app = Flask(__name__)
app.config.update(
    TEMPLATES_AUTO_RELOAD=True,
    debug=True
)
# MONGODB DATABASE
client = pymongo.MongoClient(
    "mongodb+srv://h6G9Ulz7bix5DdSC:h6G9Ulz7bix5DdSC@ceneop.zyvr9.mongodb.net/ceneop?retryWrites=true&w=majority")
# client = MongoClient('mongodb://localhost:27017/')
db = client.ceneo_products_db
product_list = db.products
opinions_file_deletion_delay = 7

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/extraction')
def extract():
    return render_template('extraction.html')


@app.route('/get-opinions', methods=['GET', 'POST'])
def get_opinions():
    if request.method == "POST":
        product_code = request.form['product_code']
        if product_code and product_code.isdecimal():
            if product_list.find_one({"code": product_code}):
                return redirect('/product/'+product_code)
            elif Product.has_opinions(product_code):
                product_list.insert_one(Product.dict(product_code))
                return redirect('/product/'+product_code)
            else:
                feedback = 'Produkt nie posiada opinii'
        else:
            feedback = 'Nieprawidłowy kod produktu.'
        return render_template('extraction.html', feedback=feedback)
    return render_template('extraction.html')


@ app.route('/product/<product_code>')
def display_product(product_code):
    product = product_list.find_one({"code": product_code})
    return render_template('product.html', product=product)


@ app.route('/product/<product_code>/download-opinions/<file_extension>')
def download_opinions(product_code, file_extension):

    file_name = f'{product_code}-opinie.{file_extension}'
    file_path = f'./opinions/{product_code}'
    opinions = Product.dict(product_code)['opinions']
    temp_file_name = ''.join(random.choices(
        string.ascii_letters + string.digits, k=16))
    with open(temp_file_name, 'w', encoding='utf-8') as file:
        dict_list_to_file(opinions, file, file_extension)

    with open(temp_file_name, 'rb') as file:
        try:
            threading.Thread(target=delete_file_after, args=[
                             temp_file_name, opinions_file_deletion_delay]).start()
            return send_file(file.name, as_attachment=True, attachment_filename=file_name)
        except Exception as e:
            return str(e)


def delete_file_after(file_name, seconds):
    time.sleep(seconds)
    os.remove(file_name)


@ app.route('/product/<product_code>/statistics')
def display_statistics_page(product_code):
    return render_template('statistics.html', product_code=product_code)


@ app.route('/product/<product_code>/get-statistics')
def get_score_stats(product_code):
    product = product_list.find_one({"code": product_code})
    return jsonify([product['score_stats'], product['recommendations']])


@ app.route('/product-list')
def display_product_list_page():
    return render_template('product_list.html', product_list=product_list.find())


@ app.route('/author')
def display_author_page():
    return render_template('author.html')


"""

if __name__ == '__main__':
    server = Server(app.wsgi_app)
    server.serve()
"""
# old version, just runs the app
if __name__ == "__main__":
    app.run()
