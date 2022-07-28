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

# Template -- have some data her (will move to 'chains.toml')
all_chains = ['avalanche', 'binance-smart-chain', 'polygon']
chain_meta = {
    'avalanche': {
        'name': "Avalanche",
        'description': "Avalanche is an open-source platform for launching decentralized finance applications and enterprise blockchain deployments in one interoperable, scalable ecosystem. Developers who build on Avalanche can create applications and custom blockchain networks with complex rulesets or build on existing private or public subnets.",
        'website': "https://www.avax.network/",
        'twitter': "https://twitter.com/avalancheavax",
        'github': "https://github.com/ava-labs"
    },
    'binance-smart-chain': {
        'name': "Binance Smart Chain",
        'description': "BNB Smart Chain (BSC) (Previously Binance Smart Chain) - EVM compatible, consensus layers, and with hubs to multi-chains.",
        'website': "https://www.binance.com/en",
        'twitter': "https://twitter.com/BNBChain",
        'github': "https://github.com/bnb-chain/bsc"
    },
    'polygon': {
        'name': "Polygon",
        'description': "Polygon is a platform design to support infrastructure development and help Ethereum scale. Its core component is a modular, flexible framework (Polygon SDK) that allows developers to build and connect Layer-2 infrastructures like Plasma, Optimistic Rollups, zkRollups, and Validium and standalone sidechains like the project's flagship product, Matic POS (Proof-of-Stake).",
        'website': "https://polygon.technology/",
        'twitter': "https://twitter.com/0xPolygon",
        'github': "https://github.com/maticnetwork/"
    }
}

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
    return render_template('index.html', chains=all_chains, descriptions=chain_meta)

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
    return render_template('chain.html', name=chain, repositories=repos[:20],
        metadata=chain_meta,
        chain=chain_data, tvl_nums=tvl_data, tvl_dates=date_data,
        tx_nums=tx_data, tx_dates=tx_date_data, acc_nums=acc_data,
        acc_dates=acc_date_data)