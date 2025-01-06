import uuid
import random
import string

def generate_random_uuid():
    return str(uuid.uuid4())

def generate_random_code():
    return str(uuid.uuid4().int)[:6]

def generate_random_string(length: int):
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))

def generate_random_number(length: int):
    return "".join(random.choices(string.digits, k=length))

def generate_random_hex(length: int):
    return "".join(random.choices(string.hexdigits, k=length))