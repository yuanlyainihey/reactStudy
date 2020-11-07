from Crypto.PublicKey import ECC
from Crypto.Hash import SHA256
from Crypto.Math.Numbers import *


def str_to_bytes(o_str):
    """
      字符串转字节串
    """
    return o_str.encode()


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


def get_point_dic(input_string):
    """
    根据输入的消息，对应到椭圆曲线上的某个点(x, y)
    """
    G = ECC._curves['P-256'].G.copy()
    order = ECC._curves['P-256'].order
    ha = SHA256.new()
    ha.update(str_to_bytes(input_string))
    input_bytes = ha.digest()
    input_integer = Integer.__mod__(Integer.from_bytes(input_bytes), order)
    return {input_string: G*input_integer}


# message_dict = get_point_dic('ii')
# print(message_dict)
# m = string_to_point('ii', message_dict)
# print(m.x, ':', m.y)
