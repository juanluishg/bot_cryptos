import ccxt
import sys

print("Arguments: ", sys.argv)

if len(sys.argv) == 4:
    try:
        exchange1 = getattr(ccxt, sys.argv[1])();
        pair = sys.argv[3];
        orderbook1 = exchange1.fetch_order_book(pair);
        print(exchange1.name, orderbook1['bids'][0][0]);

        exchange2 = getattr(ccxt, sys.argv[2])();
        pair = sys.argv[3];
        orderbook2 = exchange2.fetch_order_book(pair);
        print(exchange2.name, orderbook2['asks'][0][0]);

        print(exchange2.fetchFees())

    except Exception as e :
        print("Error", e);



else: 
    print("Bad arguments")
    print("python3 arbitrage.py `exchange1´ `exchange2´ `pair´")