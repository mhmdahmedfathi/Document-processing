# Generated by Django 3.2.12 on 2023-08-10 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0002_auto_20230810_1025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='pdfs',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
