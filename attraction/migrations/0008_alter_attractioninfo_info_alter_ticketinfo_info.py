# Generated by Django 4.1.6 on 2023-05-26 20:52

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attraction', '0007_alter_comment_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attractioninfo',
            name='info',
            field=ckeditor.fields.RichTextField(),
        ),
        migrations.AlterField(
            model_name='ticketinfo',
            name='info',
            field=ckeditor.fields.RichTextField(),
        ),
    ]
