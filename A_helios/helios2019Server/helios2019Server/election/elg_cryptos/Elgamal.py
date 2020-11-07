from Crypto import Random
from Crypto.PublicKey import ElGamal
from .HashTools import CryptoHash
from .Utils import str_to_message
# from HashTools import CryptoHash
# from Utils import str_to_message


class GenerateParameters(object):
    """
      生成Elgamal相关的参数
    """

    def __init__(self, length):
        self.key = ElGamal.generate(length, Random.new().read)
        self.p = self.key.p
        self.g = self.key.g
        self.h = None
        self.x = None

    def get_public_key(self):
        """
          根据私钥生成公钥
          获取服务器需要对外公布的信息：模p、生成元g以及根据私钥算出来的公钥y
        """
        self.h = pow(self.g, self.x, self.p)
        dic = {'g': str(self.g), 'h': str(self.h), 'p': str(self.p)}
        return str(dic)

    def set_private_key(self, key, salt):
        """
          根据用户口令加盐生成私钥
        """
        # salt = 'secret'
        # self.x = Utils.do_hmac(key, salt)
        mes = str_to_message(key + salt)
        self.x = CryptoHash.get_hash(mes, self.p)

    @staticmethod
    def get_private_key(key, salt, p):
        """
        获取私钥
        """
        # salt = 'secret'
        mes = str_to_message(key + salt)
        # return Utils.do_hmac(key, salt)
        return CryptoHash.get_hash(mes, p)
