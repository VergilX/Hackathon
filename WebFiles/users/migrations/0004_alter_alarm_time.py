# Generated by Django 4.0.1 on 2022-01-30 05:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_alarm_status_alter_alarm_turned_on'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alarm',
            name='time',
            field=models.CharField(max_length=8),
        ),
    ]
