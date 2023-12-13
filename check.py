import mongo  # Ensure correct import as per your MongoDB driver
from get_coin import difficulty
from hashlib import sha512
import command

class Check(command.Command):
    """ Allows miners to send work to the
        server for submission. If the given
        hashes are valid, it will be added to
        the given account address.

        fingerprint:
         {"cmd": "check", "winning_string": _, "winning_hash": _, "addr": _}
    """
    required = ['winning_string', 'winning_hash', 'addr']

    def handle(self, *args, **kwargs):
        addr = self.data['addr']
        if not mongo.db.addresses.find_one({"addr": addr}):
            self.error("Your address does not exist")
            return

        winning_string = self.data['winning_string']
        winning_hash = self.data['winning_hash']

        is_same_hash = winning_hash == sha512(winning_string.encode()).hexdigest()
        coin_exists = mongo.db.coins.find_one({"hash": winning_hash})
        correct_diff = winning_hash.startswith(difficulty() * "0")

        try:
            if is_same_hash and not coin_exists and correct_diff:
                mongo.db.coins.insert_one({"hash": winning_hash, "addr": addr})
                self.success({"hash": winning_hash})
            else:
                # Intentionally a bit vague, just so it's not infinitely easy
                self.error("Something went wrong")
        except Exception as e:
            self.error(f"Error: {e}")
