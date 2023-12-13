import command
import json
import mongo

class TotalCoins(command.Command):
    """ 
    {"cmd":"total_coins"}
    """
    required = []

    def handle(self):
        total_coins = mongo.db.coins.count_documents({})
        self.success({"amount": total_coins})
