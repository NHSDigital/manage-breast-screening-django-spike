# Generated by Django 5.1.8 on 2025-05-06 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinics', '0007_appointment_reinvite'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='stopped_reasons',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
