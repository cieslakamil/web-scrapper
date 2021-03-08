from flask import Flask, render_template, url_for, request, redirect, send_file
from product import Product
from data_conversion import dict_list_to_json, dict_list_to_csv, dict_list_to_xml


app = Flask(__name__)


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
    product = Product(product_code)
    # dict_list_to_json(product.opinions, 'opinions.json')
    # dict_list_to_csv(product.opinions, 'opinions.csv')
    # dict_list_to_xml(product.opinions, 'opinions.xml')
    return render_template('/product.html', product=product)


@app.route('/download-opinions/<file_name>')
def download_opinions(file_name):
    try:
        return send_file(file_name, attachment_filename=file_name)
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    app.run()
