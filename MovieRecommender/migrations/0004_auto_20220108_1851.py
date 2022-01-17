# Generated by Django 3.2.5 on 2022-01-08 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MovieRecommender', '0003_auto_20220108_0244'),
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre_id', models.IntegerField()),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ['-updated', '-created']},
        ),
    ]
