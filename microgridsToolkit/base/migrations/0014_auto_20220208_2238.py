# Generated by Django 3.2.7 on 2022-02-09 03:38

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0013_auto_20220208_2225'),
    ]

    operations = [
        migrations.AlterField(
            model_name='r_rates',
            name='rev_FixedCostCommercialOp1',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, validators=[django.core.validators.DecimalValidator]),
        ),
        migrations.AlterField(
            model_name='r_rates',
            name='rev_FixedCostCommercialOp3',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, validators=[django.core.validators.DecimalValidator]),
        ),
        migrations.AlterField(
            model_name='r_rates',
            name='rev_FixedCostResidentialOp1',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, validators=[django.core.validators.DecimalValidator]),
        ),
        migrations.AlterField(
            model_name='r_rates',
            name='rev_FixedCostResidentialOp3',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, validators=[django.core.validators.DecimalValidator]),
        ),
        migrations.AlterField(
            model_name='r_rates',
            name='rev_KwhCommercialOp3',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, validators=[django.core.validators.DecimalValidator]),
        ),
        migrations.AlterField(
            model_name='r_rates',
            name='rev_KwhResidentialOp2',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, validators=[django.core.validators.DecimalValidator]),
        ),
        migrations.AlterField(
            model_name='r_rates',
            name='rev_KwhResidentialOp3',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, validators=[django.core.validators.DecimalValidator]),
        ),
        migrations.AlterField(
            model_name='r_rates',
            name='rev_kwhCommercialOp2',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, validators=[django.core.validators.DecimalValidator]),
        ),
    ]