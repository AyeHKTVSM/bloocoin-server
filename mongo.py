import pymongo

# Only change for remote authentication
host = "your_remote_host"  # Replace with your remote host
port = 27017  # Replace with your remote port
username = "your_username"  # Replace with your username
password = "your_password"  # Replace with your password

client = pymongo.MongoClient(host, port, username=username, password=password)
db = client.bloocoin

# db.authenticate(username, password)  # Not required for recent versions of pymongo

# Perform operations using the 'db' object as needed
