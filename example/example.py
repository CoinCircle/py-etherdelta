import etherdelta

account = '0x85E4B84D784eE9eEB7489F0B0c66B343AF2a0BE5'
client = etherdelta.Client()
balance = client.get_eth_balance(account)
print(balance)
