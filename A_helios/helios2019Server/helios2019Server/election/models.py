from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from .utils.utils import random_string


class ElectionsAminitrator(models.Model):
    asset_status = (
        (0, '已通知'),
        (1, '投票中'),
    )
    author = models.ForeignKey(
        User, related_name='author_admins', on_delete=models.CASCADE)
    aminitrator = models.OneToOneField(
        User, related_name='aminitrator_admins', on_delete=models.CASCADE)
    aminitrator_first_name = models.CharField(max_length=30, blank=True)
    aminitrator_last_name = models.CharField(max_length=150, blank=True)
    aminitrator_email = models.EmailField(blank=True)
    aminitrator_password = models.CharField(max_length=100)
    aminitrator_status = models.SmallIntegerField(
        choices=asset_status, default=0)

    class Meta:
        permissions = (
            ('view_elections_aminitrator', 'can view elections aminitrator'),
        )

    def generate_password(self, length=10):
        """
        随机生成密码
        """
        if self.aminitrator_password != '':
            raise Exception("password already exists")

        self.aminitrator_password = random_string(length)


class Election(models.Model):
    asset_status = (
        (0, '未启动'),
        (1, '投票中'),
        (2, '冻结中'),
        (3, '验证中'),
        (4, '已完成'),
        (5, '已结束'),
        (6, '已废弃'),
    )
    short_name = models.CharField(max_length=300)
    full_name = models.CharField(max_length=300)
    author = models.ForeignKey(
        'ElectionsAminitrator', on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True, default='')
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(default=timezone.now)
    status = models.SmallIntegerField(choices=asset_status, default=0)
    is_private = models.BooleanField(default=True)
    is_anonymous = models.BooleanField(default=True)
    questions = models.TextField(null=True, default='')
    selections = models.TextField(null=True, default='')
    public_key = models.TextField(null=True, default='')
    verify_file = models.CharField(max_length=300, blank=True)
    vote_result = models.CharField(max_length=500, blank=True)
    selections_message = models.TextField(
        null=True, default='')
    selections_hash = models.TextField(
        null=True, default='')

    class Meta:
        permissions = (
            ('view_elections', 'can view elections'),
        )
        unique_together = (("author", "short_name"),)


class Voter(models.Model):
    voter = models.ForeignKey(User, on_delete=models.CASCADE)
    # voter = models.OneToOneField(User, on_delete=models.CASCADE)
    election = models.ForeignKey('Election', on_delete=models.CASCADE)
    voter_email = models.EmailField(blank=True)
    voter_password = models.CharField(max_length=100)
    voter_first_name = models.CharField(max_length=30, blank=True)
    voter_last_name = models.CharField(max_length=150, blank=True)
    is_vote = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    vote_g = models.TextField(null=True, default='')
    vote_p = models.TextField(null=True, default='')
    hash_g = models.TextField(null=True, default='')
    hash_p = models.TextField(null=True, default='')

    class Meta:
        permissions = (
            ('view_voters', 'can view voters'),
        )
        unique_together = (("voter", "election"),)

    def generate_password(self, length=10):
        """
        随机生成密码
        """
        if self.voter_password != '':
            raise Exception("password already exists")

        self.voter_password = random_string(length)
