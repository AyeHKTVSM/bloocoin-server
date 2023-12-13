import mongo  # Ensure correct import as per your MongoDB driver
import command

class MyCoins(command.Command):
    """ Allows users to check the amount of coins
        under their account.

        fingerprint: {"cmd": "my_coins", "addr": _, "pwd": _}
    """
    required = ['addr', 'pwd']

    def handle(self, *args, **kwargs):
        addr = self.data['addr']
        pwd = self.data['pwd']
        
        # Assuming mongo.db is your MongoDB connection
        if mongo.db.addresses.find_one({"addr": addr, "pwd": pwd}):
            coins_count = mongo.db.coins.count_documents({"addr": addr})
            self.success({"amount": coins_count})
        else:
            self.error("Your address or password was invalid")
