# Generated by Django 3.2 on 2023-01-25 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_auto_20230125_1920'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productimage',
            name='alt',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
