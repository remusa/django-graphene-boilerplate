# Generated by Django 3.0 on 2019-12-14 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0002_link_posted_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='link',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
