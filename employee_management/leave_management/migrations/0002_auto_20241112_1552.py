# Generated by Django 3.2.25 on 2024-11-12 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leave_management', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='designation',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='phone_number',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
