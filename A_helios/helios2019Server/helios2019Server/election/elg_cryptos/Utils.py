import base64
from Crypto.Hash import HMAC, SHA256
from Crypto.PublicKey import ECC
# from Crypto.Math.Numbers import *
import random


def str_to_bytes(o_str):
    """
      字符串转字节串
    """
    return o_str.encode()


def bytes_to_str(o_bytes):
    """
      字节串转字符串
    """
    return o_bytes.decode()


def bytes_to_long(o_bytes):
    """
      字节串转整型
    """
    return int.from_bytes(o_bytes, 'big')


# def bytes_to_long(o_bytes):
#     """
#       字节串转整型
#     """
#     return Integer.from_bytes(o_bytes)


def long_to_bytes(o_int):
    """
      整型转字节串
    """
    nbytes, rem = divmod(o_int.bit_length(), 8)
    if rem:
        nbytes += 1
    return o_int.to_bytes(nbytes, 'big')

# def long_to_bytes(o_int):
#     """
#       整型转字节串
#     """
#     return o_int.to_bytes()


def do_hmac(key, salt):
    """
    口令加盐之后用sha256生成私钥
    """
    b_key = str_to_bytes(key)
    b_salt = str_to_bytes(salt)
    mac = HMAC.new(b_key, b_salt, digestmod=SHA256)
    return bytes_to_long(mac.digest())


def str_to_message(input_string):  # the length of string must less than 32 byte
    """
    消息由str转换为一个长整型
    """
    return bytes_to_long(base64.b64encode(str_to_bytes(input_string)))


def message_to_str(message_num):  # input must be a integer of message
    """
    消息由长整型转换为一个str
    """
    return bytes_to_str(base64.b64decode(long_to_bytes(message_num)))

# the length of string must less than 32 byte


def string_to_point(input_string, point_dict):
    """
    消息由str转换为一个椭圆曲线上的点
    """
    return point_dict[input_string]


# input must be a ECC point of message
def point_to_string(message_point, point_dict):
    """
    消息由一个椭圆曲线上的点转换为str
    """
    for key in point_dict.keys():
        if point_dict[key] == message_point:
            return key
    return "Not find!"


def random_string(length=20, alphabet=None):
    """
    随机生成字符串
    """
    ALPHABET = alphabet or 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    salt = ''
    for i in range(length):
        salt += random.choice(ALPHABET)

    return salt
