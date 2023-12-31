# Generated by Django 4.1.6 on 2023-02-24 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ims', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(blank=True, max_length=100)),
                ('product_name', models.CharField(blank=True, max_length=100)),
                ('product_qtn', models.IntegerField(blank=True)),
                ('price', models.IntegerField(blank=True)),
                ('sale_price', models.IntegerField(blank=True)),
            ],
        ),
    ]
