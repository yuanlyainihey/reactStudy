from rest_framework import serializers
from .models import ElectionsAminitrator, Election, Voter
from django.contrib.auth.models import User
from .utils.utils import random_string
from rest_framework.exceptions import ValidationError


class ElectionsAminitratorSerializer(serializers.ModelSerializer):
    """
      选举活动管理员的序列化器
    """
    # user_id = serializers.CharField(write_only=True)  # 增加token字段

    class Meta:
        model = ElectionsAminitrator
        fields = ('id', 'aminitrator_first_name',
                  'aminitrator_last_name', 'aminitrator_email', 'aminitrator_status')

    def create(self, validated_data):
        user_name = validated_data['author'].username
        username = validated_data['aminitrator_first_name'] + \
            validated_data['aminitrator_last_name']+'_'+user_name
        try:
            User.objects.get(username=username)
            raise ValidationError('用户名已存在')
        except User.DoesNotExist:
            password = random_string(10)
            user = User.objects.create_user(
                username=username, password=password, email=validated_data['aminitrator_email'])
            user.groups.add(1)
            validated_data['aminitrator_id'] = user.id
            validated_data['aminitrator_password'] = password
            validated_data['aminitrator'] = user
            election_aminitrator = ElectionsAminitrator.objects.create(
                **validated_data)
            return election_aminitrator

    def update(self, instance, validated_data):
        instance.aminitrator_status = validated_data.get(
            'aminitrator_status', instance.aminitrator_status)
        instance.save()
        print(instance)
        print(validated_data)
        return instance


class ElectionSerializer(serializers.ModelSerializer):
    """
      创建选举活动的序列化器
    """
    voter_list = serializers.ListField(
        child=serializers.JSONField()
    )
    email_list = serializers.ListField(
        child=serializers.EmailField()
    )
    question_list = serializers.ListField(
        child=serializers.CharField()
    )
    selection_list = serializers.ListField(
        child=serializers.ListField(child=serializers.CharField())
    )

    class Meta:
        model = Election
        fields = ('id', 'short_name', 'full_name', 'description', 'start_time', 'end_time', 'status',
                  'is_private', 'is_anonymous', 'question_list', 'selection_list', 'voter_list', 'email_list')

    def create(self, validated_data):
        # 先构建Election的模型
        print(validated_data)
        election_aminitrator = ElectionsAminitrator.objects.get(
            aminitrator=validated_data['author'])
        try:
            Election.objects.get(
                author=election_aminitrator, short_name=validated_data['short_name'])
            raise ValidationError('选举活动已存在')
        except Election.DoesNotExist:
            election_dict = {}
            election_dict['author'] = election_aminitrator
            election_dict['short_name'] = validated_data['short_name']
            election_dict['full_name'] = validated_data['full_name']
            election_dict['description'] = validated_data['description']
            election_dict['start_time'] = validated_data['start_time']
            election_dict['end_time'] = validated_data['end_time']
            election_dict['is_private'] = validated_data['is_private']
            election_dict['is_anonymous'] = validated_data['is_anonymous']
            election_dict['status'] = 0
            election_dict['questions'] = "@".join(
                validated_data['question_list'])
            selections = []
            for selection in validated_data['selection_list']:
                selections.append("&".join(selection))
            election_dict['selections'] = "@".join(selections)
            print(election_dict['selections'])
            election = Election.objects.create(**election_dict)
            # 之后为每个voter创建账户
            for i in range(len(validated_data['voter_list'])):
                voter = validated_data['voter_list'][i]
                voter_email = validated_data['email_list'][i]
                voter_dict = {}
                try:
                    user = User.objects.get(username=voter['username'])
                    voter_dict['voter_password'] = 'you know the password'
                except User.DoesNotExist:
                    password = random_string(10)
                    user = User.objects.create_user(
                        username=voter['username'], password=password, email=voter_email)
                    user.first_name = voter['firstname']
                    user.last_name = voter['lastname']
                    user.save()
                    user.groups.add(4)
                    voter_dict['voter_password'] = password
                voter_dict['voter'] = user
                voter_dict['election'] = election
                voter_dict['voter_email'] = voter_email
                voter_dict['voter_first_name'] = voter['firstname']
                voter_dict['voter_last_name'] = voter['lastname']
                Voter.objects.create(**voter_dict)
            return election

    def update(self, instance, validated_data):
        print(validated_data)
        print(instance.id)
        instance.short_name = validated_data.get(
            'short_name', instance.short_name)
        instance.full_name = validated_data.get(
            'full_name', instance.full_name)
        instance.description = validated_data.get(
            'description', instance.description)
        instance.start_time = validated_data.get(
            'start_time', instance.start_time)
        instance.end_time = validated_data.get(
            'end_time', instance.end_time)
        instance.is_private = validated_data.get(
            'is_private', instance.is_private)
        instance.is_anonymous = validated_data.get(
            'is_anonymous', instance.is_anonymous)
        instance.questions = "@".join(
            validated_data['question_list'])
        selections = []
        for selection in validated_data['selection_list']:
            selections.append("&".join(selection))
        instance.selections = "@".join(selections)
        # 之后修改voter及其账户
        for i in range(len(validated_data['voter_list'])):
            voter = validated_data['voter_list'][i]
            voter_email = validated_data['email_list'][i]
            voter_dict = {}
            try:
                user = User.objects.get(username=voter['username'])
                try:
                    Voter.objects.get(voter=user, election=instance)
                    continue
                except Voter.DoesNotExist:
                    voter_dict['voter_password'] = 'you know the password'
            except User.DoesNotExist:
                password = random_string(10)
                user = User.objects.create_user(
                    username=voter['username'], password=password, email=voter_email)
                user.first_name = voter['firstname']
                user.last_name = voter['lastname']
                user.save()
                user.groups.add(4)
                voter_dict['voter_password'] = password
            voter_dict['voter'] = user
            voter_dict['election'] = instance
            voter_dict['voter_email'] = voter_email
            voter_dict['voter_first_name'] = voter['firstname']
            voter_dict['voter_last_name'] = voter['lastname']
            Voter.objects.create(**voter_dict)
        instance.save()
        return instance


class ElectionListSerializer(serializers.ModelSerializer):
    """
      获取选举活动列表的序列化器
    """
    class Meta:
        model = Election
        fields = ('id', 'short_name', 'full_name', 'description', 'start_time', 'end_time', 'status',
                  'is_private', 'is_anonymous', 'questions', 'selections', 'public_key', 'selections_message', 'selections_hash', 'vote_result', 'verify_file')

    def update(self, instance, validated_data):
        """
          局部更新status
        """
        instance.status = validated_data.get(
            'status', instance.status)
        if validated_data['status'] == 1:
            instance.public_key = validated_data.get(
                'public_key', instance.public_key)
            instance.selections_message = validated_data.get(
                'selections_message', instance.selections_message)
            instance.selections_hash = validated_data.get(
                'selections_hash', instance.selections_hash)
        if validated_data['status'] == 3:
            instance.vote_result = validated_data.get(
                'vote_result', instance.vote_result)
            instance.verify_file = validated_data.get(
                'verify_file', instance.verify_file)
        print(instance)
        instance.save()
        return instance


class VoterSerializer(serializers.ModelSerializer):
    """
      投票者的序列化器
    """
    class Meta:
        model = Election
        fields = ('id', 'short_name', 'full_name', 'description', 'start_time', 'end_time',
                  'is_private', 'is_anonymous', 'questions', 'selections')


class VoterPublicSerializer(serializers.ModelSerializer):
    """
      公钥的序列化器
    """
    class Meta:
        model = Election
        fields = ('id', 'public_key', 'selections_message', 'selections_hash')


class VoterUpdateSerializer(serializers.ModelSerializer):
    """
      修改Voter的字段
    """
    class Meta:
        model = Voter
        fields = ('id', 'is_vote', 'vote_g', 'vote_p', 'hash_g', 'hash_p')

    def update(self, instance, validated_data):
        """
          局部更新status
        """
        instance.is_vote = validated_data.get(
            'is_vote', instance.is_vote)
        instance.vote_g = validated_data.get(
            'vote_g', instance.vote_g)
        instance.vote_p = validated_data.get(
            'vote_p', instance.vote_p)
        instance.hash_g = validated_data.get(
            'hash_g', instance.hash_g)
        instance.hash_p = validated_data.get(
            'hash_p', instance.hash_p)
        instance.save()
        return instance
