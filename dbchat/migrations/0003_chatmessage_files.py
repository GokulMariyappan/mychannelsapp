# Generated by Django 5.1.1 on 2025-05-13 03:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dbchat', '0002_alter_chatmessage_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatmessage',
            name='files',
            field=models.FileField(blank=True, null=True, upload_to='files/'),
        ),
    ]
