import hashlib

def hash(value: str) -> str:
    hash_obj = hashlib.sha3_256(value.encode())
    return hash_obj.hexdigest()