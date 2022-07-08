'''
Current front-end for TCV Blockchain Dashbaord
'''
import sqlite3
from flask import Flask, render_template

# Set up Flask app
app = Flask(__name__)

'''
Make connection to SQL database
'''
def get_db_connection():
    conn = sqlite3.connect('data.db')
    conn.row_factory = sqlite3.Row
    return conn

'''
Starting endpoint (for right now, just point to developers)
'''
@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM chains').fetchall()
    print(posts)
    conn.close()
    return render_template('index.html', chains=posts)