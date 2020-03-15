import ccxt
import sys

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

if len(sys.argv) > 2:
    ids = list(sys.argv[1:])
    exchanges = {}
    print("Exchanges selected: ", ids)
    string = bcolors.BOLD + ' {:<15} | '.format("Exchanges")
    for id in ids:
        exchange = getattr(ccxt, id)()
        exchanges[id] = exchange
        markets = exchange.load_markets()
        string += bcolors.BOLD + ' {:<15} | '.format(exchanges[id].name)
        string += bcolors.BOLD + ' {:<15} | '.format(exchanges[id].name)

    allSymbols = [symbol for id in ids for symbol in exchanges[id].symbols]
    uniqueSymbols = list(set(allSymbols))
    arbitrableSymbols = sorted(
        [symbol for symbol in uniqueSymbols if allSymbols.count(symbol) > 1])

    table = []

    print(string)

    sym = ""

    try:
        for sym in arbitrableSymbols:
            string = bcolors.HEADER + ' {:<15} | '.format(sym)
            for id in ids:
                if sym in exchanges[id].symbols:
                    orderbook = exchanges[id].fetch_order_book(sym)
                    if (len(orderbook['bids']) > 0):
                        string += bcolors.OKGREEN + ' {:<15} | '.format(orderbook['bids'][0][0])
                        string += bcolors.FAIL + ' {:<15} | '.format(orderbook['asks'][0][0])
                    else:
                        string += ' {:<15} | '.format('')
                else:
                    string += ' {:<15} | '.format('')
            print(string)
    except:
        print(sym)