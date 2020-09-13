# Generated by Django 2.2.3 on 2020-09-12 17:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reviewapp', '0005_activitylog'),
    ]

    operations = [
        migrations.CreateModel(
            name='RatingEvaluationString',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('string_review', models.CharField(max_length=255)),
                ('evaluate_review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='evaluated_string', to='reviewapp.ActivityLog')),
            ],
        ),
    ]
