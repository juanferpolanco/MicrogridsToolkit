# Generated by Django 3.2.7 on 2022-01-15 01:29

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0011_auto_20220114_1733'),
    ]

    operations = [
        migrations.CreateModel(
            name='CO2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('co2_CurrentFactor', models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True, validators=[django.core.validators.DecimalValidator])),
                ('co2_CurrentFactorUnit', models.CharField(blank=True, max_length=50, null=True)),
                ('co2_Diesel', models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True, validators=[django.core.validators.DecimalValidator])),
                ('co2_DieselUnit', models.CharField(blank=True, max_length=50, null=True)),
                ('co2_WoodLogs', models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True, validators=[django.core.validators.DecimalValidator])),
                ('co2_WoodLogsUnit', models.CharField(blank=True, max_length=50, null=True)),
                ('co2_Kerosene', models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True, validators=[django.core.validators.DecimalValidator])),
                ('co2_KeroseneUnit', models.CharField(blank=True, max_length=50, null=True)),
                ('co2_ProductionPerLitre', models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True, validators=[django.core.validators.DecimalValidator])),
                ('co2_ProductionPerLitreUnit', models.CharField(blank=True, max_length=50, null=True)),
                ('co2_EmissionCar', models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True, validators=[django.core.validators.DecimalValidator])),
                ('co2_EmissionCarUnit', models.CharField(blank=True, max_length=50, null=True)),
                ('co2_Notes', models.TextField(blank=True, null=True)),
                ('co2_Source', models.TextField(blank=True, null=True)),
                ('co2_idProject', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.project')),
                ('co2_idUser', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]