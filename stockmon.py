from yahoo_fin import stock_info as si
import configparser
import time
from flask import Flask

# Flask setup
stockmon = Flask(__name__)
@stockmon.route('/')
def hello():
    return 'Hello World!'
if __name__ == '__main__':
    stockmon.run(host='127.0.0.1', port=8080, debug=True)

class bcolors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Config parser setup
config = configparser.ConfigParser()
if not config.read('config.ini'):
    print('No config.ini found. Creating Default one.')
    config['AMZN'] = {'purchaseprice' : '100',
                      'numberofshares' : '10'}
    config['SETTINGS'] = {}
    config['SETTINGS']['LookupDelay'] = '5'
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
    exit()
lookupdelay = int(config['SETTINGS']['LookupDelay'])
previousprice = {}
for stock in config.sections():
    if stock == 'SETTINGS':
        continue
    stocktomonitor = stock
    numberofshares = config.get(stock, 'numberofshares')
    purchaseprice = config.get(stock, 'purchaseprice')
    print('Stock to monitor: ' + stocktomonitor +
          ' bought: ' + numberofshares +
          ' at: ' + purchaseprice)
    previousprice[stock] = 0

print('Lookup delay at ' + str(lookupdelay) + 's')
print('=========================================')

while True:
    time.sleep(lookupdelay)
    for stock in config.sections():
        if stock == 'SETTINGS':
            continue
        numberofshares = config.get(stock, 'numberofshares')
        purchaseprice = config.get(stock, 'purchaseprice') 
        currentprice = round(si.get_live_price(stock), 2)
        currenttotal = int(numberofshares) * float(currentprice)
        initialtotal = int(numberofshares) * float(purchaseprice)
        if currentprice >= previousprice[stock]:
            stockcolor = bcolors.GREEN
        else:
            stockcolor = bcolors.RED
        if currenttotal >=  initialtotal:
            totalcolor = bcolors.GREEN
        else: 
            totalcolor = bcolors.RED
        print(stockcolor + stock + ":" + str(currentprice) +
              bcolors.ENDC + totalcolor + " / " + str(currenttotal) +
            " (" + str(initialtotal) + " / " + str(round(currenttotal-initialtotal, 2)) + ") " +
              bcolors.ENDC)
        previousprice[stock] = currentprice
