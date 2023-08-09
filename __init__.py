

# Import arbitrage finder. 
from CoinGecko.arbitrage_finder import ArbitrageFinder




import json




def test1(arb: ArbitrageFinder, ticker_list: list):
    for t in ticker_list:
        data = arb.get_current_exchanges(t)
        print(f"{data}")
def test2(arb: ArbitrageFinder, ticker_list: list):

    arb.set_ticker_list(ticker_list)
    arb.scan_exchanges_threads()




if __name__ == "__main__":
    arb = ArbitrageFinder()
    tickers = arb.get_tickers_from_csv()
    tickers = tickers[:10]
    #test1(arb, tickers)
    #test2(arb, tickers)
    


"""    # Format the exchange data to remove any coins that only trade on one exchange. 
    filtered_exchanges = {coin: data for coin, data in exchanges.items() if data is not None and len(data) > 1}
    filtered_exchanges = json.dumps(filtered_exchanges, indent=4)
    #print(f"Exchanges: {filtered_exchanges}")"""






