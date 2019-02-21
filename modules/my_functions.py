import hashlib
import random, string


def id_generator(size = 12, chars = string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def hash_password(password):
    return hashlib.md5(bytes(password, encoding = 'utf8')).hexdigest()
