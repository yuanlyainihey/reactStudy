from Crypto.Hash import SHA256
from Crypto.Random import random
from Crypto.Util import number
from .Utils import long_to_bytes, bytes_to_long, message_to_str, str_to_message
from .Elgamal import GenerateParameters
from .HashTools import CryptoHash
# from Crypto.Math.Numbers import *
# from Utils import long_to_bytes, bytes_to_long, message_to_str, str_to_message
# from Elgamal import GenerateParameters
# from HashTools import CryptoHash
import json


class MixTools(object):
    """
    混洗以及验证时需要的函数
    """
    @staticmethod
    def generate_random_sequence(pi, length):
        """
        根据输入参数 生成随机打乱后的新坐标
        """
        verify_list = []
        new_sequence = []
        h = SHA256.new()
        for i in range(length):
            verify_list.append(-1)
        for i in range(length):
            h.new(long_to_bytes(pi) + long_to_bytes(i))
            byte = h.digest()
            m = bytes_to_long(byte) % length
            if verify_list[m] == -1:
                new_sequence.append(m)
                verify_list[m] = 0
            else:
                m = (m+1) % length
                while verify_list[m] != -1:
                    m = (m+1) % length
                new_sequence.append(m)
                verify_list[m] = 0
        del h
        return new_sequence

    @staticmethod
    def random_sample(p):
        """
        随机生成参数pi用于置换函数
        """
        return random.randrange(2, p)


class MixNet(object):
    def __init__(self, p, g, key, salt, public_key, vote_g, vote_p, hash_g, hash_p, vote_num, selections):
        self.p = p
        self.g = g
        self.private_key = GenerateParameters.get_private_key(
            key, salt, p)
        self.public_key = public_key
        self.vote_g = vote_g
        self.vote_p = vote_p
        self.hash_g = hash_g
        self.hash_p = hash_p
        self.vote_num = vote_num
        self.selections = selections
        self._PI = MixTools.random_sample(self.p)
        self.result = {}

    def get_plain_text(self):
        """
          解密并打乱选票
        """
        message = []
        question_len = len(self.vote_g[0])
        for i in range(self.vote_num):
            message.append(["0" for j in range(question_len)])

        position = MixTools.generate_random_sequence(self._PI, self.vote_num)
        # print(position)
        for i in range(self.vote_num):
            for j in range(question_len):
                m = self.vote_p[i][j] * number.inverse(
                    pow(self.vote_g[i][j], self.private_key, self.p), self.p) % self.p
                hm = self.hash_p[i][j] * number.inverse(
                    pow(self.hash_g[i][j], self.private_key, self.p), self.p) % self.p
                hm_backup = CryptoHash.get_hash(m, self.p)
                if hm == hm_backup:
                    message[position[i]][j] = message_to_str(m)
                else:
                    message[position[i]][j] = 'error vote'
        self.result = MixNet.count_votes(message)
        return message

    @staticmethod
    def count_votes(message):
        """
          统计选票
        """
        result = {}
        for item in message:
            for each in item:
                if each in result:
                    result[each] = result[each] + 1
                else:
                    result[each] = 1
        return result

    @staticmethod
    def prod(list_prod, p):
        """
        大数连乘
        """
        v = 1
        for i in range(len(list_prod)):
            v = v * list_prod[i] % p
        return v

    def verify_file_generate(self, file_path):
        """
          生成证明文件，问题数量对应着不同的证明参数
        """
        question_len = len(self.vote_g[0])
        verify_params = [{} for j in range(question_len)]
        for i in range(question_len):
            s = MixTools.random_sample(self.p)
            u = pow(self.g, s, self.p)
            hash_g_question = []
            for j in range(len(self.hash_g)):
                hash_g_question.append(self.hash_g[j][i])
            hash_p_question = []
            for j in range(len(self.hash_p)):
                hash_p_question.append(self.hash_p[j][i])
            v = pow((MixNet.prod(hash_g_question, self.p)) % self.p, s, self.p)
            z = pow((MixNet.prod(hash_g_question, self.p)) %
                    self.p, self.private_key, self.p)
            verify_params[i]['e'] = str(CryptoHash.get_hash(
                (self.public_key+z+u+v) % self.p, self.p))
            verify_params[i]['f'] = str(
                s - int(verify_params[i]['e'])*self.private_key)
            verify_params[i]['c'] = str(
                MixNet.prod(hash_g_question, self.p) % self.p)
            verify_params[i]['d'] = str(
                MixNet.prod(hash_p_question, self.p) % self.p)
        # 写入文件
        verify_file = []
        for i in range(len(verify_params)):
            verify_file.append({'question'+str(i+1): verify_params[i]})
        with open(file_path, 'w') as f:
            json.dump(verify_file, f)

    @staticmethod
    def verify(g, y, h, d, m, e, f, p, index):
        """
          验证程序:
          g:生成元g
          y:公钥
          h:证明文件中的c
          d:证明文件中的d
          m:bbs上提供的投票集合
          e:证明文件中的e
          f:证明文件中的f
          p:modp
          index:需要验证第几个问题
        """
        g_f = number.inverse(pow(g, -f, p), p)
        a = (g_f*pow(y, e, p)) % p
        hm = []
        for i in range(len(m)):
            hm.append(CryptoHash.get_hash(
                str_to_message(m[i][index]), p))
        z = d * number.inverse(MixNet.prod(hm, p), p) % p
        h_f = number.inverse(pow(h, -f, p), p)
        b = (h_f*pow(z, e, p)) % p
        return e == CryptoHash.get_hash((y+z+a+b) % p, p)
