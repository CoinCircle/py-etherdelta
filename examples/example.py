import etherdelta

client = etherdelta.Client()
account = "0x85E4B84D784eE9eEB7489F0B0c66B343AF2a0BE5"

client = etherdelta.Client()
bal = client.get_eth_balance(account)
print(bal)
