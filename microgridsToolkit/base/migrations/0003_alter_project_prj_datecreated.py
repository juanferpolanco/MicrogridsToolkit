# Generated by Django 3.2.7 on 2021-11-20 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_alter_project_prj_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='prj_datecreated',
            field=models.DateField(auto_now_add=True),
        ),
    ]
