# Generated by Django 2.2.2 on 2019-07-10 11:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0009_auto_20190704_1540'),
    ]

    operations = [
        migrations.RenameField(
            model_name='questions',
            old_name='question_id',
            new_name='question_tag',
        ),
    ]
