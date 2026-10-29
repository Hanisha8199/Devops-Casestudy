from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# Initialize the database automatically
def init_db():
    conn = sqlite3.connect('purebites.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS reports 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  product TEXT, 
                  brand TEXT, 
                  description TEXT)''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return render_template('report.html')

@app.route('/submit', methods=['POST'])
def submit():
    product = request.form.get('product_name')
    brand = request.form.get('brand')
    description = request.form.get('description')
    
    # Save the report to the database
    conn = sqlite3.connect('purebites.db')
    c = conn.cursor()
    c.execute("INSERT INTO reports (product, brand, description) VALUES (?, ?, ?)", 
              (product, brand, description))
    conn.commit()
    conn.close()
    
    return render_template('success.html', product=product, brand=brand)

# Secret route to view the database
@app.route('/admin')
def admin():
    conn = sqlite3.connect('purebites.db')
    c = conn.cursor()
    c.execute("SELECT * FROM reports")
    reports = c.fetchall()
    conn.close()
    return render_template('admin.html', reports=reports)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)