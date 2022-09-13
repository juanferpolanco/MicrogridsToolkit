from os import remove
from django.db.models import fields
from django.db.models.base import Model
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.forms.models import modelform_factory
from crispy_forms.helper import FormHelper

from .models import * 

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['prj_name', 'prj_description']
        labels = {
            'prj_name': 'Project Name',
            'prj_description': 'Description',
        }

class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']

class G_LocationDetailsForm(ModelForm):
    class Meta:
        model = G_LocationDetails
        fields = ['gen_idProject', 'gen_SettlementName', 'gen_StateName', 'gen_CountryName', 'gen_Currency', 'gen_Notes', 'gen_Source']
        labels = {
            'gen_SettlementName': 'Settlement Name',
            'gen_StateName': 'State Name',
            'gen_CountryName': 'Country Name',
            'gen_Currency': 'Currency',
            'gen_Notes': 'Notes',
            'gen_Source': 'Sources',
        }

class G_DemographyForm(ModelForm):
    class Meta:
        model = G_Demography
        fields = '__all__'

class G_IncomeForm(ModelForm):
    class Meta:
        model = G_Income
        fields = '__all__'

class G_FuelForm(ModelForm):
    class Meta:
        model = G_Fuel
        fields = '__all__'

class G_DiscountForm(ModelForm):
    class Meta:
        model = G_Discount
        fields = '__all__'

