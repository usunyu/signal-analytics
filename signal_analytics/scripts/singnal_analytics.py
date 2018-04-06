# - *- coding: utf- 8 - *-
import sys, requests, json, time
from datetime import datetime

API_KEY = "QIRES25C6HSDVSRP"
SMA_REQUEST = "https://www.alphavantage.co/query?function=SMA&apikey={}&symbol={}&interval=daily&time_period={}&series_type=close"
# ftp://ftp.nasdaqtrader.com/SymbolDirectory/nasdaqlisted.txt
NASDAQ_SYMBOL_FILE = "nasdaqlisted.txt"

class Stock(object):
    symbol = ""
    company = ""

    def __init__(self, symbol, company):
        self.symbol = symbol
        self.company = company

class SMA(object):
    time = ""
    value = 0

    def __init__(self, time, value):
        self.time = time
        self.value = value

def print_log(msg):
    print("[" + str(datetime.now()) + "]", msg)

def get_sma_data(symbol, period, days):
    api_request = SMA_REQUEST.format(API_KEY, symbol, period)
    response = requests.get(api_request)
    json_response = json.loads(response.text)
    sma_data = []
    day = 0
    # print(response.text)
    for time, sma_obj in json_response["Technical Analysis: SMA"].items():
        if day >= days:
            break
        sma_data.append(SMA(time, float(sma_obj["SMA"])))
        day += 1
    return sma_data

def main():
    print_log("Signal analytics started...")
    # get all stock symbols
    stocks = []
    with open(NASDAQ_SYMBOL_FILE) as file:
        for line in file:
            parts = line.split('|')
            if len(parts) < 2 or "File Creation Time" in line or "Symbol" in line:
                continue
            stocks.append(Stock(parts[0], parts[1]))
    # analytics for golden cross & silver cross
    CAL_DAYS = 30
    golden_cross_stocks = []
    silver_cross_stocks = []
    error_stocks = []
    for index in range(0, len(stocks)):
        try:
            stock = stocks[index]
            print_log("Processing stock " + stock.symbol + "...")
            # get sma data
            time.sleep(1)
            sma_15 = get_sma_data(stock.symbol, 15, CAL_DAYS)
            time.sleep(1)
            sma_50 = get_sma_data(stock.symbol, 50, CAL_DAYS)
            time.sleep(1)
            sma_200 = get_sma_data(stock.symbol, 200, CAL_DAYS)
            if len(sma_200) == 0 or len(sma_50) == 0 or len(sma_15) == 0:
                continue
            # check if we have cross
            if sma_15[0].value > sma_200[0].value and sma_15[len(sma_15) - 1].value < sma_200[len(sma_15) - 1].value:
                # find golden cross
                golden_cross_stocks.append(stock)
                print_log("Found golden cross:)")
            if sma_50[0].value > sma_200[0].value and sma_50[len(sma_15) - 1].value < sma_200[len(sma_15) - 1].value:
                # find silver cross
                silver_cross_stocks.append(stock)
                print_log("Found silver cross:)")
            print_log("Progress: " + str(index + 1) + "/" + str(len(stocks)))
            # sys.stdout.write("Progress: " + str(index + 1) + "/" + str(len(stocks)) + "\r")
            # sys.stdout.flush()
        except:
            stock = stocks[index]
            error_stocks.append(stock)
            print_log("Error process stock " + stock.symbol + "!!")
    print_log("Signal analytics success!")
    print_log("Error stocks:")
    for stock in error_stocks:
        print(stock.symbol, stock.company)
    print_log("Silver cross stocks(50 cross 200):")
    for stock in silver_cross_stocks:
        print(stock.symbol, stock.company)
    print_log("Golden cross stocks(15 cross 200):")
    for stock in golden_cross_stocks:
        print(stock.symbol, stock.company)

if __name__ == '__main__':
    main()