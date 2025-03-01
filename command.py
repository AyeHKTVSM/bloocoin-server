import json
import hashlib

class Command(object):
    """ The base class for commands the clients can run.
        TBD (to be documented)
    """
    required = []

    def __init__(self, sock, data):
        self.sock = sock
        try:
            self.data = json.loads(data)
            pre_hashed = 'x-pre-hashed' in self.data
            if 'pwd' in self.data and not pre_hashed:
                self.data['pwd'] = hashlib.sha256(self.data['pwd'].encode()).hexdigest()
        except (ValueError, KeyError):
            self.error("Unable to decode request JSON")
            self._handle = False
            return
        missing = [k for k in self.required if k not in self.data]
        if missing:
            self.error("Missing keys: {}".format(', '.join(missing)))
            self._handle = False
            return
        # This is so we don't call handle() unless we should
        self._handle = True

    def handle(self, *args, **kwargs):
        self.error("This command has not been implemented correctly")

    def success(self, payload, message=None, close=True):
        self.sock.send(json.dumps({
            "success": True,
            "message": message,
            "payload": payload
        }).encode())
        if close:
            self.sock.close()

    def error(self, message, payload=None, close=True):
        self.sock.send(json.dumps({
            "success": False,
            "message": message,
            "payload": payload
        }).encode())
        if close:
            self.sock.close()
            
