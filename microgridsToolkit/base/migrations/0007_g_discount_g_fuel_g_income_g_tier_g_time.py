# Generated by Django 3.2.7 on 2021-12-12 02:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0006_auto_20211211_2143'),
    ]

    operations = [
        migrations.CreateModel(
            name='G_Time',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gen_StartingYear', models.IntegerField(blank=True, null=True)),
                ('gen_ProjectionPeriod', models.IntegerField(blank=True, null=True)),
                ('gen_MonthsNumber', models.IntegerField(blank=True, null=True)),
                ('gen_Notes', models.TextField(blank=True, null=True)),
                ('gen_Source', models.TextField(blank=True, null=True)),
                ('gen_idProject', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.project')),
                ('gen_idUser', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='G_Tier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gen_WorldBankTier', models.CharField(blank=True, max_length=50, null=True)),
                ('gen_Notes', models.TextField(blank=True, null=True)),
                ('gen_Source', models.TextField(blank=True, null=True)),
                ('gen_idProject', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.project')),
                ('gen_idUser', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='G_Income',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gen_ResidentialIncome', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('gen_ResidentialWillingness', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('gen_CommercialIncome', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('gen_CommercialWillingness', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('gen_Notes', models.TextField(blank=True, null=True)),
                ('gen_Source', models.TextField(blank=True, null=True)),
                ('gen_idProject', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.project')),
                ('gen_idUser', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='G_Fuel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gen_CommercialFuelUsed', models.CharField(blank=True, max_length=20, null=True)),
                ('gen_CommercialFuelMonthly', models.FloatField(blank=True, null=True)),
                ('gen_CommercialFuelCost', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('gen_ResidentialFuelUsed', models.CharField(blank=True, max_length=20, null=True)),
                ('gen_ResidentialFuelMonthly', models.FloatField(blank=True, null=True)),
                ('gen_ResidentialFuelCost', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('gen_Notes', models.TextField(blank=True, null=True)),
                ('gen_Source', models.TextField(blank=True, null=True)),
                ('gen_idProject', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.project')),
                ('gen_idUser', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='G_Discount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gen_DiscountRate', models.FloatField(blank=True, null=True)),
                ('gen_Notes', models.TextField(blank=True, null=True)),
                ('gen_Source', models.TextField(blank=True, null=True)),
                ('gen_idProject', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.project')),
                ('gen_idUser', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
