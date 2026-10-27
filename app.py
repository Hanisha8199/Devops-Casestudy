from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('report.html')

@app.route('/submit', methods=['POST'])
def submit():
    product = request.form.get('product_name')
    brand = request.form.get('brand')
    return render_template('success.html', product=product, brand=brand)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)