# Generated by Django 2.1.7 on 2019-06-11 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_friend'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductRank',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uniq_id', models.CharField(blank=True, max_length=255, null=True)),
                ('rank', models.IntegerField(null=True)),
            ],
            options={
                'verbose_name_plural': 'Ranking',
            },
        ),
    ]