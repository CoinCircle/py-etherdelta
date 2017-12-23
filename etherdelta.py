import hashlib
import websocket
import _thread
import time
import json
import random
import sys
import os
import web3
from twisted.internet import defer

from web3 import Web3, HTTPProvider
from operator import itemgetter
from collections import OrderedDict

# The functions below are used for our soliditySha256() function
from web3.utils.normalizers import abi_ens_resolver
from web3.utils.abi import map_abi_data
from eth_utils import add_0x_prefix, remove_0x_prefix
from web3.utils.encoding import hex_encode_abi_type

# etherdelta_2's contract address
addressEtherDelta = '0x8d12A197cB00D4747a1fe03395095ce2A5CC6819'
web3 = Web3(HTTPProvider('https://mainnet.infura.io/'))

class EtherDeltaClient:
    ws = None

    def __init__(self):
        token_abi = None
        with open(os.path.join(os.path.dirname(__file__), 'contracts/token.json'), 'r') as token_abi_definition:
            token_abi = json.load(token_abi_definition)
        self.token_abi = token_abi

        global addressEtherDelta
        addressEtherDelta = Web3.toChecksumAddress(addressEtherDelta)

        with open(os.path.join(os.path.dirname(__file__), 'contracts/etherdelta.json'), 'r') as abi_definition:
            abiEtherDelta = json.load(abi_definition)
        self.contractEtherDelta = web3.eth.contract(address=addressEtherDelta, abi=abiEtherDelta)

    def get_eth_balance(self, user):
        user = Web3.toChecksumAddress(user)
        balance = web3.eth.getBalance(user)
        return web3.fromWei(balance, 'ether')

    def get_token_balance(self, tokenAddr, user):
        tokenAddr = Web3.toChecksumAddress(tokenAddr)
        contractToken = web3.eth.contract(address=tokenAddr, abi=self.token_abi)
        user = Web3.toChecksumAddress(user)
        balance = contractToken.call().balanceOf(user)
        return web3.fromWei(balance, 'ether')

    def get_etherdelta_balance(self, user):
        user = Web3.toChecksumAddress(user)
        balance = self.contractEtherDelta.call().balanceOf(token="0x0000000000000000000000000000000000000000", user=user)
        return web3.fromWei(balance, 'ether')

    def get_token_address(self, currency):
        ticker = self.get_ticker(currency)
        tokenAddr = ticker.result["tokenAddr"]
        return tokenAddr

    def get_orders(self, currency):
        d = defer.Deferred()
        def callback(msg):
            self.ws.close()
            result = msg["orders"]
            d.callback(result)

        tokenAddr = self.get_token_address(currency)
        emitMessage = '42["getMarket",{"token":"' + tokenAddr + '","user":""}]'
        self.listen_once_and_close("getMarket", emitMessage, "market", callback)
        return d

    def get_order(self, currency, uuid):
        d = defer.Deferred()
        def callback(msg):
            self.ws.close()
            order = None
            orders = msg["orders"]

            for o in orders["sells"]:
                if o["id"] == uuid:
                    order = o
            for o in orders["buys"]:
                if o["id"] == uuid:
                    order = o

            d.callback(order)

        tokenAddr = self.get_token_address(currency)
        emitMessage = '42["getMarket",{"token":"' + tokenAddr + '","user":""}]'
        self.listen_once_and_close("getMarket", emitMessage, "market", callback)
        return d

    def get_sell_orderbook(self, currency):
        d = defer.Deferred()
        def callback(msg):
            self.ws.close()
            result = msg["orders"]["sells"]
            d.callback(result)

        tokenAddr = self.get_token_address(currency)
        emitMessage = '42["getMarket",{"token":"' + tokenAddr + '","user":""}]'
        self.listen_once_and_close("getMarket", emitMessage, "market", callback)
        return d

    def get_buy_orderbook(self, currency):
        d = defer.Deferred()
        def callback(msg):
            self.ws.close()
            result = msg["orders"]["buys"]
            d.callback(result)

        tokenAddr = self.get_token_address(currency)
        emitMessage = '42["getMarket",{"token":"' + tokenAddr + '","user":""}]'
        self.listen_once_and_close("getMarket", emitMessage, "market", callback)
        return d

    def get_amount_filled(self, currency, orderId):
        order = self.get_order(currency, orderId)
        order = order.result

        if order == None:
            return None
        amountGet = int('{:.0f}'.format(float(order["amountGet"])))
        amountGive = int('{:.0f}'.format(float(order["amountGive"])))
        tokenGet = Web3.toChecksumAddress(order["tokenGet"])
        tokenGive = Web3.toChecksumAddress(order["tokenGive"])
        expires = int(order["expires"])
        nonce = int(order["nonce"])
        user = Web3.toChecksumAddress(order["user"])
        v = int(order["v"])
        r = Web3.toBytes(hexstr=order["r"])
        s = Web3.toBytes(hexstr=order["s"])

        amount_filled = self.contractEtherDelta.call().amountFilled(tokenGet, amountGet, tokenGive, amountGive, expires, nonce, user, v, r, s)
        return amount_filled

    def get_available_volume(self, currency, orderId):
        order = self.get_order(currency, orderId)
        order = order.result

        if order == None:
            return None
        amountGet = int('{:.0f}'.format(float(order["amountGet"])))
        amountGive = int('{:.0f}'.format(float(order["amountGive"])))
        tokenGet = Web3.toChecksumAddress(order["tokenGet"])
        tokenGive = Web3.toChecksumAddress(order["tokenGive"])
        expires = int(order["expires"])
        nonce = int(order["nonce"])
        user = Web3.toChecksumAddress(order["user"])
        v = int(order["v"])
        r = Web3.toBytes(hexstr=order["r"])
        s = Web3.toBytes(hexstr=order["s"])

        available_volume = self.contractEtherDelta.call().availableVolume(tokenGet, amountGet, tokenGive, amountGive, expires, nonce, user, v, r, s)
        return available_volume

    def get_block_number(self):
        return web3.eth.blockNumber

    def create_order(self, side, expires, price, amount, token, user_wallet_private_key, randomseed = None):
        global addressEtherDelta, web3
        userAccount = web3.eth.account.privateKeyToAccount(user_wallet_private_key).address

        print("\nCreating '" + side + "' order for %.18f tokens @ %.18f ETH/token" % (amount, price))

        # Validate the input
        if len(user_wallet_private_key) != 64: raise ValueError('WARNING: user_wallet_private_key must be a hexadecimal string of 64 characters long')

        # Ensure good parameters
        token = Web3.toChecksumAddress(token)
        userAccount = Web3.toChecksumAddress(userAccount)
        user_wallet_private_key = Web3.toBytes(hexstr=user_wallet_private_key)

        # Build the order parameters
        amountBigNum = amount
        amountBaseBigNum = float(amount) * float(price)
        if randomseed != None: random.seed(randomseed)    # Seed the random number generator for unit testable results
        orderNonce = random.randint(0,10000000000)
        if side == 'sell':
            tokenGive = token
            tokenGet = '0x0000000000000000000000000000000000000000'
            amountGet = web3.toWei(amountBaseBigNum, 'ether')
            amountGive = web3.toWei(amountBigNum, 'ether')
        elif side == 'buy':
            tokenGive = '0x0000000000000000000000000000000000000000'
            tokenGet = token
            amountGet = web3.toWei(amountBigNum, 'ether')
            amountGive = web3.toWei(amountBaseBigNum, 'ether')
        else:
            print("WARNING: invalid order side, no action taken: " + str(side))

        # Serialize (according to ABI) and sha256 hash the order's parameters
        hashhex = self.soliditySha256(
            ['address', 'address', 'uint256', 'address', 'uint256', 'uint256', 'uint256'],
            [addressEtherDelta, tokenGet, amountGet, tokenGive, amountGive, expires, orderNonce]
        )
        # Sign the hash of the order's parameters with our private key (this also addes the "Ethereum Signed Message" header)
        signresult = web3.eth.account.sign(message_hexstr=hashhex, private_key=user_wallet_private_key)
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
        d = defer.Deferred()
        def callback(msg):
            self.ws.close()

            d.callback(msg)

        emitMessage = '42["message",' + json.JSONEncoder().encode(order) + ']'
        self.listen_once_and_close("message", emitMessage, "messageResult", callback)
        return d

    def trade(self, order, etherAmount, user_wallet_private_key=''):
        global web3, addressEtherDelta
        userAccount = web3.eth.account.privateKeyToAccount(user_wallet_private_key).address

        # Transaction info
        maxGas = 250000
        gasPriceWei = 1000000000    # 1 Gwei
        if order['tokenGive'] == '0x0000000000000000000000000000000000000000':
            ordertype = 'buy'    # it's a buy order so we are selling tokens for ETH
            amount = etherAmount / float(order['price'])
        else:
            ordertype = 'sell'   # it's a sell order so we are buying tokens for ETH
            amount = etherAmount
        amount_in_wei = web3.toWei(amount, 'ether')

        print("\nTrading " + str(etherAmount) + " ETH of tokens (" + str(amount) + " tokens) against this " + ordertype + " order: %.10f tokens @ %.10f ETH/token" % (float(order['ethAvailableVolume']), float(order['price'])))
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
            'r' : web3.toBytes(hexstr=order['r']),
            's' : web3.toBytes(hexstr=order['s']),
            'amount' : int(amount_in_wei),
        }

        # Bail if there's no private key
        if len(user_wallet_private_key) != 64: raise ValueError('WARNING: user_wallet_private_key must be a hexadecimal string of 64 characters long')

        # Build binary representation of the function call with arguments
        abidata = self.contractEtherDelta.encodeABI('trade', kwargs=kwargs)
        print("abidata: " + str(abidata))
        nonce = web3.eth.getTransactionCount(userAccount)
        # Override to have same as other transaction:
        #nonce = 53
        print("nonce: " + str(nonce))
        transaction = { 'to': addressEtherDelta, 'from': userAccount, 'gas': maxGas, 'gasPrice': gasPriceWei, 'data': abidata, 'nonce': nonce, 'chainId': 1}
        print(transaction)
        signed = web3.eth.account.signTransaction(transaction, user_wallet_private_key)
        print("signed: " + str(signed))
        result = web3.eth.sendRawTransaction(web3.toHex(signed.rawTransaction))
        print("Transaction returned: " + str(result))
        print("\nDone! You should see the transaction show up at https://etherscan.io/tx/" + web3.toHex(result))

    def cancel_order(self, order, user_wallet_private_key=''):
        global web3, addressEtherDelta
        userAccount = web3.eth.account.privateKeyToAccount(user_wallet_private_key).address

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
            'r' : web3.toBytes(hexstr=order['r']),
            's' : web3.toBytes(hexstr=order['s']),
        }

        # Bail if there's no private key
        if len(user_wallet_private_key) != 64: raise ValueError('WARNING: user_wallet_private_key must be a hexadecimal string of 64 characters long')

        # Build binary representation of the function call with arguments
        abidata = self.contractEtherDelta.encodeABI('cancelOrder', kwargs=kwargs)
        print("abidata: " + str(abidata))
        nonce = web3.eth.getTransactionCount(userAccount)
        # Override to have same as other transaction:
        #nonce = 53
        print("nonce: " + str(nonce))
        transaction = { 'to': addressEtherDelta, 'from': userAccount, 'gas': maxGas, 'gasPrice': gasPriceWei, 'data': abidata, 'nonce': nonce, 'chainId': 1}
        print(transaction)
        signed = web3.eth.account.signTransaction(transaction, user_wallet_private_key)
        print("signed: " + str(signed))
        result = web3.eth.sendRawTransaction(web3.toHex(signed.rawTransaction))
        print("Transaction returned: " + str(result))
        print("\nDone! You should see the transaction show up at https://etherscan.io/tx/" + web3.toHex(result))

    # This function is very similar to Web3.soliditySha3() but there is no Web3.soliditySha256() as per November 2017
    # It serializes values according to the ABI types defined in abi_types and hashes the result with sha256.
    def soliditySha256(self, abi_types, values):
        normalized_values = map_abi_data([abi_ens_resolver(Web3)], abi_types, values)
        #print(normalized_values)
        hex_string = add_0x_prefix(''.join(
            remove_0x_prefix(hex_encode_abi_type(abi_type, value))
            for abi_type, value
            in zip(abi_types, normalized_values)
        ))
        hash_object = hashlib.sha256(Web3.toBytes(hexstr=hex_string))
        return hash_object.hexdigest()

    def listen_once_and_close(self, emitTopic, emitMessage, eventTopic, callback):
        def on_message(ws, message):
            if message[:2] != "42":
                return
            j = json.loads(message[2:])
            if eventTopic in j:
                callback(j[1])

        def on_open(ws):
            self.ws.send(emitMessage)

        def on_close(ws):
            None

        self.ws = websocket.WebSocketApp(
            "wss://socket.etherdelta.com/socket.io/?transport=websocket",
            on_message = on_message,
              on_ping = self.on_ping,
              on_pong = self.on_pong,
              on_error = self.on_error,
              on_close = on_close)
        self.ws.on_open = on_open
        self.ws.run_forever(ping_interval=10)

    def get_ticker(self, ticker):
        d = defer.Deferred()
        def callback(msg):
            self.ws.close()
            result = msg["returnTicker"]["ETH_" + ticker]
            d.callback(result)

        emitMessage = '42["getMarket",{"token":"","user":""}]'
        self.listen_once_and_close("getMarket", emitMessage, "market", callback)
        return d

    def send_message(self, argObject):
        tosend = '42["message",' + json.JSONEncoder().encode(argObject) + ']'
        print ("Sending message: " + tosend)
        self.ws.send(tosend)

    def on_ping(self, ws, ping):
        print('Ping:' + str(ping))

    def on_pong(self, ws, pong):
        print('EtherDelta WebSocket API replied to our ping with a pong:' + str(pong))
