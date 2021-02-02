# Generated by Django 3.1.5 on 2021-02-02 11:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20210131_1530'),
        ('repository', '0003_auto_20210201_1802'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='formcontent',
            name='creator',
        ),
        migrations.AddField(
            model_name='repository',
            name='creator_fk',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.user'),
        ),
    ]