# Generated by Django 2.2.3 on 2020-09-12 09:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviewapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='Ticket',
            new_name='image',
        ),
    ]
