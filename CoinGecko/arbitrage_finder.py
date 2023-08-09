# Time & Date related imports
import time

# Custom CoinGecko Parent class import.
from CoinGecko.coin_gecko import CoinGecko

# Asnchronous related imports
import concurrent.futures



class ArbitrageFinder(CoinGecko):
    def __init__(self, ticker_list: list = []) -> None:
        super().__init__(ticker_list)
    '''------------------------------------'''
    def scan_exchanges_threads(self):
        start = time.time()
        # Use multi-threading to access external api calls. 
        with concurrent.futures.ThreadPoolExecutor() as thread_executor:
            thread_results = thread_executor.map(self.get_current_exchanges, self.ticker_list)

            print(f"Thread: {thread_results}") 

            for t in thread_results:

                print(f"T: {t}")
        end = time.time()

        elaspe = end - start

    '''------------------------------------'''
    '''------------------------------------'''
    '''------------------------------------'''
    '''------------------------------------'''
    '''------------------------------------'''
    '''------------------------------------'''