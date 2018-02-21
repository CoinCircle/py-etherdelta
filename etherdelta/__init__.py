#!/usr/bin/python3
__version__ = '0.0.1'

import hashlib
import websocket
import _thread
import time
import json
import random
import sys
import os
import web3
from web3 import Web3, HTTPProvider
from operator import itemgetter
from collections import OrderedDict
# The functions below are used for our solidity_sha256() function
#from web3.utils.normalizers import abi_ens_resolver
from web3.utils.abi import map_abi_data
from eth_utils import add_0x_prefix, remove_0x_prefix
from web3.utils.encoding import hex_encode_abi_type

# etherdelta_2's contract address
addressEtherDelta = '0x8d12A197cB00D4747a1fe03395095ce2A5CC6819'
w3 = Web3(HTTPProvider('https://mainnet.infura.io/'))

class Client:
    ws = None
    websocket_url = None

    def __init__(self):
        self.websocket_url = 'wss://socket05.etherdelta.com/socket.io/?EIO=3&transport=websocket'
        self.bootstrap()

    def bootstrap(self):
        token_abi = None
        with open(os.path.join(os.path.dirname(__file__), './contracts/token.json'), 'r') as token_abi_definition:
            token_abi = json.load(token_abi_definition)
        self.token_abi = token_abi
        global addressEtherDelta
        addressEtherDelta = Web3.toChecksumAddress(addressEtherDelta)
        with open(os.path.join(os.path.dirname(__file__), './contracts/etherdelta.json'), 'r') as abi_definition:
            abiEtherDelta = json.load(abi_definition)
        self.contractEtherDelta = w3.eth.contract(address=addressEtherDelta, abi=abiEtherDelta)

    def get_eth_balance(self, account):
        """
        Returns the ETH balance of an account

        :param account: account
        :type account: str
        :return: balance
        :rtype: float
        """
        account = Web3.toChecksumAddress(account)
        balance = w3.eth.getBalance(account)
        return w3.fromWei(balance, 'ether')

    def get_token_balance(self, account, token_addr):
        """
        Returns the token balance of an account

        :param account: account
        :type account: str
        :param token_addr: token address
        :type token_addr: str
        :return: balance
        :rtype: int
        """
        token_addr = Web3.toChecksumAddress(token_addr)
        contractToken = w3.eth.contract(address=token_addr, abi=self.token_abi)
        account = Web3.toChecksumAddress(account)
        balance = contractToken.call().balanceOf(account)
        return w3.fromWei(balance, 'ether')

    def get_etherdelta_eth_balance(self, account):
        """
        Returns the ETH balance in EtherDelta of an account

        :param account: account
        :type account: str
        :return: balance
        :rtype: int
        """
        account = Web3.toChecksumAddress(account)
        balance = self.contractEtherDelta.call().balanceOf(token='0x0000000000000000000000000000000000000000', user=account)
        return w3.fromWei(balance, 'ether')

    def get_etherdelta_token_balance(self, account, token_addr):
        """
        Returns the token balance in EtherDelta of an account

        :param account: account
        :type account: str
        :param token_addr: token address
        :type token_addr: str
        :return: balance
        :rtype: int
        """
        account = Web3.toChecksumAddress(account)
        balance = 0
        if token_addr:
            balance = self.contractEtherDelta.call().balanceOf(token=token_addr, user=account)
        return w3.fromWei(balance, 'ether')

    def get_token_address(self, symbol):
        """
        Returns the token address given the token symbol

        :param symbol: token symbol
        :type account: str
        :return: token address
        :rtype: str
        """
        ticker = self.get_ticker(symbol)
        tokenAddr = ''
        if ticker != None:
            if ticker:
                if hasattr(ticker, 'result'):
                    if ticker.result:
                        if ticker.result['tokenAddr']:
                            tokenAddr = ticker.result['tokenAddr']
        return tokenAddr

    def get_orderbook(self, token_addr):
        """
        Returns the orderbook for a token given the symbol

        :param token_addr: token address
        :type token_addr: str
        :return: orderbook
        :rtype: list
        """
        result = {}
        def done():
            yield result
        def callback(msg):
            nonlocal result
            self.ws.close()
            if msg:
                if msg['orders']:
                    result = msg['orders']
            done()
        emitMessage = '42["getMarket",{"token":"' + token_addr + '","user":""}]'
        self.listen_once_and_close('getMarket', emitMessage, 'market', callback)
        return next(done())

    def get_order(self, token_addr, order_id):
        """
        Returns the the order information for a token given the symbol and order ID

        :param token_addr: token address
        :type token_addr: str
        :param order_id: order ID
        :type order_id: str
        :return: order
        :rtype: object
        """
        result = {}
        def done():
            yield result
        def callback(msg):
            nonlocal result
            self.ws.close()
            if msg:
                if msg['orders']:
                    orders = msg['orders']
                    for o in orders['sells']:
                        if o['id'] == order_id:
                            result = o
                    for o in orders['buys']:
                        if o['id'] == order_id:
                            result = o
            done()
        emitMessage = '42["getMarket",{"token":"' + token_addr + '","user":""}]'
        self.listen_once_and_close('getMarket', emitMessage, 'market', callback)
        return next(done())

    def get_sell_orderbook(self, token_addr):
        """
        Returns the sell (asks) orderbook

        :param token_addr: token address
        :type token_addr: str
        :return: sell orderbook list
        :rtype: list
        """
        result = []
        def done():
            yield result
        def callback(msg):
            nonlocal result
            self.ws.close()
            if msg['orders']:
                if msg['orders']['sells']:
                    result = msg['orders']['sells']
            done()
        emitMessage = '42["getMarket",{"token":"' + token_addr + '","user":""}]'
        self.listen_once_and_close('getMarket', emitMessage, 'market', callback)
        return next(done())

    def get_buy_orderbook(self, token_addr):
        """
        Returns the buy (bids) orderbook

        :param token_addr: token address
        :type token_addr: str
        :return: buy orderbook list
        :rtype: list
        """
        result = []
        def done():
            yield result
        def callback(msg):
            nonlocal result
            self.ws.close()
            if msg['orders']:
                if msg['orders']['buys']:
                    result = msg['orders']['buys']
                    return done()
            return done()
        emitMessage = '42["getMarket",{"token":"' + token_addr + '","user":""}]'
        self.listen_once_and_close('getMarket', emitMessage, 'market', callback)
        return next(done())

    def get_amount_filled(self, token_addr, order_id):
        """
        Returns amount filled for an order given order ID

        :param token_addr: token address
        :type token_addr: str
        :param order_id: order ID
        :type order_id: str
        :return: filled amount
        :rtype: int
        """
        order = self.get_order(token_addr, order_id)
        if order == None:
            return None
        amountGet = int('{:.0f}'.format(float(order['amountGet'])))
        amountGive = int('{:.0f}'.format(float(order['amountGive'])))
        tokenGet = Web3.toChecksumAddress(order['tokenGet'])
        tokenGive = Web3.toChecksumAddress(order['tokenGive'])
        expires = int(order['expires'])
        nonce = int(order['nonce'])
        user = Web3.toChecksumAddress(order['user'])
        v = int(order['v'])
        r = Web3.toBytes(hexstr=order['r'])
        s = Web3.toBytes(hexstr=order['s'])
        amount_filled = self.contractEtherDelta.call().amountFilled(tokenGet, amountGet, tokenGive, amountGive, expires, nonce, user, v, r, s)
        return amount_filled

    def get_available_volume(self, token_addr, order_id):
        """
        Returns available volume for an order give order ID

        :param token_addr: token address
        :type token_addr: str
        :param order_id: order ID
        :type order_id: str
        :return: available volume
        :rtype: int
        """
        order = self.get_order(token_addr, order_id)
        if order == None:
            return None
        amountGet = int('{:.0f}'.format(float(order['amountGet'])))
        amountGive = int('{:.0f}'.format(float(order['amountGive'])))
        tokenGet = Web3.toChecksumAddress(order['tokenGet'])
        tokenGive = Web3.toChecksumAddress(order['tokenGive'])
        expires = int(order['expires'])
        nonce = int(order['nonce'])
        user = Web3.toChecksumAddress(order['user'])
        v = int(order['v'])
        r = Web3.toBytes(hexstr=order['r'])
        s = Web3.toBytes(hexstr=order['s'])
        available_volume = self.contractEtherDelta.call().availableVolume(tokenGet, amountGet, tokenGive, amountGive, expires, nonce, user, v, r, s)
        return available_volume

    def get_ticker(self, symbol=''):
        """
        Returns ticker data for token

        :param symbol: token symbol
        :type symbol: str
        :return: ticker data
        :rtype: object
        """
        result = {}
        def done():
            yield result
        def callback(msg):
            nonlocal result
            self.ws.close()
            if msg:
                if msg['returnTicker']:
                    if msg['returnTicker']['ETH_' + symbol.upper()]:
                        result = msg['returnTicker']['ETH_' + symbol.upper()]
            done()
        emitMessage = '42["getMarket",{"token":"","user":"0x0000000000000000000000000000000000000000"}]'
        self.listen_once_and_close('getMarket', emitMessage, 'market', callback)
        return next(done())

    def get_tickers(self):
        """
        Returns ticker data for all tokens

        :return: ticker data
        :rtype: object
        """
        result = {}
        def done():
            yield result
        def callback(msg):
            nonlocal result
            self.ws.close()
            print(msg)
            if msg != None:
                if msg:
                    if msg['returnTicker']:
                        result = msg['returnTicker']
            done()
        emitMessage = '42["getMarket",{"token":"","user":"0x0000000000000000000000000000000000000000"}]'
        self.listen_once_and_close('getMarket', emitMessage, 'market', callback)
        return next(done())

    def get_block_number(self):
        """
        Returns the highest block number

        :return: block number
        :rtype: int
        """
        return w3.eth.blockNumber

    def create_order(self, side, expires, price, amount, token_addr, randomseed, user_private_key):
        """
        Returns a signed order

        :param side: buy or sell type
        :type side: str
        :param expires: expiration time in unix time
        :type expires: int
        :param price: price in ETH
        :type price: float
        :param amount: amount buying or selling
        :type amount: int
        :param token_addr: token address
        :type token_addr: string
        :param randomseed: use random seed
        :type randomseed: bool
        :param user_private_key: user private key
        :type user_private_key: string
        :return: signed order
        :rtype: object
        """
        global addressEtherDelta, w3
        userAccount = w3.eth.account.privateKeyToAccount(user_private_key).address
        print("\nCreating '" + side + "' order for %.18f tokens @ %.18f ETH/token" % (amount, price))
        # Validate the input
        if len(user_private_key) != 64: raise ValueError('WARNING: user_private_key must be a hexadecimal string of 64 characters long')
        # Ensure good parameters
        token = Web3.toChecksumAddress(token_addr)
        userAccount = Web3.toChecksumAddress(userAccount)
        user_private_key = Web3.toBytes(hexstr=user_private_key)
        # Build the order parameters
        amountBigNum = amount
        amountBaseBigNum = float(amount) * float(price)
        if randomseed != None: random.seed(randomseed)    # Seed the random number generator for unit testable results
        orderNonce = random.randint(0,10000000000)
        if side == 'sell':
            tokenGive = token
            tokenGet = '0x0000000000000000000000000000000000000000'
            amountGet = w3.toWei(amountBaseBigNum, 'ether')
            amountGive = w3.toWei(amountBigNum, 'ether')
        elif side == 'buy':
            tokenGive = '0x0000000000000000000000000000000000000000'
            tokenGet = token
            amountGet = w3.toWei(amountBigNum, 'ether')
            amountGive = w3.toWei(amountBaseBigNum, 'ether')
        else:
            print('WARNING: invalid order side, no action taken: ' + str(side))
        # Serialize (according to ABI) and sha256 hash the order's parameters
        hashhex = self.solidity_sha256(
            ['address', 'address', 'uint256', 'address', 'uint256', 'uint256', 'uint256'],
            [addressEtherDelta, tokenGet, amountGet, tokenGive, amountGive, expires, orderNonce]
        )
        # Sign the hash of the order's parameters with our private key (this also addes the "Ethereum Signed Message" header)
        signresult = w3.eth.account.sign(message_hexstr=hashhex, private_key=user_private_key)
        #print("Result of sign:" + str(signresult))
        orderDict = {
            'amountGet' : amountGet,
            'amountGive' : amountGive,
            'tokenGet' : tokenGet,
            'tokenGive' : tokenGive,
            'contractAddr' : addressEtherDelta,
            'expires' : expires,
            'nonce' : orderNonce,
            'user' : userAccount,
            'v' : signresult['v'],
            'r' : signresult['r'],
            's' : signresult['s'],
        }
        return orderDict

    def post_order(self, order):
        """
        Posts an order to the off-chain order book

        :param order: signed order
        :type order: object
        :return: response
        :rtype: string
        """
        result = ''
        def done():
            yield result
        def callback(msg):
            nonlocal result
            self.ws.close()
            result = msg
        emitMessage = '42["message",' + json.JSONEncoder().encode(order) + ']'
        self.listen_once_and_close("message", emitMessage, "messageResult", callback)
        return next(done())

    def trade(self, order, eth_amount, user_private_key):
        """
        Invokes on-chain trade

        :param order: order
        :type order: object
        :param eth_amount: ETH amount
        :type eth_amount: float
        :param user_private_key: user private key
        :type user_private_key: string
        :return: tx
        :rtype: object
        """
        global web3, addressEtherDelta
        userAccount = w3.eth.account.privateKeyToAccount(user_private_key).address
        # Transaction info
        maxGas = 250000
        gasPriceWei = 1000000000    # 1 Gwei
        if order['tokenGive'] == '0x0000000000000000000000000000000000000000':
            ordertype = 'buy'    # it's a buy order so we are selling tokens for ETH
            amount = eth_amount / float(order['price'])
        else:
            ordertype = 'sell'   # it's a sell order so we are buying tokens for ETH
            amount = eth_amount
        amount_in_wei = web3.toWei(amount, 'ether')
        print("\nTrading " + str(eth_amount) + " ETH of tokens (" + str(amount) + " tokens) against this " + ordertype + " order: %.10f tokens @ %.10f ETH/token" % (float(order['ethAvailableVolume']), float(order['price'])))
        print("Details about order: " + str(order))
        # trade function arguments
        kwargs = {
            'tokenGet' : Web3.toChecksumAddress(order['tokenGet']),
            'amountGet' : int(float(order['amountGet'])),
            'tokenGive' : Web3.toChecksumAddress(order['tokenGive']),
            'amountGive' : int(float(order['amountGive'])),
            'expires' : int(order['expires']),
            'nonce' : int(order['nonce']),
            'user' : Web3.toChecksumAddress(order['user']),
            'v' : order['v'],
            'r' : w3.toBytes(hexstr=order['r']),
            's' : w3.toBytes(hexstr=order['s']),
            'amount' : int(amount_in_wei),
        }
        # Bail if there's no private key
        if len(user_private_key) != 64: raise ValueError('WARNING: user_private_key must be a hexadecimal string of 64 characters long')
        # Build binary representation of the function call with arguments
        abidata = self.contractEtherDelta.encodeABI('trade', kwargs=kwargs)
        print("abidata: " + str(abidata))
        nonce = w3.eth.getTransactionCount(userAccount)
        # Override to have same as other transaction:
        #nonce = 53
        print("nonce: " + str(nonce))
        transaction = { 'to': addressEtherDelta, 'from': userAccount, 'gas': maxGas, 'gasPrice': gasPriceWei, 'data': abidata, 'nonce': nonce, 'chainId': 1}
        print(transaction)
        signed = w3.eth.account.signTransaction(transaction, user_private_key)
        print("signed: " + str(signed))
        result = w3.eth.sendRawTransaction(w3.toHex(signed.rawTransaction))
        print("Transaction returned: " + str(result))
        print("\nDone! You should see the transaction show up at https://etherscan.io/tx/" + w3.toHex(result))
        return result

    def cancel_order(self, order, user_private_key):
        """
        Cancels an order on-chain

        :param order: order
        :type order: object
        :param user_private_key: user private key
        :type user_private_key: string
        :return: tx
        :rtype: object
        """
        global w3, addressEtherDelta
        userAccount = w3.eth.account.privateKeyToAccount(user_private_key).address
        # Transaction info
        maxGas = 250000
        gasPriceWei = 1000000000    # 1 Gwei
        print("\nCancelling")
        print("Details about order: " + str(order))
        # trade function arguments
        kwargs = {
            'tokenGet' : Web3.toChecksumAddress(order['tokenGet']),
            'amountGet' : int(float(order['amountGet'])),
            'tokenGive' : Web3.toChecksumAddress(order['tokenGive']),
            'amountGive' : int(float(order['amountGive'])),
            'expires' : int(order['expires']),
            'nonce' : int(order['nonce']),
            'v' : order['v'],
            'r' : w3.toBytes(hexstr=order['r']),
            's' : w3.toBytes(hexstr=order['s']),
        }
        # Bail if there's no private key
        if len(user_private_key) != 64: raise ValueError('WARNING: user_private_key must be a hexadecimal string of 64 characters long')
        # Build binary representation of the function call with arguments
        abidata = self.contractEtherDelta.encodeABI('cancelOrder', kwargs=kwargs)
        print("abidata: " + str(abidata))
        nonce = w3.eth.getTransactionCount(userAccount)
        # Override to have same as other transaction:
        #nonce = 53
        print("nonce: " + str(nonce))
        transaction = { 'to': addressEtherDelta, 'from': userAccount, 'gas': maxGas, 'gasPrice': gasPriceWei, 'data': abidata, 'nonce': nonce, 'chainId': 1}
        print(transaction)
        signed = w3.eth.account.signTransaction(transaction, user_private_key)
        print("signed: " + str(signed))
        result = w3.eth.sendRawTransaction(w3.toHex(signed.rawTransaction))
        print("Transaction returned: " + str(result))
        print("\nDone! You should see the transaction show up at https://etherscan.io/tx/" + w3.toHex(result))
        return result

    # This function is very similar to Web3.soliditySha3() but there is no Web3.solidity_sha256() as per November 2017
    # It serializes values according to the ABI types defined in abi_types and hashes the result with sha256.
    def solidity_sha256(self, abi_types, values):
        # TODO
        #normalized_values = map_abi_data([abi_ens_resolver(Web3)], abi_types, values)
        normalized_values = map_abi_data([], abi_types, values)
        #print(normalized_values)
        hex_string = add_0x_prefix(''.join(
            remove_0x_prefix(hex_encode_abi_type(abi_type, value))
            for abi_type, value
            in zip(abi_types, normalized_values)
        ))
        hash_object = hashlib.sha256(Web3.toBytes(hexstr=hex_string))
        return hash_object.hexdigest()

    def listen_once_and_close(self, emitTopic, emitMessage, eventTopic, callback):
        tries = 0
        max_tries = 3
        def on_message(ws, message):
            if message[:2] != '42':
                pass
            else:
                j = json.loads(message[2:])
                if not j:
                    pass
                else:
                    if j[0] == eventTopic:
                        if j[1]:
                            callback(j[1])
                        else:
                            make_request()
                    else:
                        make_request()
        def on_open(ws):
            self.ws.send(emitMessage)
        def on_close(ws):
            pass
        def make_request():
            nonlocal tries
            nonlocal max_tries
            if tries > max_tries:
                pass
            self.ws = websocket.WebSocketApp(
                self.websocket_url,
                on_message = on_message,
                  on_ping = self.on_ping,
                  on_pong = self.on_pong,
                  on_error = self.on_error,
                  on_close = on_close)
            self.ws.on_open = on_open
            self.ws.run_forever(ping_interval=10)
            tries = tries + 1
        make_request()

    def send_message(self, argObject):
        tosend = '42["message",' + json.JSONEncoder().encode(argObject) + ']'
        print ('Sending message: ' + tosend)
        self.ws.send(tosend)

    def on_ping(self, ws, ping):
        pass
        #print('Ping:' + str(ping))
    def on_pong(self, ws, pong):
        pass
        #print('EtherDelta WebSocket API replied to our ping with a pong:' + str(pong))
    def on_error(self, ws, err):
        pass
        #print(err)

class ForkDeltaClient(Client):
    def __init__(self):
        self.websocket_url = 'wss://api.forkdelta.com/socket.io/?EIO=3&transport=websocket'
        self.bootstrap()
