# Generated by Django 2.2.2 on 2019-07-03 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0004_auto_20190703_1223'),
    ]

    operations = [
        migrations.AddField(
            model_name='quizzes',
            name='url_name',
            field=models.SlugField(default='medtest'),
            preserve_default=False,
        ),
    ]