import pandas as pd

'''
Function to get TVL data from existing CSV.
To-Do: Put data into SQL database, and add new data every day.
'''
def get_chain_tvl(chain_name):
    # Special exception for BSC
    if (chain_name == "Binance-smart-chain"):
        chain_name = "BSC"

    # Grab all data
    data = pd.read_csv('db/chains.csv')

    # Extract TVL data
    all_data = data[chain_name].values.tolist()
    final_data = [x for x in all_data if pd.isnull(x) == False]

    # Extract Date data
    dates = data['Date'].values.tolist()
    date_data = dates[len(all_data) - len(final_data):]
    return date_data, final_data