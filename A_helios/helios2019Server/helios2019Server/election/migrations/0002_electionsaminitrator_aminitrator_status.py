# Generated by Django 2.2.7 on 2020-02-06 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('election', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='electionsaminitrator',
            name='aminitrator_status',
            field=models.SmallIntegerField(choices=[(0, '已通知'), (1, '投票中')], default=0),
        ),
    ]
