# Generated by Django 2.2.2 on 2019-07-03 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0002_auto_20190626_1536'),
    ]

    operations = [
        migrations.AddField(
            model_name='answers',
            name='answer_correct',
            field=models.BooleanField(default=0),
            preserve_default=False,
        ),
    ]
