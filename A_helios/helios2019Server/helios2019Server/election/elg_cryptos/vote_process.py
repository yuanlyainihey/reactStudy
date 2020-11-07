# from Elgamal import GenerateParameters
# from HashTools import CryptoHash
# from ElgamalCrypto import MixNet
from .Elgamal import GenerateParameters
from .HashTools import CryptoHash
from .ElgamalCrypto import MixNet
from Crypto.Random import random
import random as random_int
import Utils
import json
import datetime
from Crypto.Math.Numbers import *


# 第一步：生成公钥等信息，并根据管理员提供的口令加盐生成
# 假设口令key的值为'zhunny'

# key = GenerateParameters(1024)
# key.set_private_key('zhunny')
# print(key.x)
# public_key要传给前端
# public_key = key.get_public_key()
# private_key = GenerateParameters.get_private_key('zhunny')
# print(private_key)

# 第二步: 根据p生成的强hash函数,前端后端都需要

# public_key_dict = eval(public_key)
# print(public_key_dict)


# 第三步，在此模拟前端的加密选票以及验证选票，假设选票可以write-in
# 因此前端时可随时增加心目中的候选人，因此hash函数前端也需要
# 问题选项的hash值是在后端准备好的
"""
问题1：我好看么
好看/不好看
问题2：你心中的主席是
张三/李四
"""
selections = [{'好看': Utils.str_to_message('好看'), '不好看': Utils.str_to_message('不好看')}, {
    '张三': Utils.str_to_message('张三'), '李四': Utils.str_to_message('李四')}]

# print(selections)

"""
加密选票
x:74146282434781760803021138873562457892284862363537360816234278379335524312153
g:42917890429530522137248457792174856916018365580355432917171346924112335523001
h:28667631733616517079054372746734964007587670207925384154814247841543875703721
p:59627112464263997180826043902311363945324718046120299595291811302281049902143
第一张选票:[好看:109768664229044656864348494342599658807413167749721707643427985388627804784075，
          张三:13350487970053528139526382157613951754684246801943953388572231538040876769999]
第二张选票:[不好看:97284078109122329152791998189728155795807683774896757156508015839365113476052，
          李四:58142184244210636460650249765194385113208320899491914088413785076635797277096]
"""

g = int('23462756022781219063177742528105152613107380490299013411060646603133126955246197852245833155759325687847562173551560012558646525195544682276257790652002725402489307514242430737797144631838841538207032778241998258085200027722378228789087396529202346540892311046463093333540040250137450549913814948647551538696')
h = int('80411125422987174979000660364697096248049267994140719668019407280795786364451524527081886432644376501653858433978496064086706792769376641533736131798265840592256974419918497554739241365736786244788320855388920789334931854142302933706065812465416433621004591738843249860482585155297143318756700970693779150093')
p = int('92470546430388686191097347151041999415251362259186034602375112690908573542186277704568047911263475288613908115490318989245406281092315045273079184611763579841000950339650348180275123044886906845389434249060777625583529085186780980582525396794766987475243240321492700180109165656597839707580185195074454651763')
x = int('42274486158269146732967015925777091278663592956586120471756883555562905198754441852104673240013485124733148123732549089572450163440852784073519750111791118170648281356805946669992120094544794880487884278686496420611628343828430299635263121635297879966986387168399759504673645922254800878767784399632965839434')
# print(x)

# votes : [['好看', '不好看'], ['张三', '李四']]


def random_result(votes, num, g, h, p):
    vote_g = []
    vote_p = []
    hash_g = []
    hash_p = []
    for i in range(num):
        vote_g_i = []
        vote_p_i = []
        hash_g_i = []
        hash_p_i = []
        for j in range(len(votes)):
            len_j = len(votes[j])
            ran = random_int.randint(0, len_j-1)
            m_str = votes[j][ran]
            m = Utils.str_to_message(m_str)
            hm = CryptoHash.get_hash(m, p)
            r = random.randrange(2, p)
            s = random.randrange(2, p)
            vote_g_i.append(pow(g, r, p))
            vote_p_i.append(pow(h, r, p) * m % p)
            hash_g_i.append(pow(g, s, p))
            hash_p_i.append(pow(h, s, p) * hm % p)
        vote_g.append(vote_g_i)
        vote_p.append(vote_p_i)
        hash_g.append(hash_g_i)
        hash_p.append(hash_p_i)
    return [vote_g, vote_p, hash_g, hash_p]


vote_res = random_result([['好看', '不好看'], ['张三', '李四']], 5, g, h, p)
# print(p)
# print(h)
# print(g)
# m_1 = Utils.str_to_message('好看')
# hm_1 = CryptoHash.get_hash(m_1, p)
# m_2 = Utils.str_to_message('张三')
# hm_2 = CryptoHash.get_hash(m_2, p)
# m_3 = Utils.str_to_message('不好看')
# hm_3 = CryptoHash.get_hash(m_3, p)
# m_4 = Utils.str_to_message('李四')
# hm_4 = CryptoHash.get_hash(m_4, p)
# print(m_1)
# print(hm_1)
# print(m_2)
# print(hm_2)
# print(m_3)
# print(hm_3)
# print(m_4)
# print(hm_4)
# r_1 = random.randrange(2, p)
# s_1 = random.randrange(2, p)
# r_2 = random.randrange(2, p)
# s_2 = random.randrange(2, p)
# r_3 = random.randrange(2, p)
# s_3 = random.randrange(2, p)
# r_4 = random.randrange(2, p)
# s_4 = random.randrange(2, p)


# vote_g = [[pow(g, r_1, p), pow(g, r_2, p)], [pow(g, r_3, p), pow(g, r_4, p)]]
# vote_p = [[pow(h, r_1, p) * m_1 % p, pow(h, r_2, p) * m_2 % p],
#           [pow(h, r_3, p) * m_3 % p, pow(h, r_4, p) * m_4 % p]]
# hash_g = [[pow(g, s_1, p), pow(g, s_2, p)], [pow(g, s_3, p), pow(g, s_4, p)]]
# hash_p = [[pow(h, s_1, p) * hm_1 % p, pow(h, s_2, p) * hm_2 % p],
# [pow(h, s_3, p) * hm_3 % p, pow(h, s_4, p) * hm_4 % p]]
starttime = datetime.datetime.now()
net = MixNet(p, g, 'zhunny', 'secret', h, vote_res[0], vote_res[1], vote_res[2],
             vote_res[3], 5, selections)

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
c = int(load_dict[1]['question2']['c'])
d = int(load_dict[1]['question2']['d'])
e = int(load_dict[1]['question2']['e'])
f = int(load_dict[1]['question2']['f'])
res = MixNet.verify(g, h, c, d, message, e, f, p, 1)
print(res)
endtime3 = datetime.datetime.now()
print((endtime3 - starttime3))
