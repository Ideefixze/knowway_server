import hashlib

def hash(something):
    h = hashlib.sha256()
    h.update(str.encode(something))
    return h.hexdigest()
