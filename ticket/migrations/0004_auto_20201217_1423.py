# Generated by Django 3.1.2 on 2020-12-17 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0003_towtoworkshop'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('location', models.CharField(default='', max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'location',
            },
        ),
        migrations.AddField(
            model_name='tickets',
            name='locationID',
            field=models.CharField(default='', max_length=255, null=True),
        ),
    ]
