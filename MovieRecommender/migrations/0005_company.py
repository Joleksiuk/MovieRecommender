# Generated by Django 3.2.5 on 2022-01-08 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MovieRecommender', '0004_auto_20220108_1851'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_id', models.IntegerField()),
                ('name', models.CharField(max_length=200)),
            ],
        ),
    ]
