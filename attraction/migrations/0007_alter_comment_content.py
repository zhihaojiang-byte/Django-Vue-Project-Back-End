# Generated by Django 4.1.6 on 2023-05-25 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attraction', '0006_remove_attraction_desc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='content',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
