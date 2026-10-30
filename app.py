from flask import Flask, render_template, request
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Initialize and migrate the SQLite database automatically
def init_db():
    conn = sqlite3.connect('purebites.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS reports 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  product TEXT, 
                  brand TEXT, 
                  company_address TEXT,
                  batch_no TEXT,
                  severity TEXT,
                  description TEXT,
                  created_at TEXT,
                  status TEXT DEFAULT 'Under Investigation')''')
    
    # Backwards-compatible schema migration
    c.execute("PRAGMA table_info(reports)")
    existing_cols = [col[1] for col in c.fetchall()]
    if 'company_address' not in existing_cols:
        c.execute("ALTER TABLE reports ADD COLUMN company_address TEXT DEFAULT 'Not Provided'")
    if 'batch_no' not in existing_cols:
        c.execute("ALTER TABLE reports ADD COLUMN batch_no TEXT DEFAULT 'N/A'")
    if 'severity' not in existing_cols:
        c.execute("ALTER TABLE reports ADD COLUMN severity TEXT DEFAULT 'Moderate'")
    if 'created_at' not in existing_cols:
        c.execute("ALTER TABLE reports ADD COLUMN created_at TEXT DEFAULT '2026-10-30 00:00:00'")
    if 'status' not in existing_cols:
        c.execute("ALTER TABLE reports ADD COLUMN status TEXT DEFAULT 'Under Investigation'")
        
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    conn = sqlite3.connect('purebites.db')
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM reports")
    count_row = c.fetchone()
    total_logged = count_row[0] if count_row else 0
    conn.close()
    return render_template('report.html', total_logged=total_logged)

@app.route('/submit', methods=['POST'])
def submit():
    product = request.form.get('product_name', '').strip()
    brand = request.form.get('brand', '').strip()
    company_address = request.form.get('company_address', 'Not Specified').strip() or 'Not Specified'
    batch_no = request.form.get('batch_no', 'N/A').strip() or 'N/A'
    severity = request.form.get('severity', 'Moderate').strip() or 'Moderate'
    description = request.form.get('description', '').strip()
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    conn = sqlite3.connect('purebites.db')
    c = conn.cursor()
    c.execute("""INSERT INTO reports 
                 (product, brand, company_address, batch_no, severity, description, created_at, status) 
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", 
              (product, brand, company_address, batch_no, severity, description, now_str, 'Under Investigation'))
    report_id = c.lastrowid
    conn.commit()
    conn.close()
    
    return render_template('success.html', 
                           report_id=report_id,
                           product=product, 
                           brand=brand, 
                           company_address=company_address,
                           batch_no=batch_no,
                           severity=severity)

# Enterprise Admin Operations Portal
@app.route('/admin')
def admin():
    conn = sqlite3.connect('purebites.db')
    c = conn.cursor()
    c.execute("""SELECT id, product, brand, company_address, batch_no, severity, description, created_at, status 
                 FROM reports ORDER BY id DESC""")
    reports = c.fetchall()
    
    total_reports = len(reports)
    critical_count = sum(1 for r in reports if r[5] and 'critical' in str(r[5]).lower())
    active_cases = sum(1 for r in reports if r[8] and 'investigation' in str(r[8]).lower())
    
    conn.close()
    return render_template('admin.html', 
                           reports=reports,
                           total_reports=total_reports,
                           critical_count=critical_count,
                           active_cases=active_cases)

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
