# Generated by Django 4.0.1 on 2022-01-28 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alarm',
            name='REPEAT',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='alarm',
            name='repeat_time',
            field=models.TimeField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='alarm',
            name='status',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
        migrations.AlterField(
            model_name='alarm',
            name='turned_on',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
    ]
