# Generated by Django 3.2.5 on 2022-01-09 01:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MovieRecommender', '0011_auto_20220109_0218'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='production_companies',
        ),
        migrations.AddField(
            model_name='movie',
            name='production_companies',
            field=models.ManyToManyField(blank=True, related_name='companies', to='MovieRecommender.Company'),
        ),
    ]