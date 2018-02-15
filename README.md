# EtherDelta Python Client

> Python wrapper for interacting with the [EtherDelta](https://etherdelta.com/) API and Smart Contracts.

This was originally a fork of [this client](https://github.com/tomvanbraeckel/etherdeltaclientservice.py).

# Install

```bash
pip3 install etherdelta
```
or (always latest)

```
pip3 install git+git://github.com/miguelmota/py-etherdelta.git
```

## Documentation

[Documentation](./doc/README.md)

### Examples

Get account ETH balance

```python
client = etherdelta.Client()
account = '0x85E4B84D784eE9eEB7489F0B0c66B343AF2a0BE5'
bal = client.get_eth_balance(account)
print(bal) # 0.053658783
```

Get account token balance

```python
client = etherdelta.Client()
account = '0x85E4B84D784eE9eEB7489F0B0c66B343AF2a0BE5'
token_addr = '0x0d8775f648430679a709e98d2b0cb6250d2887ef'
bal = client.get_token_balance(account, token_addr)
print(bal) # 71.464571009031715384
```

Get account ETH balance on EtherDelta

```python
client = etherdelta.Client()
account = '0x85E4B84D784eE9eEB7489F0B0c66B343AF2a0BE5'
bal = client.get_etherdelta_eth_balance(account)
print(bal) # 0.060271757614136072
```

Get account token balance on EtherDelta

```python
client = etherdelta.Client()
account = '0x85E4B84D784eE9eEB7489F0B0c66B343AF2a0BE5'
token_addr = '0x0d8775f648430679a709e98d2b0cb6250d2887ef'
bal = client.get_etherdelta_token_balance(account, token_addr)
print(bal) # 0
```

Get highest block number

```python
client = etherdelta.Client()
number = client.get_block_number()
print(number) # 5018972
```

Get token address of token symbol

```python
client = etherdelta.Client()
symbol = 'BAT'
token_addr = client.get_token_address(symbol)
print(token_addr) # 0x0d8775f648430679a709e98d2b0cb6250d2887ef
```

Get ticker data for all tokens

```python
client = etherdelta.Client()
tickers = client.get_tickers()
print(tickers)
# {'ETH_0xec46': {'ask': 0.01, 'quoteVolume': 193.809, 'last': 0.000300001, 'baseVolume': 0.058, 'bid': 0.000300002, 'percentChange': 0, 'tokenAddr': '0xec46f8207d766012454c408de210bcbc2243e71c'}, 'ETH_EMV': {'ask': 0.0004579, 'quoteVolume': 11451.47, 'last': 0.0004579, 'baseVolume': 4.647, 'bid': 0.0004586, 'percentChange': 0.2376, 'tokenAddr': '0xb802b24e0637c2b87d2e8b7784c055bbe921011a'}}
```

Get ticker data for a token

```python
client = etherdelta.Client()
symbol = 'BAT'
ticker = client.get_ticker(symbol)
print(ticker)
# {'quoteVolume': 2603.107, 'bid': 0.000421, 'baseVolume': 1.135, 'tokenAddr': '0x0d8775f648430679a709e98d2b0cb6250d2887ef', 'last': 0.000477839, 'ask': 0.000477838, 'percentChange': 0.0607}
```

Get orderbook (all buy and sell orders) for token

```python
client = etherdelta.Client()
token_addr = '0x0d8775f648430679a709e98d2b0cb6250d2887ef'
orders = client.get_orderbook(token_addr)
print(orders)
# {'buys': [{'s': '0x36728e74f49ed1ef7f85e603c8ea4b149f5c427b9f0bfc6bc072ad780486dd7b', 'user': '0x0f8aa39a58adcc3df98d826ac798ab837cc0833c', 'ethAvailableVolume': '6755.671999999999', 'amount': '6755671999999999213568', 'availableVolumeBase': '2876979662150982000', 'tokenGive': '0x0000000000000000000000000000000000000000', 'expires': '5019005', 'amountFilled': None, 'updated': '2018-02-02T19:42:59.089Z', 'nonce': '4500026492', 'id': '9f365bafc972b2e21ed52569075647c4778385c0ce9283cb16630df78ed99f72_buy', 'availableVolume': '6.755671999999999213568e+21', 'r': '0xa3ca2a8fb3773271b073bc45a1b81138d8bf95c82ca877bf407ec3250a934b2a', 'tokenGet': '0x0d8775f648430679a709e98d2b0cb6250d2887ef', 'amountGet': '6755671999999999213568', 'v': 28, 'price': '0.00042586135948444247', 'ethAvailableVolumeBase': '2.876979662150982', 'amountGive': '2876979662150982144'}}
```

Get order from ID

```python
client = etherdelta.Client()
token_addr = '0x0d8775f648430679a709e98d2b0cb6250d2887ef'
order_id = '6e40fdfc81d58a70405431599a1d5c76d502b3cf02e1936bc36f1e8583c0d2b9_sell'
order = client.get_order(token_addr, order_id)
print(order)
# {'ethAvailableVolumeBase': '4.495', 'availableVolume': '100000000000000', 'expires': '1004639969', 'user': '0x2C34973C4c46f13534C81A893645F347B65c89d6', 'amount': '-100000000000000', 'r': '0xff456276e336d37bee3e59f9c8e46e9dffa4dea73dfe85dcad73df543ebc9ec2', 'price': '44950', 'nonce': '1384390526', 'v': 27, 'id': '6e40fdfc81d58a70405431599a1d5c76d502b3cf02e1936bc36f1e8583c0d2b9_sell', 'tokenGive': '0x0d8775f648430679a709e98d2b0cb6250d2887ef', 'updated': '2017-11-28T21:15:11.423Z', 'availableVolumeBase': '4495000000000000000', 'amountFilled': None, 'ethAvailableVolume': '0.0001', 'amountGive': '100000000000000', 's': '0x166c467778a5f89aa3d9283eca77d5e4d857a6de365da9f25b8ec30446ae08e5', 'tokenGet': '0x0000000000000000000000000000000000000000', 'amountGet': '4495000000000000000'}
```

Get buy (bids) orderbook for a token

```python
client = etherdelta.Client()
token_addr = '0x0d8775f648430679a709e98d2b0cb6250d2887ef'
orders = client.get_buy_orderbook(token_addr)
print(orders)
# [{'availableVolumeBase': '6115302748878024', 'user': '0x9b3e7f46e4e8894d4bc84bb3200161cc6f0fa0f2', 'tokenGet': '0x0d8775f648430679a709e98d2b0cb6250d2887ef', 'amountGive': '189450000000000000', 'amount': '450000000000000000000', 's': '0x07ec06b8e95e84530755a55aa20d8e16d978592a76d1990ba38f96c35be930af', 'ethAvailableVolumeBase': '0.006115302748878024', 'updated': '2018-02-02T17:40:30.400Z', 'price': '0.000421', 'expires': '5028370', 'id': '0f97c3f4c9d78eb44f20395adfa4ed85b4a5f69389853faa6f2cad2b0c24931e_buy', 'nonce': '2687232062', 'amountFilled': None, 'r': '0xb47fce6954b181d656629f62f7c9ff6a7bd11604a5e26bc7a00a099e396c5138', 'availableVolume': '14525659736052313539', 'amountGet': '450000000000000000000', 'tokenGive': '0x0000000000000000000000000000000000000000', 'ethAvailableVolume': '14.525659736052313', 'v': 27}]
```

Get sell (asks) orderbook for a token

```python
client = etherdelta.Client()
token_addr = '0x0d8775f648430679a709e98d2b0cb6250d2887ef'
orders = client.get_sell_orderbook(token_addr)
print(orders)
# [{'user': '0x955051F2cF3bA245ae8Ee9057458836eAe3b1FeC', 'expires': '5018717', 'amount': '-2.1572374771676692e+21', 'ethAvailableVolumeBase': '1.0308100416148447', 'tokenGet': '0x0000000000000000000000000000000000000000', 'ethAvailableVolume': '2157.237477167669', 'updated': '2018-02-02T18:15:21.791Z', 'price': '0.000477838', 'r': '0xe3129e0ec2110063d16d84ac4770f402555614d077b6cfd1ba9d701839f0691d', 'availableVolumeBase': '1030810041614844700', 'v': 28, 'availableVolume': '2.15723747716766907792023752118211285330018e+21', 'amountGet': '1030810041614844700', 'id': 'b66abf9a645756ef32aff132d6dde19ad7d7b2c5c026475c60140da266186a01_sell', 'nonce': '26698014251852476', 'tokenGive': '0x0d8775f648430679a709e98d2b0cb6250d2887ef', 's': '0x38a06acd697cb5cf91f9c8d19389904331b1014a0713a11f775f632d7e7e4dc3', 'amountFilled': None, 'amountGive': '2.157237477167669064104e+21'}]
```

Get amount filled for an order

```python
client = etherdelta.Client()
token_addr = '0x0d8775f648430679a709e98d2b0cb6250d2887ef'
order_id = '6e40fdfc81d58a70405431599a1d5c76d502b3cf02e1936bc36f1e8583c0d2b9_sell'
filled = client.get_amount_filled(token_addr, order_id)
print(filled) # 0
```

Get available volume of an order

```python
client = etherdelta.Client()
token_addr = '0x0d8775f648430679a709e98d2b0cb6250d2887ef'
order_id = '6e40fdfc81d58a70405431599a1d5c76d502b3cf02e1936bc36f1e8583c0d2b9_sell'
volume = client.get_available_volume(token_addr, order_id)
print(volume) # 4495000000000000000
```

Make a trade

```python
import etherdelta

client = etherdelta.Client()

# Get Buy Order Book
token_addr = '0x0d8775f648430679a709e98d2b0cb6250d2887ef'
orders = client.get_buy_orderbook(token_addr)

print(orders)

# Make a Trade
order_id = '959690a3d665ce5e77c76df4273170bae5e57f990436d4b909e9656f64e221f7_buy'
order = client.get_order(token_addr, order_id)

expires = int(order['expires'])
token_price = 0.0001
token_amount = 1
token_address = order['tokenGet']
priv_key = '123...'
randomseed = True

signed_order = client.create_order('buy', expires, token_price, token_amount, token_address, randomseed, priv_key)

eth_amount = 0.0001
tx = client.trade(order, eth_amount, priv_key)
print(tx)
```

## Development

Install Web3.py

<!--
```bash
git clone git@github.com:ethereum/web3.py.git
cd web3.py
virtualenv -p python3 venvpy3
pip3 install -r requirements-dev.txt
pip3 install -e .
```
-->
```bash
sudo pip3 install git+git://github.com/ethereum/web3.py.git
```

Install dependencies

<!--
```bash
virtualenv -p python3 venvpy3
. venvpy3/bin/activate
pip3 install websocket-client
pip3 install twisted
```
-->
```bash
pip3 install -r requirements.txt
```

## FAQ

- Q: Why do I get empty results sometimes?

    - A: Unfortunately, the EtherDelta websocket client is unreliable.

- Q: Why doesn't `get_ticker()` return any data?

    - A: For some reason the EtherDelta API doesn't return this data anymore.

- Q: Why doesn't `get_token_address()` work?

    - A: This method is dependent on the `get_ticker()` method. See above question.

# Resources

- [EtherDelta API](https://github.com/etherdelta/etherdelta.github.io/blob/master/docs/API.md)

- [EtherDelta Smart Contracts](https://github.com/etherdelta/etherdelta.github.io/blob/master/docs/SMART_CONTRACT.md)

## License

MIT
