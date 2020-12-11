# Generated by Django 3.1.3 on 2020-12-06 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0003_auto_20201203_0510'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='public',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='item',
            name='visible_priv',
            field=models.BooleanField(default=True),
        ),
    ]