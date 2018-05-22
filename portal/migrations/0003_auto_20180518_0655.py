# Generated by Django 2.0 on 2018-05-17 22:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0002_customer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='netflow',
            name='server_url',
        ),
        migrations.AddField(
            model_name='netflow',
            name='server',
            field=models.CharField(choices=[('netflow1', 'netflow1'), ('netflow2', 'netflow2'), ('netflow3', 'netflow3'), ('netflow4', 'netflow4')], default='netflow1', max_length=10, verbose_name='服务器'),
        ),
    ]
