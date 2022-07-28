'''
Current front-end for TCV Blockchain Dashbaord
'''
from backend.tvl import get_chain_tvl
from backend.transactions import get_daily_txs
from backend.accounts import get_daily_accs
from flask import Flask, render_template, send_from_directory
import os
import sqlite3

# Set up Flask app
app = Flask(__name__, instance_relative_config=True)
database = 'db/sample_data.db'

'''
Adding favicon
'''
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

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
    all_chains = ['avalanche', 'binance-smart-chain', 'polygon']
    return render_template('index.html', chains=all_chains)

'''
Endpoint for visualizing data activity for each chain
'''
@app.route('/<chain>')
def chain_devs(chain):
    print(chain)
    conn = get_db_connection()

    # Developer Data
    repos = conn.execute("SELECT * FROM repositories WHERE chain = '" + str(chain) + "'").fetchall()
    chain_data = conn.execute("SELECT * FROM chains WHERE id ='" + str(chain) + "'").fetchall()

    # TVL Data
    date_data, tvl_data = get_chain_tvl(chain.capitalize())

    # Transaction Data
    tx_date_data, tx_data = get_daily_txs(chain, "Date(UTC)", "Value")

    # Account Data
    acc_date_data, acc_data = get_daily_accs(chain, "Date(UTC)", "Unique Address Total Count")

    conn.close()
    return render_template('chain.html', repositories=repos[:15], 
        chain=chain_data, tvl_nums=tvl_data, tvl_dates=date_data,
        tx_nums=tx_data, tx_dates=tx_date_data, acc_nums=acc_data,
        acc_dates=acc_date_data)