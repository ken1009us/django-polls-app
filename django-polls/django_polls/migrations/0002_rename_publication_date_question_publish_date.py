# Generated by Django 5.0.3 on 2024-03-11 04:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question',
            old_name='publication_date',
            new_name='publish_date',
        ),
    ]
