# Generated by Django 5.0.3 on 2024-05-07 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('price', models.IntegerField()),
                ('cat', models.CharField(max_length=50)),
                ('pdetail', models.CharField(max_length=300)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
    ]
