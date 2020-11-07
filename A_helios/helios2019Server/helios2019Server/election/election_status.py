import os
from .elg_cryptos.Elgamal import GenerateParameters
from .elg_cryptos.Utils import str_to_message
from .elg_cryptos.HashTools import CryptoHash
from .elg_cryptos.ElgamalCrypto import MixNet
from .models import ElectionsAminitrator, Election, Voter


def start_election(password, election_id):
    # 生成公钥信息，并根据选举活动管理员提供的口令加盐生成私钥
    election_obj = {}
    try:
        election = Election.objects.get(id=election_id)
        # 生成1024位的公钥需要半个小时，因此先用提前生成好的
        # key = GenerateParameters(1024)
        # key.set_private_key(password, 'salt')
        # election['public_key'] = key.get_public_key()
        election_obj['public_key'] = "{'g':'23462756022781219063177742528105152613107380490299013411060646603133126955246197852245833155759325687847562173551560012558646525195544682276257790652002725402489307514242430737797144631838841538207032778241998258085200027722378228789087396529202346540892311046463093333540040250137450549913814948647551538696', 'h':'80411125422987174979000660364697096248049267994140719668019407280795786364451524527081886432644376501653858433978496064086706792769376641533736131798265840592256974419918497554739241365736786244788320855388920789334931854142302933706065812465416433621004591738843249860482585155297143318756700970693779150093', 'p': '92470546430388686191097347151041999415251362259186034602375112690908573542186277704568047911263475288613908115490318989245406281092315045273079184611763579841000950339650348180275123044886906845389434249060777625583529085186780980582525396794766987475243240321492700180109165656597839707580185195074454651763'}"
        public_key = "{'g':'23462756022781219063177742528105152613107380490299013411060646603133126955246197852245833155759325687847562173551560012558646525195544682276257790652002725402489307514242430737797144631838841538207032778241998258085200027722378228789087396529202346540892311046463093333540040250137450549913814948647551538696', 'h':'80411125422987174979000660364697096248049267994140719668019407280795786364451524527081886432644376501653858433978496064086706792769376641533736131798265840592256974419918497554739241365736786244788320855388920789334931854142302933706065812465416433621004591738843249860482585155297143318756700970693779150093', 'p': '92470546430388686191097347151041999415251362259186034602375112690908573542186277704568047911263475288613908115490318989245406281092315045273079184611763579841000950339650348180275123044886906845389434249060777625583529085186780980582525396794766987475243240321492700180109165656597839707580185195074454651763'}"
        selection_list = [each.split('&')
                          for each in election.selections.split('@')]
        print(selection_list)

        def covert_m(lists):
            dic_m = {}
            for each in lists:
                m = str_to_message(each)
                dic_m[each] = str(m)
            return str(dic_m)

        def covert_hash(lists, p):
            dic_hash = {}
            for each in lists:
                m = str_to_message(each)
                dic_hash[each] = str(CryptoHash.get_hash(m, p))
            return str(dic_hash)

        m_list = [covert_m(item) for item in selection_list]
        message_value = "&&".join(m_list)
        hash_list = [covert_hash(item, eval(public_key)['p'])
                     for item in selection_list]
        hash_value = "&&".join(hash_list)
        election_obj['selections_message'] = message_value
        election_obj['selections_hash'] = hash_value
        return election_obj
    except Election.DoesNotExist:
        return election_obj


def set_active(election_id, is_active):
    # 将某个选举的is_active置为True/False
    election = Election.objects.get(id=election_id)
    voter_list = Voter.objects.filter(election=election)
    for each in voter_list:
        each.is_active = is_active
        each.save()


def delete_voters(election_id):
    """
    删除该选举对应的voters
    """
    election = Election.objects.get(id=election_id)
    Voter.objects.filter(election=election).delete()


def generate_result(password, election_id):
    """
      生成投票结果
    """
    election = Election.objects.get(id=election_id)
    voterlist = Voter.objects.filter(election=election)
    public_key = eval(election.public_key)
    p = int(public_key['p'])
    g = int(public_key['g'])
    h = int(public_key['h'])
    selections = [eval(each)
                  for each in election.selections_message.split("&&")]
    vote_g = []
    vote_p = []
    hash_g = []
    hash_p = []
    voter_len = 0
    for item in voterlist:
        if len(item.vote_g) != 0:
            voter_len += 1
            vote_g.append([int(each) for each in item.vote_g.split("&&")])
            vote_p.append([int(each) for each in item.vote_p.split("&&")])
            hash_g.append([int(each) for each in item.hash_g.split("&&")])
            hash_p.append([int(each) for each in item.hash_p.split("&&")])

    net = MixNet(p, g, password, 'secret', h, vote_g, vote_p, hash_g,
                 hash_p, voter_len, selections)
    result = net.get_plain_text()
    folder = os.path.join(os.path.abspath(os.path.dirname(
        os.path.dirname(__file__))), 'election\\verifyfiles\\')
    path = folder + "verify_for_election_" + str(election_id) + ".json"
    net.verify_file_generate(path)

    print(net.result)
    election_obj = {}
    election_obj['vote_result'] = str(result)
    election_obj['verify_file'] = "download/" + \
        "verify_for_election_" + str(election_id) + ".json"
    return election_obj
