# Generated by Django 5.0.2 on 2024-05-10 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_user_password'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
            ],
        ),
        migrations.AlterField(
            model_name='user',
            name='startAmountOfCigarettes',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
