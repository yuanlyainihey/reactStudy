from Crypto.Hash import SHA256
from Crypto import Random
from Crypto.Math.Numbers import *
from Crypto.PublicKey import ECC
from EccGenerate import GenerateParameters
from Utils import point_to_string, get_point_dic, string_to_point
from HashTools import CryptoHash
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
            h.new(pi.to_bytes() + i.to_bytes(8, byteorder="big"))
            byte = h.digest()
            # 这种方法可以淘汰了，python3功能已经可以不用这个库了
            m = int(Integer.__mod__(Integer.from_bytes(byte), Integer(length)))
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
    def random_sample(order):
        """
        随机生成参数pi用于置换函数
        """
        return Integer.random_range(min_inclusive=1, max_exclusive=order, randfunc=Random.new().read)


class MixNet(object):
    def __init__(self, order, G, key, salt, public_key, vote_c1, vote_c2, hash_c1, hash_c2, vote_num, selections):
        self.order = order
        self.G = G
        self.k = GenerateParameters.get_private_key(key, salt, order)
        self.public_key = public_key
        self.vote_c1 = vote_c1
        self.vote_c2 = vote_c2
        self.hash_c1 = hash_c1
        self.hash_c2 = hash_c2
        self.vote_num = vote_num
        self.selections = selections
        self._PI = MixTools.random_sample(self.order)
        self.result = {}

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
    def prod(list_prod):
        """
        在椭圆曲线中为连加
        """
        v = list_prod[0]
        for i in range(1, len(list_prod)):
            v = v + list_prod[i]
        return v

    def get_plain_text(self):
        """
          解密并打乱选票
          M = C1-kC2
        """
        message = []
        question_len = len(self.vote_c1[0])
        for i in range(self.vote_num):
            message.append(["0" for j in range(question_len)])
        position = MixTools.generate_random_sequence(
            self._PI, self.vote_num)
        for i in range(self.vote_num):
            for j in range(question_len):
                m = self.vote_c1[i][j] + (-(self.k * self.vote_c2[i][j]))
                hm = self.hash_c1[i][j] + (-(self.k * self.hash_c2[i][j]))
                hm_backup = CryptoHash.get_hash_ecc(m, self.order)
                if hm == hm_backup:
                    message[position[i]][j] = point_to_string(
                        m, self.selections[j])
                else:
                    message[position[i]][j] = 'error vote'

        # hm_test_prod = []
        # for i in range(self.vote_num):
        #     hm_test_prod.append(
        #         self.hash_c1[i][1] + (-(self.k * self.hash_c2[i][1])))
        # for i in range(len(hm_test_prod)):
        #     print(hm_test_prod[i].x, ':', hm_test_prod[i].y)
        # hm_test = MixNet.prod(hm_test_prod)
        # print('hm_test:')
        # print(hm_test.x)
        # print(hm_test.y)

        self.result = MixNet.count_votes(message)
        return message

    def verify_file_generate(self, file_path):
        """
          生成证明文件，问题数量对应着不同的证明参数
        """
        question_len = len(self.vote_c1[0])
        verify_params = [{} for j in range(question_len)]
        for i in range(question_len):
            s = MixTools.random_sample(self.order)
            u = s * self.G
            # print('u:')
            # print(u.x)
            # print(u.y)
            hash_c2_question = []
            for j in range(len(self.hash_c2)):
                hash_c2_question.append(self.hash_c2[j][i])
            hash_c1_question = []
            for j in range(len(self.hash_c1)):
                hash_c1_question.append(self.hash_c1[j][i])
            v = s * MixNet.prod(hash_c2_question)
            # print('v:')
            # print(v.x)
            # print(v.y)
            z = self.k * MixNet.prod(hash_c2_question)
            # print('z:')
            # print(z.x)
            # print(z.y)
            e = CryptoHash.get_hash_ecc_r(
                (self.public_key + z + u + v), self.order)
            verify_params[i]['e'] = str(e)
            f = s - e*self.k
            verify_params[i]['f'] = str(f)
            c = MixNet.prod(hash_c2_question)
            verify_params[i]['c'] = str({'x': c.x, 'y': c.y})
            d = MixNet.prod(hash_c1_question)
            verify_params[i]['d'] = str({'x': d.x, 'y': d.y})
        # 写入文件
        verify_file = []
        for i in range(len(verify_params)):
            verify_file.append({'question'+str(i+1): verify_params[i]})
        with open(file_path, 'w') as f:
            json.dump(verify_file, f)

    @staticmethod
    def verify(G, K, c, d, m, e, f, order, index):
        """
          验证程序:
          G:基点G
          K:公钥
          c:证明文件中的c
          d:证明文件中的d
          m:bbs上提供的投票集合
          e:证明文件中的e
          f:证明文件中的f
          p:椭圆曲线的阶
          index:需要验证第几个问题
        """
        f_reverse = Integer.__mod__(Integer(-int(f)), order)
        a = -(f_reverse * G) + e * K
        # print('a:')
        # print(a.x)
        # print(a.y)
        hm = []
        for i in range(len(m)):
            hm.append(CryptoHash.get_hash_ecc(string_to_point(
                m[i][index], get_point_dic(m[i][index])), order))
        # for i in range(len(hm)):
        #     print(hm[i].x, ':', hm[i].y)
        z = d + (-MixNet.prod(hm))
        # hm_prod = MixNet.prod(hm)
        # print('hm_prod:')
        # print(hm_prod.x)
        # print(hm_prod.y)
        # print('z:')
        # print(z.x)
        # print(z.y)
        b = -(f_reverse * c) + e * z
        # print('b:')
        # print(b.x)
        # print(b.y)
        return e == CryptoHash.get_hash_ecc_r((K + z + a + b), order)
