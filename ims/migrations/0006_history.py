# Generated by Django 4.1.3 on 2023-02-25 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ims', '0005_sales'),
    ]

    operations = [
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_name', models.CharField(blank=True, max_length=100)),
                ('client_phone', models.CharField(blank=True, max_length=100)),
                ('client_address', models.CharField(blank=True, max_length=100)),
                ('products', models.CharField(blank=True, max_length=100)),
                ('total_qtn', models.IntegerField(blank=True)),
                ('total_price', models.IntegerField(blank=True)),
                ('date', models.CharField(blank=True, max_length=100)),
            ],
        ),
    ]