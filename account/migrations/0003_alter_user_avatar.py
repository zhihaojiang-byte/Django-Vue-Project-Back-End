# Generated by Django 4.1.6 on 2023-05-30 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_alter_user_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, default='avatar/default/avatar.png', max_length=250, null=True, upload_to='avatar/%Y%m'),
        ),
    ]
