# Generated by Django 3.2.5 on 2022-01-09 01:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MovieRecommender', '0010_rename_movies_movie'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='budget',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='movie',
            name='movie_id',
            field=models.IntegerField(default=-1),
        ),
        migrations.AlterField(
            model_name='movie',
            name='org_language',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='movie',
            name='overview',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='movie',
            name='popularity',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='movie',
            name='poster_path',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='movie',
            name='release_date',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='movie',
            name='title',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='movie',
            name='video',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='movie',
            name='vote_average',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='movie',
            name='vote_count',
            field=models.IntegerField(default=0),
        ),
    ]