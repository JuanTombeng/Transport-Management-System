# Generated by Django 3.2.2 on 2021-05-13 05:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0012_alter_destinations_departure_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicles',
            name='currentMaintenanceIssue',
            field=models.TextField(),
        ),
    ]
