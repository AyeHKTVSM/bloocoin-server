import mongo  # Ensure correct import as per your MongoDB driver
import command

class CheckAddr(command.Command):
    """
    {"cmd":"check_addr", "addr":"addr"}
    """
    required = ['addr']

    def handle(self, *args, **kwargs):
        addr = self.data['addr']
        try:
            amount = mongo.db.coins.count_documents({'addr': addr})
            self.success({"addr": addr, "amount": amount})
        except Exception as e:  # Catch specific exceptions for better error handling
            self.error(f"Error: {e}")
            return
