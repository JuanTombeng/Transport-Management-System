# Generated by Django 3.2.2 on 2021-05-15 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True),
        ),
    ]