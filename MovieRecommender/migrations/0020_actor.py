# Generated by Django 3.2.5 on 2022-01-15 22:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MovieRecommender', '0019_alter_rating_unique_together'),
    ]

    operations = [
        migrations.CreateModel(
            name='Actor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=200)),
                ('role', models.CharField(default='', max_length=200)),
                ('biography', models.TextField(blank=True, null=True)),
                ('birthday', models.CharField(default='', max_length=200)),
                ('profile_path', models.CharField(default='https://davinci22.ru/wp-content/uploads/2014/01/default-avatar-m_1920.png', max_length=200)),
            ],
        ),
    ]
