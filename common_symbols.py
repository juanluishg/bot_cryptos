import ccxt
import sys

if len(sys.argv) > 2:
    ids = list(sys.argv[1:])
    exchanges = {}
    print("Exchanges selected: ", ids)
    string = ' {:<15} | '.format("Exchanges")
    for id in ids:
        exchange = getattr(ccxt, id)()
        exchanges[id] = exchange
        markets = exchange.load_markets()
        string += ' {:<15} | '.format(exchanges[id].name)

    allSymbols = [symbol for id in ids for symbol in exchanges[id].symbols]
    uniqueSymbols = list(set(allSymbols))
    arbitrableSymbols = sorted(
        [symbol for symbol in uniqueSymbols if allSymbols.count(symbol) > 1])

    table = []

    print(string)

    sym = ""

    try:
        for sym in arbitrableSymbols:
            string = ' {:<15} | '.format(sym)
            for id in ids:
                if sym in exchanges[id].symbols:
                    orderbook = exchanges[id].fetch_order_book(sym)
                    if (len(orderbook['bids']) > 0):
                        string += ' {:<15} | '.format(orderbook['bids'][0][0])
                    else:
                        string += ' {:<15} | '.format('')
                else:
                    string += ' {:<15} | '.format('')
            print(string)
    except:
        print(sym)

    """"
    for symbol in arbitrableSymbols:
        string = ' {:<15} | '.format(symbol)
        row = {}
        for id in ids:
            string += ' {:<15} | '.format(id if symbol in exchanges[id].symbols else '')
        print(string)
    """
