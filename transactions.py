import json
import mongo
import command

class Transactions(command.Command):
    """ Gives the user a list of their transactions,
        allowing clients to display changes of coins
        to and from the given address.

        fingerprint: {"cmd": "transactions", "addr": _, "pwd": _}
    """
    required = ['addr', 'pwd']

    def handle(self, *args, **kwargs):
        addr = self.data['addr']
        pwd = self.data['pwd']
        user = mongo.db.addresses.find_one({"addr": addr, "pwd": pwd})
        
        if not user:
            self.error("Your address or password was invalid")
            return
        
        payload = {"transactions": []}
        sender_transactions = mongo.db.transactions.find({"from": addr})
        receiver_transactions = mongo.db.transactions.find({"to": addr})
        
        for t in sender_transactions:
            payload['transactions'].append({
                "from": addr,
                "to": t['to'],
                "amount": t['amount']
            })
        
        for t in receiver_transactions:
            payload['transactions'].append({
                "from": t['from'],
                "to": addr,
                "amount": t['amount']
            })
        
        self.success(payload)
