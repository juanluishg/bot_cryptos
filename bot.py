# -*- coding: utf-8 -*-

import os
import sys
root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root + '/python')

import ccxt  # noqa: E402
import style as st

proxies = [
    '',  # no proxy by default
    'https://crossorigin.me/',
    'https://cors-anywhere.herokuapp.com/',
]

if len(sys.argv) > 2:
    ids = list(sys.argv[1:])
    exchanges = {}
    st.dump(ids)
    st.dump(st.yellow(' '.join(ids)))
    for id in ids:  # load all markets from all exchange exchanges

        # instantiate the exchange by id
        exchange = getattr(ccxt, id)()

        # save it in a dictionary under its id for future use
        exchanges[id] = exchange

        # load all markets from the exchange
        markets = exchange.load_markets()

        # basic round-robin proxy scheduler
        currentProxy = -1
        maxRetries = len(proxies)

        for numRetries in range(0, maxRetries):

            # try proxies in round-robin fashion
            currentProxy = (currentProxy + 1) % len(proxies)

            try:  # try to load exchange markets using current proxy

                exchange.proxy = proxies[currentProxy]
                exchange.load_markets()

            except ccxt.DDoSProtection as e:
                st.dump(st.yellow(type(e).__name__), e.args)
            except ccxt.RequestTimeout as e:
                st.dump(st.yellow(type(e).__name__), e.args)
            except ccxt.AuthenticationError as e:
                st.dump(st.yellow(type(e).__name__), e.args)
            except ccxt.ExchangeNotAvailable as e:
                st.dump(st.yellow(type(e).__name__), e.args)
            except ccxt.ExchangeError as e:
                st.dump(st.yellow(type(e).__name__), e.args)
            except ccxt.NetworkError as e:
                st.dump(st.yellow(type(e).__name__), e.args)
            except Exception as e:  # reraise all other exceptions
                raise

        st.dump(st.green(id), 'loaded', st.green(str(len(exchange.symbols))), 'markets')

    st.dump(st.green('Loaded all markets'))

    allSymbols = [symbol for id in ids for symbol in exchanges[id].symbols]

    # get all unique symbols
    uniqueSymbols = list(set(allSymbols))

    # filter out symbols that are not present on at least two exchanges
    arbitrableSymbols = sorted([symbol for symbol in uniqueSymbols if allSymbols.count(symbol) > 1])

    # print a table of arbitrable symbols
    table = []
    st.dump(st.green(' symbol          | ' + ''.join([' {:<15} | '.format(id) for id in ids])))
    st.dump(st.green(''.join(['-----------------+-' for x in range(0, len(ids) + 1)])))

    for symbol in arbitrableSymbols:
        string = ' {:<15} | '.format(symbol)
        row = {}
        for id in ids:
            # if a symbol is present on a exchange print that exchange's id in the row
            string += ' {:<15} | '.format(id if symbol in exchanges[id].symbols else '')
        st.dump(string)

else:
    st.print_usage()
