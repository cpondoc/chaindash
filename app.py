'''
Current front-end for TCV Blockchain Dashbaord
'''
import sqlite3
from flask import Flask, render_template
from backend.tvl import get_chain_tvl

# Set up Flask app
app = Flask(__name__)
database = 'db/sample_data.db'

'''
Make connection to SQL database
'''
def get_db_connection():
    conn = sqlite3.connect(database)
    conn.row_factory = sqlite3.Row
    return conn

'''
Starting endpoint (for right now, just point to developers)
'''
@app.route('/')
def index():
    conn = get_db_connection()
    chain_data = conn.execute('SELECT * FROM chains').fetchall()
    conn.close()
    return render_template('index.html', chains=chain_data)

'''
Endpoint for visualizing data activity for each chain
'''
@app.route('/<chain>')
def chain_devs(chain):
    conn = get_db_connection()
    repos = conn.execute("SELECT * FROM repositories WHERE chain = '" + str(chain) + "'").fetchall()
    chain_data = conn.execute("SELECT * FROM chains WHERE id ='" + str(chain) + "'").fetchall()
    date_data, tvl_data = get_chain_tvl(chain.capitalize())
    conn.close()
    return render_template('chain.html', repositories=repos[:20], chain=chain_data, tvl_nums=tvl_data, tvl_dates=date_data)