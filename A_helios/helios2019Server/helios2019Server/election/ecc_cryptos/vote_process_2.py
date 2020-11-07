from Crypto.Math.Numbers import *
from Crypto.PublicKey import ECC
from Crypto import Random
from EccGenerate import GenerateParameters
from Utils import get_point_dic, string_to_point, str_to_bytes
from HashTools import CryptoHash
from EccCrypto import MixNet
import json
import datetime
import random as random_int

key = GenerateParameters()
key.set_private_key('zhunny', 'salt')
# public_key
public_key = eval(key.get_public_key())
# print(public_key)

# 为每个问题的选项生成对应的点
"""
问题1：我好看么
好看/不好看
问题2：你心中的主席是
张三/李四
"""
order = key.order
G = key.G
selections = [{'好看': string_to_point('好看', get_point_dic('好看')), '不好看': string_to_point('不好看', get_point_dic('不好看'))}, {
    '张三': string_to_point('张三', get_point_dic('张三')), '李四': string_to_point('李四', get_point_dic('李四'))}]

K = ECC.EccPoint(Integer(int(public_key['x'])), Integer(int(public_key['y'])))


def random_result(votes, num, G, K, order):
    vote_c1 = []
    vote_c2 = []
    hash_c1 = []
    hash_c2 = []
    for i in range(num):
        vote_c1_i = []
        vote_c2_i = []
        hash_c1_i = []
        hash_c2_i = []
        for j in range(len(votes)):
            len_j = len(votes[j])
            ran = random_int.randint(0, len_j-1)
            m_str = votes[j][ran]
            m = string_to_point(m_str, get_point_dic(m_str))
            hm = CryptoHash.get_hash_ecc(m, order)
            r = Integer.random_range(
                min_inclusive=1, max_exclusive=order, randfunc=Random.new().read)
            s = Integer.random_range(
                min_inclusive=1, max_exclusive=order, randfunc=Random.new().read)
            vote_c1_i.append(m+r*K)
            vote_c2_i.append(r*G)
            hash_c1_i.append(hm+s*K)
            hash_c2_i.append(s*G)
        vote_c1.append(vote_c1_i)
        vote_c2.append(vote_c2_i)
        hash_c1.append(hash_c1_i)
        hash_c2.append(hash_c2_i)
    return [vote_c1, vote_c2, hash_c1, hash_c2]


vote_res = random_result([['好看', '不好看'], ['张三', '李四']], 10000, G, K, order)

# 选票为['好看'，'张三']['不好看'，'李四']
# m_1 = string_to_point('好看', get_point_dic('好看'))
# hm_1 = CryptoHash.get_hash_ecc(m_1, order)
# m_2 = string_to_point('张三', get_point_dic('张三'))
# hm_2 = CryptoHash.get_hash_ecc(m_2, order)
# m_3 = string_to_point('不好看', get_point_dic('不好看'))
# hm_3 = CryptoHash.get_hash_ecc(m_3, order)
# m_4 = string_to_point('李四', get_point_dic('李四'))
# hm_4 = CryptoHash.get_hash_ecc(m_4, order)
# 随机生成r
# r_1 = Integer.random_range(
#     min_inclusive=1, max_exclusive=order, randfunc=Random.new().read)
# s_1 = Integer.random_range(
#     min_inclusive=1, max_exclusive=order, randfunc=Random.new().read)
# r_2 = Integer.random_range(
#     min_inclusive=1, max_exclusive=order, randfunc=Random.new().read)
# s_2 = Integer.random_range(
#     min_inclusive=1, max_exclusive=order, randfunc=Random.new().read)
# r_3 = Integer.random_range(
#     min_inclusive=1, max_exclusive=order, randfunc=Random.new().read)
# s_3 = Integer.random_range(
#     min_inclusive=1, max_exclusive=order, randfunc=Random.new().read)
# r_4 = Integer.random_range(
#     min_inclusive=1, max_exclusive=order, randfunc=Random.new().read)
# s_4 = Integer.random_range(
#     min_inclusive=1, max_exclusive=order, randfunc=Random.new().read)
# 加密C1=M+rK；C2=rG

# vote_c1 = [[m_1+r_1*K, m_2+r_2*K], [m_3+r_3*K, m_4+r_4*K]]
# vote_c2 = [[r_1*G, r_2*G], [r_3*G, r_4*G]]
# hash_c1 = [[hm_1+s_1*K, hm_2+s_2*K], [hm_3+s_3*K, hm_4+s_4*K]]
# hash_c2 = [[s_1*G, s_2*G], [s_3*G, s_4*G]]

starttime = datetime.datetime.now()
net = MixNet(order, G, 'zhunny', 'salt', K, vote_res[0],
             vote_res[1], vote_res[2], vote_res[3], 10000, selections)

message = net.get_plain_text()
# print(message)
print(net.result)
endtime = datetime.datetime.now()
print((endtime - starttime))

starttime2 = datetime.datetime.now()
net.verify_file_generate('text.json')
endtime2 = datetime.datetime.now()
print((endtime2 - starttime2))

with open("text.json", 'r') as load_f:
    load_dict = json.load(load_f)

starttime3 = datetime.datetime.now()
c_point = eval(load_dict[1]['question2']['c'])
c = ECC.EccPoint(c_point['x'], c_point['y'])
d_point = eval(load_dict[1]['question2']['d'])
d = ECC.EccPoint(d_point['x'], d_point['y'])
e = Integer(int(load_dict[1]['question2']['e']))
f = Integer(int(load_dict[1]['question2']['f']))
res = MixNet.verify(G, K, c, d, message, e, f, order, 1)
print(res)
endtime3 = datetime.datetime.now()
print((endtime3 - starttime3))
