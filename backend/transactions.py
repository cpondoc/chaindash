import pandas as pd
import requests

# TO-DO: Export into .yaml file and export all the information
tx_sources = {'avalanche' : "https://snowtrace.io/chart/tx?output=csv"}

'''
Once again, proof of concept, but: grabbing data from other sources.
Goal: once again, probably just replace all the data?
'''
def get_daily_txs(chain_name, date_param, value_param):
    url = tx_sources[chain_name]
    response = requests.get(url)
    open("db/" + str(chain_name) + "/transaction_data.csv", "wb").write(response.content)
    
    # Grab all data
    data = pd.read_csv("db/" + str(chain_name) + "/transaction_data.csv")

    # Extract TVL and date data
    final_data = data[value_param].values.tolist()
    date_data = data[date_param].values.tolist()

    return date_data, final_data

#date_data, final_data = get_daily_txs("avalanche", "Date(UTC)", "Value")
#print(date_data, final_data)