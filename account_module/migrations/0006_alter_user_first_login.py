# Generated by Django 5.0.3 on 2024-12-12 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account_module', '0005_user_first_login'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='First_login',
            field=models.BooleanField(default=True),
        ),
    ]