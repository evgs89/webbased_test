# Generated by Django 2.2.2 on 2019-07-18 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0013_auto_20190718_1513'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quizzes',
            name='initial_weight',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='quizzes',
            name='max_weight',
            field=models.FloatField(null=True),
        ),
    ]