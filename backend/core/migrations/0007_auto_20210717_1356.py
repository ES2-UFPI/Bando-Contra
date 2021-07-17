# Generated by Django 3.2.3 on 2021-07-17 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_service'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'ordering': ['arrival'], 'verbose_name': 'Event'},
        ),
        migrations.AddField(
            model_name='service',
            name='clientFeedback',
            field=models.TextField(blank=True, default=None, null=True, verbose_name='Feedback'),
        ),
        migrations.AlterField(
            model_name='clientuser',
            name='address',
            field=models.CharField(default=None, max_length=100, null=True, verbose_name='Address'),
        ),
        migrations.AlterField(
            model_name='clientuser',
            name='cpf',
            field=models.CharField(default=None, max_length=11, null=True, verbose_name='CPF'),
        ),
        migrations.AlterField(
            model_name='event',
            name='address',
            field=models.CharField(default=None, max_length=100, null=True, verbose_name='Address'),
        ),
        migrations.AlterField(
            model_name='partneruser',
            name='nationality',
            field=models.CharField(default=None, max_length=50, null=True, verbose_name='Nationality'),
        ),
        migrations.AlterField(
            model_name='partneruser',
            name='observation',
            field=models.CharField(default=None, max_length=5000, null=True, verbose_name='Observation'),
        ),
        migrations.AlterField(
            model_name='service',
            name='address',
            field=models.CharField(default=None, max_length=100, null=True, verbose_name='Address'),
        ),
        migrations.AlterField(
            model_name='service',
            name='itemDescription',
            field=models.CharField(default=None, max_length=300, null=True, verbose_name='Item Description'),
        ),
        migrations.AlterField(
            model_name='service',
            name='problemDescription',
            field=models.CharField(default=None, max_length=200, null=True, verbose_name='Problem Description'),
        ),
        migrations.AlterField(
            model_name='service',
            name='productStatus',
            field=models.CharField(default=None, max_length=100, null=True, verbose_name='Product Status'),
        ),
    ]
