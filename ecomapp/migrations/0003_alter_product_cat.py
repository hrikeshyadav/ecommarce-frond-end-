# Generated by Django 5.0.3 on 2024-05-07 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecomapp', '0002_alter_product_cat_alter_product_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='cat',
            field=models.IntegerField(verbose_name='Catogary'),
        ),
    ]
