# Generated by Django 3.1.1 on 2020-09-27 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='name_on_card',
            field=models.CharField(default='default name on card', max_length=100),
            preserve_default=False,
        ),
    ]
