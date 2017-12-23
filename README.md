# EtherDelta Python Client

> Python wrapper for interacting with the [EtherDelta](https://etherdelta.com/) API and Smart Contracts.

Note: This is a fork of [this client](https://github.com/tomvanbraeckel/etherdeltaclientservice.py).

## Usage

```python
from etherdelta import etherdeltaclient as ed

client = ed.EtherDeltaClient()

# Get Buy Order Book
token = "UKG"
orders = client.get_buy_orderbook(token)

print(orders)

# Make a Trade
order_id = "959690a3d665ce5e77c76df4273170bae5e57f990436d4b909e9656f64e221f7_buy"
order = client.get_order(token, order_id)
order = order.result

expires = int(order["expires"])
token_price = 0.0001
token_amount = 1
token_address = order["tokenGet"]
pub_address = "0x123"
priv_key = "123..."
randomseed = True

signed_order = client.create_order("buy", expires, token_price, token_amount, token_address, pub_address, priv_key, randomseed)

eth_amount = 0.0001
client.trade(order, eth_amount, priv_key)
```

## Documentation

TODO

## License

MIT
