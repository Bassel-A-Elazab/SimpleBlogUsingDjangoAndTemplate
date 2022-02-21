# Generated by Django 4.0 on 2022-02-21 20:03

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_myuser_is_active'),
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blog',
            options={'ordering': ['-post_date']},
        ),
        migrations.AlterField(
            model_name='blog',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.myuser', verbose_name="blog's author"),
        ),
        migrations.AlterField(
            model_name='blog',
            name='description',
            field=models.TextField(help_text='Enter you blog text here.', max_length=2000, verbose_name="blog's description"),
        ),
        migrations.AlterField(
            model_name='blog',
            name='post_date',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name="blog's posted date"),
        ),
        migrations.AlterField(
            model_name='blog',
            name='title',
            field=models.CharField(max_length=200, verbose_name="blog's title"),
        ),
    ]
