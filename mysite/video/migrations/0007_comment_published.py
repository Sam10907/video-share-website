# Generated by Django 2.0.5 on 2019-08-16 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0006_auto_20190816_1545'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='published',
            field=models.BooleanField(default=True),
        ),
    ]