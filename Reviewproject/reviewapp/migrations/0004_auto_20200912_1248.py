# Generated by Django 2.2.3 on 2020-09-12 12:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviewapp', '0003_product_desciption'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='desciption',
            new_name='description',
        ),
    ]
