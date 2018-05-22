# Generated by Django 2.0 on 2018-05-13 23:10

from django.db import migrations, models
import django.utils.timezone
import portal.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Availability',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=40, verbose_name='用户名')),
                ('ip', models.CharField(max_length=20, verbose_name='IP')),
                ('description', models.CharField(max_length=100, verbose_name='描述')),
                ('triggerid', models.CharField(max_length=10, verbose_name='触发器ID')),
                ('create_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建日期')),
                ('mod_date', models.DateTimeField(auto_now=True, verbose_name='最后修改日期')),
            ],
        ),
        migrations.CreateModel(
            name='Cacti',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=40, verbose_name='用户名')),
                ('description', models.CharField(max_length=100, verbose_name='描述')),
                ('link', models.CharField(max_length=100, verbose_name='URL')),
                ('create_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建日期')),
                ('mod_date', models.DateTimeField(auto_now=True, verbose_name='最后修改日期')),
            ],
        ),
        migrations.CreateModel(
            name='Netflow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=40, verbose_name='用户名')),
                ('j_username', models.CharField(max_length=40, verbose_name='Netflow帐号')),
                ('j_password', models.CharField(max_length=40, verbose_name='Netflow密码')),
                ('server_url', models.CharField(max_length=40, verbose_name='服务器URL')),
                ('create_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建日期')),
                ('mod_date', models.DateTimeField(auto_now=True, verbose_name='最后修改日期')),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=40, verbose_name='用户名')),
                ('filename', models.CharField(blank=True, max_length=255)),
                ('fileurl', models.FileField(upload_to=portal.models.reporturl_handler)),
                ('create_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建日期')),
            ],
        ),
    ]
