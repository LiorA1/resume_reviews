# Generated by Django 3.1.2 on 2021-04-28 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resumes', '0002_auto_20210428_2029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resume',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='resume',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
