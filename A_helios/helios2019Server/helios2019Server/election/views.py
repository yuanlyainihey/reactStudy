from .models import ElectionsAminitrator, Election, Voter
from rest_framework import status
from rest_framework.response import Response
from election.serializers import ElectionsAminitratorSerializer, ElectionSerializer, ElectionListSerializer, VoterSerializer, VoterPublicSerializer, VoterUpdateSerializer
from django.contrib.auth.models import User
from rest_framework import generics
from .utils.send_email import EmailSender
from .election_status import start_election, set_active, delete_voters, generate_result
import smtplib
from .elg_cryptos.ElgamalCrypto import MixNet
from itertools import chain
from django.db.models import Q
# from django.core.mail import send_mail


class EletionAminitratorListCreate(generics.ListCreateAPIView):
    queryset = ElectionsAminitrator.objects.all()

    def create(self, request):
        """
          创建选举活动管理员
        """
        serializer = ElectionsAminitratorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        """
          获取选举活动管理员列表
        """
        aminitrators = ElectionsAminitrator.objects.filter(author=request.user)
        serializer = ElectionsAminitratorSerializer(aminitrators, many=True)
        return Response(serializer.data)


class EletionAminitratorUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = ElectionsAminitrator.objects.all()

    def destroy(self, request, pk=None):
        """
          删除选举活动管理员
        """
        try:
            aminitrator = ElectionsAminitrator.objects.get(pk=pk)
            user = User.objects.get(id=aminitrator.aminitrator_id)
        except ElectionsAminitrator.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        user.delete()
        aminitrators = ElectionsAminitrator.objects.filter(author=request.user)
        serializer = ElectionsAminitratorSerializer(aminitrators, many=True)
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        """
          发送邮件，并修改状态值为1，部分更新
        """
        try:
            aminitrator = ElectionsAminitrator.objects.get(pk=pk)
        except ElectionsAminitrator.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ElectionsAminitratorSerializer(
            aminitrator, data=request.data, partial=True)
        if serializer.is_valid():
            email_sender = EmailSender([aminitrator.aminitrator_email], [aminitrator.aminitrator.username], [
                                       aminitrator.aminitrator_password], '测试url', '您已成为选举活动创建者')
            try:
                email_sender.send_emails(1)
            except smtplib.SMTPException as e:
                return Response(e, status=status.HTTP_400_BAD_REQUEST)
            # url = '测试url'
            # email_text = "尊敬的" + aminitrator.aminitrator_first_name + aminitrator.aminitrator_last_name + "，您好：\n " + '您已成为选举活动创建者' + "\n  " \
            #     "本次投票地址："+url+"\n  您的登录账户为：" + aminitrator.aminitrator.username + \
            #     "\n  您的登录密码为：" + aminitrator.aminitrator_password
            # send_mail('Helios-选举活动管理员', email_text, 'zhunnyxd@163.com',
            #           [aminitrator.aminitrator_email], fail_silently=False)
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EletionListCreate(generics.ListCreateAPIView):
    queryset = Election.objects.all()

    def create(self, request):
        """
          创建选举以及它对应的投票者们，重写serialier的create方法
        """
        serializer = ElectionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            print(serializer.validated_data)
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        """
          获取选举活动列表,同时要获取投票者列表
        """
        election_aminitrator = ElectionsAminitrator.objects.get(
            aminitrator=request.user)
        elections = Election.objects.filter(author=election_aminitrator)
        serializer = ElectionListSerializer(elections, many=True)
        elections_list = serializer.data
        for election in elections_list:
            election['questions'] = election['questions'].split('@')
            # print(election['selections'])
            election['selections'] = [each.split(
                '&') for each in election['selections'].split('@')]
            election_obj = Election.objects.get(id=election['id'])
            election['voterslist'] = [{'username': User.objects.get(id=item[0]).username, 'firstname': item[1], 'lastname': item[2]}
                                      for item in list(Voter.objects.filter(election=election_obj).values_list('voter', 'voter_first_name', 'voter_last_name'))]
            election['emaillist'] = [item[0] for item in list(
                Voter.objects.filter(election=election_obj).values_list('voter_email'))]
            election['author'] = request.user.username
        return Response(elections_list)


class EletionRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Election.objects.all()

    def update(self, request, pk=None):
        """
          全部更新
        """
        try:
            election = Election.objects.get(pk=pk)
        except Election.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ElectionSerializer(election, data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data = serializer.validated_data
            response_data['questions'] = serializer.validated_data['question_list']
            response_data['selections'] = serializer.validated_data['selection_list']
            response_data['voterslist'] = serializer.validated_data['voter_list']
            response_data['emaillist'] = serializer.validated_data['email_list']
            response_data['id'] = int(pk)
            del response_data['question_list']
            del response_data['selection_list']
            del response_data['voter_list']
            del response_data['email_list']
            return Response(serializer.validated_data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        """
          根据不同的status，做不同操作
        """
        try:
            election = Election.objects.get(pk=pk)
        except Election.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        print(request.data)
        election_status = request.data['status']
        if election_status == 1:
            """
              status为1时开启投票，准备选票，将该选举对应的voters的is_active全部至为True
            """
            if request.data['index'] == 0:
                password = request.data['password']
                election_obj = start_election(password, int(pk))
            elif request.data['index'] == 1:
                """
                重启选票，将该选举对应的voters的is_active全部至为True
                """
                election_obj = {}
            set_active(int(pk), True)
        if election_status == 2:
            """
              冻结选举期间投票者无法投票，将该选举对应的voters的is_active全部至为False
            """
            election_obj = {}
            set_active(int(pk), False)
        if election_status == 6:
            """
              废弃选举，将该选举对应的voters的is_active全部至为False
              是否删除对应的voters？删除对应的voters吧
            """
            election_obj = {}
            delete_voters(int(pk))
        if election_status == 4:
            """
              结束选举，将该选举对应的voters的is_active全部至为False
            """
            election_obj = {}
            set_active(int(pk), False)
        if election_status == 3:
            """
              生成结果，生成结果后的一段时间，选举会在公示期
            """
            password = request.data['password']
            election_obj = generate_result(password, int(pk))
        if election_status == 5:
            """
              结束投诉
            """
            election_obj = {}
            set_active(int(pk), False)
        election_obj['status'] = election_status
        serializer = ElectionListSerializer(
            election, data=election_obj, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """
          给所有voter发送邮件
        """
        try:
            election = Election.objects.get(pk=pk)
        except Election.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        voter_list = Voter.objects.filter(election=election)
        receivers = []
        usernames = []
        passwords = []
        for each in voter_list:
            usernames.append(each.voter.username)
            receivers.append(each.voter_email)
            passwords.append(each.voter_password)
            # each.is_active = True
            # each.save()
        email_sender = EmailSender(
            receivers, usernames, passwords, '测试url', '您已成为'+election.full_name+'选举活动的投票者')
        try:
            email_sender.send_emails(1)
        except smtplib.SMTPException as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)
        serializer = ElectionListSerializer(election)
        return Response(serializer.data)


class VoterList(generics.ListAPIView):
    queryset = Election.objects.all()

    def list(self, request):
        """
          获取该投票者对应的election列表
        """
        voter_elections = Voter.objects.filter(
            voter=request.user, is_active=True).values_list('election')
        elections = []
        for each in voter_elections:
            # print(each[0].short_name)
            election = Election.objects.get(id=each[0])
            elections.append(election)
        voter_is_votes = Voter.objects.filter(
            voter=request.user, is_active=True).values_list('is_vote')
        print(voter_is_votes)
        serializer = VoterSerializer(elections, many=True)
        response_data = serializer.data
        for i in range(len(response_data)):
            response_data[i]['isvoted'] = voter_is_votes[i][0]
            response_data[i]['questions'] = response_data[i]['questions'].split(
                '@')
            response_data[i]['selections'] = [each.split(
                '&') for each in response_data[i]['selections'].split('@')]
        return Response(response_data)


class VoterRetrieveUpdateDestroy(generics.RetrieveUpdateAPIView):
    queryset = Election.objects.all()

    def retrieve(self, request, pk=None):
        """
        获取某次选举的公钥信息
        """
        try:
            election = Election.objects.get(pk=pk)
        except Election.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = VoterPublicSerializer(election)
        data = serializer.data
        response_data = {}
        response_data['publickey'] = eval(data['public_key'])
        response_data['selectionmessage'] = [
            eval(each) for each in data['selections_message'].split('&&')]
        response_data['selectionhash'] = [
            eval(each) for each in data['selections_hash'].split('&&')]
        return Response(response_data)

    def partial_update(self, request, pk=None):
        """
        修改voter中的参数，is_vote为True，vote_g、vote_p、hash_g、hash_p赋值
        """
        try:
            election = Election.objects.get(pk=pk)
        except Election.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            voter = Voter.objects.get(election=election, voter=request.user)
        except Voter.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        update_data = {}
        update_data['is_vote'] = True
        update_data['vote_g'] = ('&&').join(request.data['vote_g'])
        update_data['vote_p'] = ('&&').join(request.data['vote_p'])
        update_data['hash_g'] = ('&&').join(request.data['hash_g'])
        update_data['hash_p'] = ('&&').join(request.data['hash_p'])

        serializer = VoterUpdateSerializer(
            voter, data=update_data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BbsRetrieve(generics.RetrieveAPIView):
    queryset = Election.objects.all()

    def retrieve(self, request, pk=None):
        """
        获取bbs的所有信息
        """
        try:
            election = Election.objects.get(pk=pk)
        except Election.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ElectionListSerializer(election)
        election_obj = serializer.data
        result = {}
        if election_obj['is_anonymous']:
            if election_obj['public_key'] != '':
                result['publicmessage'] = eval(election_obj['public_key'])
            else:
                result['publicmessage'] = '暂无生成公钥信息'
            if election_obj['verify_file']:
                result['provemessage'] = election_obj['verify_file']
        else:
            result['publicmessage'] = "非加密投票中无需产生公钥"
            result['provemessage'] = "非加密投票中无需产生证明文件"
        voter_list = Voter.objects.filter(
            election=election).values_list('voter', 'hash_g', 'hash_p')
        privatemessage = []
        for each in voter_list:
            if each[1] != '':
                privatemessage.append(
                    {'user': User.objects.get(id=each[0]).username, 'hash_g': each[1], 'hash_p': each[2]})
        result['privatemessage'] = privatemessage

        if election_obj['status'] == 3 or election_obj['status'] == 5:
            result['resshow'] = eval(election_obj['vote_result'])
            result['resstatistics'] = MixNet.count_votes(
                eval(election_obj['vote_result']))
        else:
            result['resshow'] = ""
            result['resstatistics'] = ""
        return Response(result)


class VerifyVoterList(generics.ListAPIView):
    queryset = Election.objects.all()

    def list(self, request):
        """
        根据身份获取可验证投票的所有elections
        选举活动管理员：1 可以验证其创建的所有选举活动
        观察员：2.只能查看公开选举，即isprivate为false的选举活动
        系统管理员：3 可以查看其创建的选举活动管理员创建的所有选举活动
        投票者：4。可以查看其参加的所有选举活动
        1，2，4都具有观察者的权限
        """
        print(request.user)
        group_id = User.objects.get(username=request.user).groups.all()[0].id
        print(group_id)
        elections = []
        if group_id == 1:
            election_aminitrator = ElectionsAminitrator.objects.get(
                aminitrator=request.user)
            elections = Election.objects.filter(
                ~Q(status=0), ~Q(status=6), author=election_aminitrator)
        if group_id == 3:
            aminitrators = ElectionsAminitrator.objects.filter(
                author=request.user)
            # elections = []
            for each in aminitrators:
                print(User.objects.get(id=each.aminitrator_id).username)
                try:
                    election_aminitrator = ElectionsAminitrator.objects.get(
                        aminitrator=User.objects.get(id=each.aminitrator_id))
                    elections_obj = Election.objects.filter(
                        ~Q(status=0), ~Q(status=6), author=election_aminitrator)
                    elections = chain(elections, elections_obj)
                except ElectionsAminitrator.DoesNotExist:
                    continue
        if group_id == 4:
            voter_elections = Voter.objects.filter(
                voter=request.user).values_list('election')
            # elections = []
            for each in voter_elections:
                election_obj = Election.objects.filter(
                    ~Q(status=0), ~Q(status=6), id=each[0])
                elections = chain(elections, election_obj)
                # if election:
                #     elections.append(election)
        isprivate_elections = Election.objects.filter(
            ~Q(status=0), ~Q(status=6), is_private=False)
        elections = chain(elections, isprivate_elections)
        serializer = VoterSerializer(elections, many=True)
        response_data = serializer.data
        for i in range(len(response_data)):
            response_data[i]['questions'] = response_data[i]['questions'].split(
                '@')
            response_data[i]['selections'] = [each.split(
                '&') for each in response_data[i]['selections'].split('@')]
        return Response(response_data)
