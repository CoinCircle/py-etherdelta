Help on module __init__:

NAME
    __init__

CLASSES
    builtins.object
        Client

    class Client(builtins.object)
     |  Methods defined here:
     |
     |  __init__(self)
     |      Initialize self.  See help(type(self)) for accurate signature.
     |
     |  cancel_order(self, order, user_private_key, user_address)
     |      Cancels an order on-chain
     |
     |      :param order: order
     |      :type order: object
     |      :param user_private_key: user private key
     |      :type user_private_key: string
     |      :param user_address: user address
     |      :type user_address: string
     |      :return: tx
     |      :rtype: object
     |
     |  create_order(self, side, expires, price, amount, token_addr, randomseed, user_private_key, user_address)
     |      Returns a signed order
     |
     |      :param side: buy or sell type
     |      :type side: str
     |      :param expires: expiration time in unix time
     |      :type expires: int
     |      :param price: price in ETH
     |      :type price: float
     |      :param amount: amount buying or selling
     |      :type amount: int
     |      :param token_addr: token address
     |      :type token_addr: string
     |      :param randomseed: use random seed
     |      :type randomseed: bool
     |      :param user_private_key: user private key
     |      :type user_private_key: string
     |      :param user_address: user address
     |      :type user_address: string
     |      :return: signed order
     |      :rtype: object
     |
     |  get_amount_filled(self, symbol, order_id)
     |      Returns amount filled for an order given order ID
     |
     |      :param symbol: token symbol
     |      :type symbol: str
     |      :param order_id: order ID
     |      :type order_id: str
     |      :return: filled amount
     |      :rtype: int
     |
     |  get_available_volume(self, symbol, order_id)
     |      Returns available volume for an order give order ID
     |
     |      :param symbol: token symbol
     |      :type symbol: str
     |      :param order_id: order ID
     |      :type order_id: str
     |      :return: available volume
     |      :rtype: int
     |
     |  get_block_number(self)
     |      Returns the highest block number
     |
     |      :return: block number
     |      :rtype: int
     |
     |  get_buy_orderbook(self, symbol)
     |      Returns the buy (bids) orderbook
     |
     |      :param symbol: token symbol
     |      :type symbol: str
     |      :return: buy orderbook list
     |      :rtype: list
     |
     |  get_eth_balance(self, account)
     |      Returns the ETH balance of an account
     |
     |      :param account: account
     |      :type account: str
     |      :return: balance
     |      :rtype: float
     |
     |  get_etherdelta_balance(self, account)
     |      Returns the ETH balance in EtherDelta of an account
     |
     |      :param account: account
     |      :type account: str
     |      :return: balance
     |      :rtype: int
     |
     |  get_order(self, symbol, order_id)
     |      Returns the the order information for a token given the symbol and order ID
     |
     |      :param symbol: token symbol
     |      :type account: str
     |      :param order_id: order ID
     |      :type order_id: str
     |      :return: order
     |      :rtype: object
     |
     |  get_orders(self, symbol)
     |      Returns the orders for a token given the symbol
     |
     |      :param symbol: token symbol
     |      :type account: str
     |      :return: orders
     |      :rtype: list
     |
     |  get_sell_orderbook(self, symbol)
     |      Returns the sell (asks) orderbook
     |
     |      :param symbol: token symbol
     |      :type symbol: str
     |      :return: sell orderbook list
     |      :rtype: list
     |
     |  get_ticker(self, symbol)
     |      Returns ticker data for token
     |
     |      :param symbol: token symbol
     |      :type symbol: str
     |      :return: ticker data
     |      :rtype: object
     |
     |  get_token_address(self, symbol)
     |      Returns the token address given the token symbol
     |
     |      :param symbol: token symbol
     |      :type account: str
     |      :return: token address
     |      :rtype: str
     |
     |  get_token_balance(self, token_addr, account)
     |      Returns the token balance of an account
     |
     |      :param token_addr: token address
     |      :type account: str
     |      :param account: account
     |      :type account: str
     |      :return: balance
     |      :rtype: int
     |
     |  listen_once_and_close(self, emitTopic, emitMessage, eventTopic, callback)
     |
     |  on_error(self, ws, err)
     |
     |  on_ping(self, ws, ping)
     |
     |  on_pong(self, ws, pong)
     |
     |  post_order(self, order)
     |      Posts an order to the off-chain order book
     |
     |      :param order: signed order
     |      :type order: object
     |      :return: response
     |      :rtype: string
     |
     |  send_message(self, argObject)
     |
     |  solidity_sha256(self, abi_types, values)
     |      # This function is very similar to Web3.soliditySha3() but there is no Web3.solidity_sha256() as per November 2017
     |      # It serializes values according to the ABI types defined in abi_types and hashes the result with sha256.
     |
     |  trade(self, order, eth_amount, user_private_key, user_address)
     |      Invokes on-chain trade
     |
     |      :param order: order
     |      :type order: object
     |      :param eth_amount: ETH amount
     |      :type eth_amount: float
     |      :param user_private_key: user private key
     |      :type user_private_key: string
     |      :param user_address: user address
     |      :type user_address: string
     |      :return: tx
     |      :rtype: object
     |
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |
     |  __dict__
     |      dictionary for instance variables (if defined)
     |
     |  __weakref__
     |      list of weak references to the object (if defined)
     |
     |  ----------------------------------------------------------------------
     |  Data and other attributes defined here:
     |
     |  ws = None

DATA
    addressEtherDelta = '0x8d12A197cB00D4747a1fe03395095ce2A5CC6819'
    w3 = <web3.main.Web3 object>
    websocket_url = 'wss://socket04.etherdelta.com/socket.io/?EIO=3&transp...

VERSION
    1.0

FILE
    /etherdelta/__init__.py


