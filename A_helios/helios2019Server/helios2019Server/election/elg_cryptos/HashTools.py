from Crypto.Hash import SHA512, SHA256
from Crypto.Math.Numbers import *
from .Utils import long_to_bytes, bytes_to_long, str_to_bytes
# from Utils import long_to_bytes, bytes_to_long, str_to_bytes


class CryptoHash(object):
    """
      生成一个强密码学哈希函数
      get_hash依据是离散对数的强hash
    """
    @staticmethod
    def get_hash(message_num, p):
        """
          将输入分成两段，分别调用SHA512，获得一个1024bit的整数n。
          令 n_1 = n mod p，令n_2 = (n_1 ** 2) mod p，则n_2就是G中的一个随机元素。最后令H的输出为 。
        """
        p = int(p)
        message_bytes = long_to_bytes(message_num)
        h = SHA512.new()
        hash_bytes = h.new(message_bytes[0:int(len(message_bytes)/2)]).digest()
        hash_bytes += h.new(message_bytes[int(len(message_bytes)/2)
                            :len(message_bytes)]).digest()
        hash_num = bytes_to_long(hash_bytes) % p
        return pow(hash_num, 2, p)

    # @staticmethod
    # def get_hash(message_num, p):
    #     """
    #       将输入分成两段，分别调用SHA512，获得一个1024bit的整数n。
    #       令 n_1 = n mod p，令n_2 = (n_1 ** 2) mod p，则n_2就是G中的一个随机元素。最后令H的输出为 。
    #     """
    #     bytes_list = message_num.to_bytes()
    #     h = SHA512.new()
    #     integer_bytes = h.new(bytes_list[0:int(len(bytes_list)/2)]).digest()
    #     integer_bytes += h.new(
    #         bytes_list[int(len(bytes_list)/2):len(bytes_list)]).digest()
    #     integer = Integer.from_bytes(integer_bytes).__mod__(p)
    #     return pow(integer, 2).__mod__(p)

    @staticmethod
    def get_hash_ecc(message_point, p):
        bytes_list = long_to_bytes(message_point.x) + \
            long_to_bytes(message_point.y)
        h = SHA256.new()
        r = bytes_to_long(h.new(bytes_list).digest()) % p
        return message_point * r


class SelectionHash(object):
    """
      用于签名选项的hash函数
    """

    def __init__(self, length):
        self.length = length

    def get_hash(self, selection):
        if self.length > 300:
            ha = SHA512.new()
        else:
            ha = SHA256.new()
        ha.update(str_to_bytes(selection))
        return str(bytes_to_long(ha.digest()))
