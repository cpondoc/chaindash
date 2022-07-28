'''
Main endpoint for the TCV Blockchain Dashboard.
'''
from collections import defaultdict
from backend.data import *
from flask import Flask, render_template, send_from_directory
import os
import sqlite3
import toml

# Set up Flask app
app = Flask(__name__, instance_relative_config=True)
database = 'db/sample_data.db'

'''
Path for Favicon (currently TCV Logo)
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
Endpoint for Blockchain Tracker Dashboard
'''
@app.route('/')
def index():
    # Find data for chains and descriptions
    chains = []
    descriptions = defaultdict()

    # Read TOML file and grab data
    chain_data = toml.load("chains.toml")
    for chain in chain_data:
        chains.append(chain)
        descriptions[chain] = chain_data[chain]
    
    return render_template('index.html', chains=chains, descriptions=descriptions)

'''
Endpoint for visualizing data activity for each chain
'''
@app.route('/<chain>')
def chain_devs(chain):
    # Read TOML file and grab data
    chain_data = toml.load("chains.toml")
    metadata = chain_data[chain]

    # Developer Data (from SQL)
    conn = get_db_connection()
    repos = conn.execute("SELECT * FROM repositories WHERE chain = '" + str(chain) + "'").fetchall()
    chain_data = conn.execute("SELECT * FROM chains WHERE id ='" + str(chain) + "'").fetchall()
    conn.close()

    # TVL, Transaction, and Accounts data (from external sources)
    date_data, tvl_data = get_chain_tvl(chain.capitalize())
    tx_date_data, tx_data = get_daily_txs(chain, "Date(UTC)", "Value", metadata["transaction-source"])
    acc_date_data, acc_data = get_daily_accs(chain, "Date(UTC)", "Unique Address Total Count", metadata["accounts-source"])

    return render_template('chain.html', name=chain, repositories=repos[:20],
        metadata=metadata,
        chain=chain_data, tvl_nums=tvl_data, tvl_dates=date_data,
        tx_nums=tx_data, tx_dates=tx_date_data, acc_nums=acc_data,
        acc_dates=acc_date_data)