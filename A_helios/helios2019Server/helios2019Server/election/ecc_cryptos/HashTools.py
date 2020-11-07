from Crypto.Hash import SHA256
from Crypto.Math.Numbers import *


class CryptoHash(object):
    """
      生成一个强密码学哈希函数
      get_hash依据是离散对数的强hash
    """

    @staticmethod
    def get_hash_ecc(message_point, order):
        bytes_list = message_point.x.to_bytes() + message_point.y.to_bytes()
        ha = SHA256.new()
        r = Integer.from_bytes(ha.new(bytes_list).digest()).__mod__(order)
        return message_point * r

    @staticmethod
    def get_hash_ecc_r(message_point, order):
        bytes_list = message_point.x.to_bytes() + message_point.y.to_bytes()
        ha = SHA256.new()
        r = Integer.from_bytes(ha.new(bytes_list).digest()).__mod__(order)
        return r
