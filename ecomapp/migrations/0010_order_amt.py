# Generated by Django 5.0.3 on 2024-05-14 07:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecomapp', '0009_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='amt',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
