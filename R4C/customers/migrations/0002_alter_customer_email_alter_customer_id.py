# Generated by Django 4.2.3 on 2024-01-26 11:21

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='email',
            field=models.CharField(max_length=255, validators=[django.core.validators.RegexValidator(regex='^[A-Za-z0-9.]+@[A-Za-z0-9.\\-]+\\.[A-Za-z]{2,}$')]),
        ),
        migrations.AlterField(
            model_name='customer',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]