# Generated by Django 3.2.7 on 2022-01-14 22:21

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0009_auto_20220113_2205'),
    ]

    operations = [
        migrations.CreateModel(
            name='R_Rates',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rev_FixedCostResidentialOp1', models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True, validators=[django.core.validators.DecimalValidator])),
                ('rev_FixedCostResidentialOp1Unit', models.CharField(blank=True, max_length=50, null=True)),
                ('rev_FixedCostCommercialOp1', models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True, validators=[django.core.validators.DecimalValidator])),
                ('rev_FixedCostCommercialOp1Unit', models.CharField(blank=True, max_length=50, null=True)),
                ('rev_KwhResidentialOp2', models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True, validators=[django.core.validators.DecimalValidator])),
                ('rev_KwhResidentialOp2Unit', models.CharField(blank=True, max_length=50, null=True)),
                ('rev_kwhCommercialOp2', models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True, validators=[django.core.validators.DecimalValidator])),
                ('rev_kwhCommercialOp2Unit', models.CharField(blank=True, max_length=50, null=True)),
                ('rev_FixedCostResidentialOp3', models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True, validators=[django.core.validators.DecimalValidator])),
                ('rev_FixedCostResidentialOp3Unit', models.CharField(blank=True, max_length=50, null=True)),
                ('rev_FixedCostCommercialOp3', models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True, validators=[django.core.validators.DecimalValidator])),
                ('rev_FixedCostCommercialOp3Unit', models.CharField(blank=True, max_length=50, null=True)),
                ('rev_KwhResidentialOp3', models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True, validators=[django.core.validators.DecimalValidator])),
                ('rev_KwhResidentialOp3Unit', models.CharField(blank=True, max_length=50, null=True)),
                ('rev_KwhCommercialOp3', models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True, validators=[django.core.validators.DecimalValidator])),
                ('rev_KwhCommercialOp3Unit', models.CharField(blank=True, max_length=50, null=True)),
                ('rev_Notes', models.TextField(blank=True, null=True)),
                ('rev_Source', models.TextField(blank=True, null=True)),
                ('rev_idProject', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.project')),
                ('rev_idUser', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='R_Options',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rev_FixedCostOp1', models.CharField(blank=True, max_length=50, null=True)),
                ('rev_KwhConsumpOp2', models.CharField(blank=True, max_length=50, null=True)),
                ('rev_FixedCostKwhOp3', models.CharField(blank=True, max_length=50, null=True)),
                ('rev_UnchargedResidentialOp3', models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True, validators=[django.core.validators.DecimalValidator])),
                ('rev_UnchargedResidentialOp3Unit', models.CharField(blank=True, max_length=50, null=True)),
                ('rev_UnchargedCommercialOp3', models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True, validators=[django.core.validators.DecimalValidator])),
                ('rev_UnchargedCommercialOp3Unit', models.CharField(blank=True, max_length=50, null=True)),
                ('rev_Notes', models.TextField(blank=True, null=True)),
                ('rev_Source', models.TextField(blank=True, null=True)),
                ('rev_idProject', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.project')),
                ('rev_idUser', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='R_Growth',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rev_ResidentialGrowth', models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True, validators=[django.core.validators.DecimalValidator])),
                ('rev_ResidentialGrowthUnit', models.CharField(blank=True, max_length=50, null=True)),
                ('rev_CommercialGrowth', models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True, validators=[django.core.validators.DecimalValidator])),
                ('rev_CommercialGrowthUnit', models.CharField(blank=True, max_length=50, null=True)),
                ('rev_Notes', models.TextField(blank=True, null=True)),
                ('rev_Source', models.TextField(blank=True, null=True)),
                ('rev_idProject', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.project')),
                ('rev_idUser', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='R_Changes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rev_FirstPriceRise', models.IntegerField(blank=True, null=True)),
                ('rev_SecondPriceRise', models.IntegerField(blank=True, null=True)),
                ('rev_ThirdPriceRise', models.IntegerField(blank=True, null=True)),
                ('rev_FourthPriceRise', models.IntegerField(blank=True, null=True)),
                ('rev_FifthPriceRise', models.IntegerField(blank=True, null=True)),
                ('rev_FirstYearPercentage', models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True, validators=[django.core.validators.DecimalValidator])),
                ('rev_SecondYearPercentage', models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True, validators=[django.core.validators.DecimalValidator])),
                ('rev_ThirdYearPercentage', models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True, validators=[django.core.validators.DecimalValidator])),
                ('rev_FourthYearPercentage', models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True, validators=[django.core.validators.DecimalValidator])),
                ('rev_FifthYearPercentage', models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True, validators=[django.core.validators.DecimalValidator])),
                ('rev_Notes', models.TextField(blank=True, null=True)),
                ('rev_Source', models.TextField(blank=True, null=True)),
                ('rev_idProject', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.project')),
                ('rev_idUser', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='R_Average',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rev_ResidentialConsump', models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True, validators=[django.core.validators.DecimalValidator])),
                ('rev_ResidentialConsumpUnit', models.CharField(blank=True, max_length=50, null=True)),
                ('rev_CommercialConsump', models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True, validators=[django.core.validators.DecimalValidator])),
                ('rev_CommercialConsumpUnit', models.CharField(blank=True, max_length=50, null=True)),
                ('rev_Notes', models.TextField(blank=True, null=True)),
                ('rev_Source', models.TextField(blank=True, null=True)),
                ('rev_idProject', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.project')),
                ('rev_idUser', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
