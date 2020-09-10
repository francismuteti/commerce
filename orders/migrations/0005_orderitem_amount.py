# Generated by Django 3.0.7 on 2020-08-13 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_auto_20200804_1532'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=23, max_digits=10),
            preserve_default=False,
        ),
    ]