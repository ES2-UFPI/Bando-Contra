# Generated by Django 3.2.3 on 2021-05-20 00:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_clientuser_options'),
    ]

    operations = [
        migrations.RenameField(
            model_name='clientuser',
            old_name='born_date',
            new_name='bornDate',
        ),
    ]
