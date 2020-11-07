from Crypto.Math.Numbers import *
from Crypto.PublicKey import ECC
from Crypto.Hash import SHA256
from Utils import string_to_point, str_to_bytes


class GenerateParameters(object):
    """
      生成ECC相关的参数
    """

    def __init__(self):
        """
        G是基点
        order是阶
        k是私钥
        point是公钥
        """
        self.G = ECC._curves['P-256'].G.copy()
        self.order = ECC._curves['P-256'].order
        self.k = None
        self.point = None

    def get_public_key(self):
        """
          根据私钥生成公钥
          获取服务器需要对外公布的信息：模p、生成元g以及根据私钥算出来的公钥y
        """
        self.point = self.k*self.G
        dic = {'x': str(self.point.x), 'y': str(
            self.point.y), 'order': str(self.order), 'G.x': str(self.G.x), 'G.y': str(self.G.y)}
        return str(dic)

    def set_private_key(self, key, salt):
        """
          根据用户口令加盐生成私钥
        """
        ha = SHA256.new()
        ha.update(str_to_bytes(key+salt))
        input_bytes = ha.digest()
        input_integer = Integer.__mod__(
            Integer.from_bytes(input_bytes), self.order)
        self.k = input_integer

    @staticmethod
    def get_private_key(key, salt, order):
        """
        获取私钥
        """
        ha = SHA256.new()
        ha.update(str_to_bytes(key+salt))
        input_bytes = ha.digest()
        input_integer = Integer.__mod__(Integer.from_bytes(input_bytes), order)
        return input_integer
