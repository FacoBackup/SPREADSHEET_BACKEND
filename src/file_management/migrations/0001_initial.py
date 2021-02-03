# Generated by Django 3.1.5 on 2021-02-03 12:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0002_auto_20210131_1530'),
        ('group', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.TextField()),
                ('is_master', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Column',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.TextField()),
                ('branch_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='file_management.branch')),
            ],
        ),
        migrations.CreateModel(
            name='Row',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('content', models.TextField()),
                ('column_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='file_management.column')),
            ],
        ),
        migrations.CreateModel(
            name='Repository',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.TextField()),
                ('about', models.TextField()),
                ('group_fk', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='group.group')),
            ],
        ),
        migrations.CreateModel(
            name='Commit',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('changes', models.BigIntegerField()),
                ('commit_time', models.BigIntegerField()),
                ('message', models.TextField()),
                ('branch_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='file_management.branch')),
            ],
        ),
        migrations.AddField(
            model_name='branch',
            name='repository_fk',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='file_management.repository'),
        ),
        migrations.AddField(
            model_name='branch',
            name='user_fk',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='user.user'),
        ),
    ]