# Generated by Django 4.0 on 2024-01-19 16:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_myuser_picture'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='myuser',
            options={'ordering': ['email']},
        ),
    ]