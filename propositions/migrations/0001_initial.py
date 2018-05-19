# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-28 16:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('email', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProtoProposition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email_message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='email.EmailMessage')),
            ],
        ),
    ]
