import random


def random_string(length=20, alphabet=None):
    """
    随机生成字符串
    """
    ALPHABET = alphabet or 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    salt = ''
    for i in range(length):
        salt += random.choice(ALPHABET)

    return salt
