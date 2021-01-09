# Generated by Django 3.1.2 on 2020-12-16 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0002_vehiclemanufacturer'),
    ]

    operations = [
        migrations.CreateModel(
            name='TowToWorkshop',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(default='', max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'towtoworkshop',
            },
        ),
    ]