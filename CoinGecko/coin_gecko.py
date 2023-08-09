# Operating System related imports
import os

# Date & Time related imports
import time
import datetime as dt
from dateutil import parser

# Pandas related imports
import pandas as pd
import json


# Coin Gecko related imports
import pycoingecko



coin_supply_path = "D:\Coding\VisualStudioCode\Projects\Python\CoinGeckoArbitrage\CoinStorage\coin_supply.csv"
coin_id_path = "D:\Coding\VisualStudioCode\Projects\Python\CoinGeckoArbitrage\CoinStorage\coin_id.csv"



class CoinGecko:
    def __init__(self, ticker_list: list) -> None:
        self.ticker_list = ticker_list
        self.cg = pycoingecko.CoinGeckoAPI()
        self.exchange_data = {}
        
    '''------------------------------------  Set & Get Operations  ------------------------------------'''
    def set_ticker_list(self, ticker_list: list = [], from_csv: bool = True):
        # If true, "self.ticker" will be set to the list of tickers recieved from the csv file. 
        if from_csv:
            self.ticker_list = self.get_tickers_from_csv()
        # If false, "self.ticker_list" will be set to the parameter variable "ticker_list"
        elif not from_csv:
            self.ticker_list = ticker_list

    '''------------------------------------'''
    def get_ticker_list(self, from_csv: bool = True) -> list:
        if self.ticker_list == []:
            self.set_ticker_list(from_csv)

        return self.ticker_list
    '''------------------------------------'''
    '''------------------------------------  Thread Operations  ------------------------------------'''
    '''------------------------------------'''
    '''------------------------------------'''
    '''------------------------------------'''
    '''------------------------------------  Single Ticker Operations  ------------------------------------'''

 
    '''------------------------------------'''
    '''------------------------------------'''
    '''------------------------------------'''
    
    '''------------------------------------'''
    def get_tickers_from_csv(self) -> list:
        df = pd.read_csv(coin_id_path)
        return df["symbol"].to_list()
    '''------------------------------------'''
    def get_ticker_id(self, ticker: str) -> str:
        symbol = ticker.lower()
        try:
            coin_ids_data = pd.read_csv(coin_id_path)
        # If the file is not found, write new data to it. 
        except FileNotFoundError as e:
            self.write_coin_ids_to_csv()
            coin_ids_data = pd.read_csv(coin_id_path)


        # Get the current date
        cur_date = dt.datetime.now().date()

        last_update = coin_ids_data["last_update"].iloc[0]
        out_of_date = self.if_ID_out_of_date(cur_date=cur_date, last_date=last_update, days_allowed=30)

        if out_of_date:
            self.write_coin_IDs_to_csv()
        else:
            row = coin_ids_data.loc[coin_ids_data["symbol"].str.lower() == symbol]

            # If the ticker is found.
            if not row.empty:
                return row.iloc[0]["id"]
            # Coin ID not found. 
            else:
                return None
    '''------------------------------------'''
    def get_current_exchanges(self, ticker):
        # Dictionary to hold the exchange name with the last trading price on the platfrom.
        exchange_data = {}
        
        # Get the current timestamp
        cur_timestamp = dt.datetime.now()

        # Get the coin data.
        coin_data = self.cg.get_coin_by_id(self.get_ticker_id(ticker))
        exchanges = coin_data.get("tickers")
        exchange_names = [exchange["market"]["name"] for exchange in exchanges]

        index = 0
        exchange_data = []
        for exchange in exchanges:

            exchange_name = exchange_names[index]
            # Get the last price and format it to have the to include coins with many numerals after the decimal point.
            price = exchange["last"]
            price = "{:.10f}".format(float(price))

            # Volume 
            volume = exchange["volume"]
            # Last converted
            last_convert = exchange["converted_last"]
            # Last trade 
            last_trade_time = exchange["last_traded_at"]
            last_trade_time = self.convert_iso_to_local(last_trade_time)
            # Boolean to check if the price is an anomoly.
            is_anomoly = exchange["is_anomaly"]
            # Boolean to check if the price is stale.
            is_stale = exchange["is_stale"]
            # Get the time of the last data fetch.
            last_fetch = exchange["last_fetch_at"]
            last_fetch = self.convert_iso_to_local(last_fetch)
            # Get the token url.
            token_url = exchange["token_info_url"]
            trade_url = exchange["trade_url"]

            # Spread of the exchange
            exchange_spread = exchange["bid_ask_spread_percentage"]
            # Trust score. Green = Good, Yellow = Uncertain, Red = Bad
            trust_score = exchange["trust_score"]
            time_difference = self.calculate_date_difference(cur_date=cur_timestamp, last_date=last_trade_time)


            data = {
                "exchange_name": exchange_name,
                "last_time": last_trade_time,
                "last_price": price,
                "spread": exchange_spread,
                "volume": volume,
                "is_anomaly": is_anomoly,
                "is_stale": is_stale,
                "trust_score": trust_score,
                "token_url": token_url,
                "trade_url": trade_url,
                "last_updated": time_difference }
            
            exchange_data.append(data)

            index += 1
        
        
        return exchange_data




    '''------------------------------------  CSV Operations  ------------------------------------'''
    '''------------------------------------'''
    def write_coin_supply_data(self, ticker: str):
        
        coin_id = self.get_id_by_ticker(ticker)
        csv_df = pd.read_csv(coin_supply_path)

        # Get the ticker by the ID
        coin_data = self.cg.get_coin_by_id(coin_id) 
        cur_date = dt.datetime.now().date()
        supply_data = {
        "ticker": ticker,
        "circulating_supply": coin_data["market_data"]["circulating_supply"],
        "total_supply": coin_data["market_data"]["total_supply"],
        "max_supply": coin_data["market_data"]["max_supply"],
        "last_updated": cur_date
        }
        # Create a dataframe from the dictionary of supply data. 
        df = pd.DataFrame(supply_data, index=[0])

        # Check if the file exists and if it's empty, then write the header
        if not os.path.isfile(coin_supply_path) or os.path.getsize(coin_supply_path) == 0:
            df.to_csv(coin_supply_path, mode="w", header=True, index=False)
        # If it's not empty, do not write the header. This removes duplicates. 
        else:
            df.to_csv(coin_supply_path, mode="a", header=False, index=False)
    '''------------------------------------'''
    def write_coin_IDs_to_csv(self):
        # Get the list of coins provided by coingecko.
        coin_list = self.cg.get_coins_list()
        # Convert to dataframe. 
        df = pd.DataFrame(coin_list)
        # Get the timestamp to keep track of when it was last updated. 
        cur_timestamp = dt.datetime.now().date()
        df["last_update"] = cur_timestamp
        df.to_csv(coin_id_path)


    '''------------------------------------  Date & Time Operations  ------------------------------------'''
    '''------------------------------------'''
    def if_ID_out_of_date(self, cur_date, last_date, days_allowed: int = 30) -> bool:

        try:
            time_difference = cur_date - last_date
        except TypeError:
            last_date = dt.datetime.strptime(last_date, "%Y-%m-%d").date()
            time_difference = cur_date - last_date
        time_difference =  time_difference.days

        if time_difference > days_allowed:
            return True
        elif time_difference < days_allowed:
            return False
    '''------------------------------------'''
    def convert_iso_to_local(self, iso_timestamp):
        parsed_timestamp = parser.isoparse(iso_timestamp)

        # Convert to local time. 
        local_time = parsed_timestamp.astimezone()
        # Example Timestamp: 2023-08-09 05:31:40-07:00
        # Split the timestamp on the space. 
        _date, _time = str(local_time).split(" ")
        # Split the time by "-". Like so 05:31:40-07:00 -> [05:31:40],[07:00]
        _time = _time.split("-")[0]
        # By the end of this function the iso_timestamp should be converted to local time. 
        # Then the local time is foramtted accordingly.
        # Ex: 2023-08-09 05:31:40-07:00 -> 2023-08-09 05:31:40
        local_time = f"{_date} {_time}"
        return local_time
    '''------------------------------------'''
    def calculate_date_difference(self, cur_date, last_date):

        cur_date_str = str(cur_date).split(".")[0]
        last_date_date, last_date_time = str(last_date).split(" ")
        last_date_time = last_date_time.split("-")[0]

        last_date_str = f"{last_date_date} {last_date_time}"

        cur_date = dt.datetime.strptime(cur_date_str, "%Y-%m-%d %H:%M:%S")
        last_date = dt.datetime.strptime(last_date_str, "%Y-%m-%d %H:%M:%S")
        
        time_difference = cur_date - last_date
        return time_difference
