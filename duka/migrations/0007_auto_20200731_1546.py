# Generated by Django 3.0.7 on 2020-07-31 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('duka', '0006_auto_20200731_1543'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='email',
            field=models.EmailField(max_length=50),
        ),
    ]
