from flask import Flask, render_template, url_for, request, redirect, send_file, jsonify
from livereload import Server
import pymongo
from pymongo import MongoClient

from product import Product
from data_conversion import dict_list_to_file
import tempfile

import json
import csv
from dicttoxml import dicttoxml
import pandas
import xlsxwriter
# for creating a path if it does not exist
import os

app = Flask(__name__)
app.config.update(
    TEMPLATES_AUTO_RELOAD=True,
    debug=True
)
# MONGODB DATABASE

client = pymongo.MongoClient("mongodb+srv://h6G9Ulz7bix5DdSC:h6G9Ulz7bix5DdSC@ceneop.zyvr9.mongodb.net/ceneop?retryWrites=true&w=majority")
#client = MongoClient('mongodb://localhost:27017/')
db = client.ceneo_products_db
products = db.products
print(f'DATABASE: {products}')

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
            return redirect('/product/'+product_code)
        else:
            feedback = 'Nieprawidłowy kod produktu.'
            return render_template('extraction.html', feedback=feedback)
    return render_template('extraction.html')


@app.route('/product/<product_code>')
def display_product(product_code):
    product = products.find_one({"code": product_code})
    if not product:
        product = Product(product_code)
        products.insert_one(product.get_properties())
    return render_template('product.html', product=product)


@app.route('/product/<product_code>/download-opinions/<file_extension>')
def download_opinions(product_code, file_extension):
    file_name = f'{product_code}-opinie.{file_extension}'
    file_path = f'./opinions/{product_code}'
    opinions = products.find_one({'code': product_code})['opinions']
    dict_list = opinions
    with tempfile.NamedTemporaryFile('w', encoding='utf-8', delete=False) as file:
        dict_list_to_file(opinions, file, file_extension)
        try:
            return send_file(file.name, as_attachment=True, attachment_filename=file_name)
        except Exception as e:
            return str(e)


@app.route('/product/<product_code>/statistics')
def display_statistics_page(product_code):
    return render_template('statistics.html', product_code=product_code)


@app.route('/product/<product_code>/get-statistics')
def get_score_stats(product_code):
    product = products.find_one({"code": product_code})
    return jsonify([product['score_stats'], product['recommendations']])

@app.route('/product-list')
def display_product_list_page():
    return render_template('product_list.html', products=products.find())

@app.route('/author')
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