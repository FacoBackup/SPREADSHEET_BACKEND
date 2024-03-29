# Generated by Django 3.1.5 on 2021-02-10 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.TextField()),
                ('email', models.CharField(max_length=320, unique=True)),
                ('phone', models.CharField(max_length=120, unique=True)),
                ('pic', models.TextField(blank=True, null=True)),
                ('birth', models.PositiveBigIntegerField()),
                ('nationality', models.TextField()),
                ('study', models.CharField(max_length=512)),
                ('about', models.TextField(blank=True, null=True)),
                ('background', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
