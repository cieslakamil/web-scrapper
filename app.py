from flask import Flask, render_template, url_for, request, redirect, send_file, jsonify
from livereload import Server
import pymongo
from pymongo import MongoClient
from product import Product
from data_conversion import dict_list_to_file




app = Flask(__name__)
app.config.update(
    TEMPLATES_AUTO_RELOAD=True,
    debug=True
)

client = MongoClient('mongodb://localhost:27017/')

db = client.ceneo_products_db

_products = db.products

products = {}


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
        if product_code:
            return redirect('/product/'+product_code)
        else:
            feedback = 'You haven\'t entered correct product code'
            return render_template('/extraction.html', feedback=feedback)

    return render_template('/extraction.html')


@app.route('/product/<product_code>')
def display_product(product_code):
    if product_code not in products.keys():
        products[product_code] = Product(product_code)
        product = products[product_code]
        if not _products.find_one({"code": product_code}):
            _products.insert_one(product.get_properties())
        print(_products.find_one({"code":"50534"})['name'])


    return render_template('/product.html', product=products[product_code])


@app.route('/product/<product_code>/download-opinions/<file_type>')
def download_opinions(product_code, file_type):
    if product_code not in products.keys():
        products[product_code] = Product(product_code)
    file_name = f'{product_code}.{file_type}'
    file_path = f'./opinions/{product_code}'
    dict_list_to_file(products[product_code].opinions,
                      file_path, file_name, file_type)
    try:
        return send_file(file_path+'/'+file_name, as_attachment=True, attachment_filename=file_name)
    except Exception as e:
        return str(e)


@app.route('/product/<product_code>/statistics')
def display_statistics_page(product_code):
    return render_template('/statistics.html', product_code=product_code)


@app.route('/product/<product_code>/get-statistics')
def get_score_stats(product_code):
    if product_code not in products.keys():
        products[product_code] = Product(product_code)
    prd = products[product_code]
    return jsonify([prd.score_stats, prd.recommendations])

"""

if __name__ == '__main__':
    server = Server(app.wsgi_app)
    server.serve()
"""


# old version, just runs the app
if __name__ == "__main__":
    app.run()


