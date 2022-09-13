from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.contrib.auth import login
from .models import *
from django.views.generic import TemplateView, FormView
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.urls import reverse_lazy
from .encryptID import *

import math
from decimal import *
import numpy_financial as npf
from django.contrib import messages

# Create your views here.

class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('menu')
    
class MenuView(LoginRequiredMixin, TemplateView):
    template_name='base/menu.html'
    context_object_name = 'menu'

class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'base/changePassword.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('menu')

class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = CreateUserForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('menu')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('menu')
        return super(RegisterPage, self).get(*args, **kwargs)

#######        LIST PROJECTS      #######
@login_required(login_url='login')
def listProject(request):
    projects = Project.objects.filter(prj_user_id=request.user).order_by('id') #(-prj_datecreated) to invert order

    return render(request, 'base/projectList.html', {'projects':projects})


#######       CREATE PROJECTS     #######
@login_required(login_url='login')
def createProject(request):
    
    if request.method == 'POST':
        user = request.user
        name = request.POST['prj_name']
        desc = request.POST['prj_description']
        
        Project.objects.create(
            prj_user=User.objects.get(id = user.id),
            prj_name=name,
            prj_description=desc
        )
        
        messages.success(request,"Project created")
        return redirect('project-list')
    
    return render(request, 'base/projectCreate.html')


#######       EDIT PROJECTS       #######
@login_required(login_url='login')
def editProject(request, id):
    prj = Project.objects.get(id=id)

    if request.method == 'POST':

        name = request.POST['prj_name']
        description = request.POST['prj_description']

        prj = Project.objects.get(id=id)
        prj.prj_name = name
        prj.prj_description = description
        prj.save()
        
        messages.success(request,"Project edited")

        return redirect('project-list')

    return render(request, "base/projectEdit.html", {"prj":prj})


#######       DETAILS PROJECTS    #######
@login_required(login_url='login')
def projectDetails(request, id):
    
    context = {'id':id}
    
    return render(request, 'base/projectDetails.html', context)


#######       DELETE PROJECTS     #######

@login_required(login_url='login')
def deleteProject(request, id):
            
    """ prj = Project.objects.get(id=id)
    prj.delete()

    messages.success(request, "Project deleted")
    
    return redirect('project-list') """
    
    prj = Project.objects.get(id=id)

    if request.method == 'POST':

        prj.delete()

        messages.success(request, "Project deleted")

        return redirect('project-list')

    return render(request, "base/projectDelete.html", {"prj":prj})

########################################################       INPUT INTERFACES       ##############################################################


#####################################       GENERAL FUNCTIONS       #####################################
@login_required(login_url='login')
def general(request, id):
    
    context = {'id':id}

    #Get LocationDetails
    try:
        query = G_LocationDetails.objects.get(gen_idProject=id)
        context['queryLoc'] = query

    except G_LocationDetails.DoesNotExist:

        query = G_LocationDetails()

    #Get Demography
    try:
        query = G_Demography.objects.get(gen_idProject=id)
        context['queryDem'] = query

    except G_Demography.DoesNotExist:

        query = G_Demography()
    
    #Get Income
    try:
        query = G_Income.objects.get(gen_idProject=id)
        context['queryInc'] = query

    except G_Income.DoesNotExist:

        query = G_Income()
    
    #Get Current Fuel
    try:
        query = G_Fuel.objects.get(gen_idProject=id)
        context['queryFue'] = query

    except G_Fuel.DoesNotExist:

        query = G_Fuel()

    #Get Discount Rates
    try:
        query = G_Discount.objects.get(gen_idProject=id)
        context['queryDis'] = query

    except G_Discount.DoesNotExist:

        query = G_Discount()

    #Get Time
    try:
        query = G_Time.objects.get(gen_idProject=id)
        context['queryTim'] = query

    except G_Time.DoesNotExist:

        query = G_Time()

    #Get Tier
    try:
        query = G_Tier.objects.get(gen_idProject=id)
        context['queryTie'] = query

    except G_Tier.DoesNotExist:

        query = G_Tier()

    return render(request, 'base/inputGeneral.html', context)

@login_required(login_url='login')
def createG_LocationDetails(request, id):

    if request.method == 'POST':

        messages.success(request,"Information submitted")
        try:
            queryCurrency = G_LocationDetails.objects.get(gen_idProject = id)
            
            currency = queryCurrency.gen_Currency
        except  G_LocationDetails.DoesNotExist:
            currency = ''
        
        user = request.user
        obj, created = G_LocationDetails.objects.update_or_create(
            gen_idProject = Project.objects.get(id = id),
            defaults={'gen_idProject':Project.objects.get(id = id), 'gen_idUser':User.objects.get(id = user.id), 'gen_SettlementName': request.POST['gen_SettlementName'],
            'gen_StateName':request.POST['gen_StateName'], 'gen_CountryName':request.POST['gen_CountryName'], 'gen_Currency':request.POST['gen_Currency'],
            'gen_Notes':request.POST['gen_Notes'], 'gen_Source':request.POST['gen_Source']}
        )
        
        if(currency != request.POST['gen_Currency']):
            
            try:
                query = G_Income.objects.get(gen_idProject=id)
                
                residentialIncomeUnit = query.gen_ResidentialIncomeUnit
                residentialIncomeUnitSplitted = residentialIncomeUnit.split('/')
                residentialIncomeUnitSplitted.pop(0)
                residentialIncomeUnitSplitted.insert(0,request.POST['gen_Currency'])
                fixedresidentialIncomeUnit = '/'.join(residentialIncomeUnitSplitted)
                
                residentialWillingnessUnit = query.gen_ResidentialWillingnessUnit
                residentialWillingnessUnitSplitted = residentialWillingnessUnit.split('/')
                residentialWillingnessUnitSplitted.pop(0)
                residentialWillingnessUnitSplitted.insert(0,request.POST['gen_Currency'])
                fixedresidentialWillingnessUnit =  '/'.join(residentialWillingnessUnitSplitted)
                
                commercialIncomeUnit = query.gen_CommercialIncomeUnit
                commercialIncomeUnitSplitted = commercialIncomeUnit.split('/')
                commercialIncomeUnitSplitted.pop(0)
                commercialIncomeUnitSplitted.insert(0,request.POST['gen_Currency'])
                fixedcommercialIncomeUnit = '/'.join(commercialIncomeUnitSplitted)
                
                commercialWillingnessUnit = query.gen_CommercialWillingnessUnit
                commercialWillingnessUnitSplitted = commercialWillingnessUnit.split('/')
                commercialWillingnessUnitSplitted.pop(0)
                commercialWillingnessUnitSplitted.insert(0,request.POST['gen_Currency'])
                fixedcommercialWillingnessUnit = '/'.join(commercialWillingnessUnitSplitted)
                
            except:

                fixedresidentialIncomeUnit = (request.POST['gen_Currency'])
                fixedresidentialIncomeUnit = ''.join(fixedresidentialIncomeUnit)
                
                fixedresidentialWillingnessUnit = (request.POST['gen_Currency'])
                fixedresidentialWillingnessUnit = ''.join(fixedresidentialWillingnessUnit)
                
                fixedcommercialIncomeUnit = (request.POST['gen_Currency'])
                fixedcommercialIncomeUnit = ''.join(fixedcommercialIncomeUnit)
                
                fixedcommercialWillingnessUnit = (request.POST['gen_Currency'])
                fixedcommercialWillingnessUnit = ''.join(fixedcommercialWillingnessUnit)
                
            obj, created = G_Income.objects.update_or_create(
                gen_idProject = Project.objects.get(id = id),
                defaults={'gen_idProject':Project.objects.get(id = id), 'gen_idUser':User.objects.get(id = user.id),
                'gen_ResidentialIncomeUnit': fixedresidentialIncomeUnit, 'gen_ResidentialWillingnessUnit':fixedresidentialWillingnessUnit,
                'gen_CommercialIncomeUnit':fixedcommercialIncomeUnit, 'gen_CommercialWillingnessUnit':fixedcommercialWillingnessUnit,}
            )
            
            try:
                query = G_Fuel.objects.get(gen_idProject=id)
                
                residentialFuelCostUnit = query.gen_ResidentialFuelCostUnit
                residentialFuelCostUnitSplitted = residentialFuelCostUnit.split('/')
                residentialFuelCostUnitSplitted.pop(0)
                residentialFuelCostUnitSplitted.insert(0,request.POST['gen_Currency'])
                fixedresidentialFuelCostUnit = '/'.join(residentialFuelCostUnitSplitted)
                
                commercialFuelCostUnit = query.gen_CommercialFuelCostUnit
                commercialFuelCostUnitSplitted = commercialFuelCostUnit.split('/')
                commercialFuelCostUnitSplitted.pop(0)
                commercialFuelCostUnitSplitted.insert(0,request.POST['gen_Currency'])
                fixedcommercialFuelCostUnit =  '/'.join(commercialFuelCostUnitSplitted)
                
            except:

                fixedresidentialFuelCostUnit = (request.POST['gen_Currency'])
                
                fixedcommercialFuelCostUnit = (request.POST['gen_Currency'])
                
            obj, created = G_Fuel.objects.update_or_create(
                gen_idProject = Project.objects.get(id = id),
                defaults={'gen_idProject':Project.objects.get(id = id), 'gen_idUser':User.objects.get(id = user.id),
                 'gen_ResidentialFuelCostUnit':fixedresidentialFuelCostUnit, 'gen_CommercialFuelCostUnit': fixedcommercialFuelCostUnit}
            )
            
            obj, created = P_Capital.objects.update_or_create(
                pla_idProject = Project.objects.get(id = id),
                defaults={'pla_idProject':Project.objects.get(id = id), 'pla_idUser':User.objects.get(id = user.id),
                'pla_LandUnit': request.POST['gen_Currency'], 'pla_PanelsTurbinesUnit':request.POST['gen_Currency'],
                'pla_SwitchgearUnit':request.POST['gen_Currency'], 'pla_ProtectionSystemUnit':request.POST['gen_Currency'],
                'pla_TransformerUnit':request.POST['gen_Currency'], 'pla_WiringUnit':request.POST['gen_Currency'],
                'pla_MetersUnit':request.POST['gen_Currency'], 'pla_BatteriesUnit':request.POST['gen_Currency'],
                'pla_InvertersUnit':request.POST['gen_Currency'], 'pla_ControlCostUnit':request.POST['gen_Currency'],
                'pla_TransportationCostUnit':request.POST['gen_Currency'], 'pla_ConstructionCostUnit':request.POST['gen_Currency'],
                'pla_AncillaryCostUnit':request.POST['gen_Currency']}
            )
            
            try:
                query = P_Operational.objects.get(pla_idProject=id)
                
                operationalExpenditureUnit = query.pla_OperationalExpenditureUnit
                operationalExpenditureUnitSplitted = operationalExpenditureUnit.split('/')
                operationalExpenditureUnitSplitted.pop(0)
                operationalExpenditureUnitSplitted.insert(0,request.POST['gen_Currency'])
                fixedoperationalExpenditureUnit = '/'.join(operationalExpenditureUnitSplitted)
                
            except:

                fixedoperationalExpenditureUnit = (request.POST['gen_Currency'])
                fixedoperationalExpenditureUnit = ''.join(fixedoperationalExpenditureUnit)
                
            obj, created = P_Operational.objects.update_or_create(
                pla_idProject = Project.objects.get(id = id),
                defaults={'pla_idProject':Project.objects.get(id = id), 'pla_idUser':User.objects.get(id = user.id),
                 'pla_OperationalExpenditureUnit':fixedoperationalExpenditureUnit}
            )
        
            obj, created = P_Replacement.objects.update_or_create(
                pla_idProject = Project.objects.get(id = id),
                defaults={'pla_idProject':Project.objects.get(id = id), 'pla_idUser':User.objects.get(id = user.id),
                'pla_FirstTotalExpenditureUnit': request.POST['gen_Currency'], 'pla_FirstBatteriesCostUnit':request.POST['gen_Currency'],
                'pla_FirstBatteriesReplacedUnit':request.POST['gen_Currency'],
                'pla_SecondTotalExpenditureUnit':request.POST['gen_Currency'], 'pla_SecondBatteriesCostUnit':request.POST['gen_Currency'],
                'pla_SecondBatteriesReplacedUnit':request.POST['gen_Currency'],
                'pla_ThirdTotalExpenditureUnit':request.POST['gen_Currency'], 'pla_ThirdBatteriesCostUnit':request.POST['gen_Currency'],
                'pla_ThirdBatteriesReplacedUnit':request.POST['gen_Currency']}
            )
            
            try:
                query = R_Rates.objects.get(rev_idProject=id)
                
                costResidentialOp1Unit = query.rev_FixedCostResidentialOp1Unit
                costResidentialOp1UnitSplitted = costResidentialOp1Unit.split('/')
                costResidentialOp1UnitSplitted.pop(0)
                costResidentialOp1UnitSplitted.insert(0,request.POST['gen_Currency'])
                fixedResidentialOp1Unit = '/'.join(costResidentialOp1UnitSplitted)
                
                costCommercialOp1Unit = query.rev_FixedCostCommercialOp1Unit
                costCommercialOp1UnitSplitted = costCommercialOp1Unit.split('/')
                costCommercialOp1UnitSplitted.pop(0)
                costCommercialOp1UnitSplitted.insert(0,request.POST['gen_Currency'])
                fixedCommercialOp1Unit =  '/'.join(costCommercialOp1UnitSplitted)
                
                kwhResidentialOp2Unit = query.rev_KwhResidentialOp2Unit
                kwhResidentialOp2UnitSplitted = kwhResidentialOp2Unit.split('/')
                kwhResidentialOp2UnitSplitted.pop(0)
                kwhResidentialOp2UnitSplitted.insert(0,request.POST['gen_Currency'])
                fixedKwhResidentialOp2Unit = '/'.join(kwhResidentialOp2UnitSplitted)
                
                kwhCommercialOp2Unit = query.rev_kwhCommercialOp2Unit
                kwhCommercialOp2UnitSplitted = kwhCommercialOp2Unit.split('/')
                kwhCommercialOp2UnitSplitted.pop(0)
                kwhCommercialOp2UnitSplitted.insert(0,request.POST['gen_Currency'])
                fixedKwhCommercialOp2Unit = '/'.join(kwhCommercialOp2UnitSplitted)
                
                costResidentialOp3Unit = query.rev_FixedCostResidentialOp3Unit
                costResidentialOp3UnitSplitted = costResidentialOp3Unit.split('/')
                costResidentialOp3UnitSplitted.pop(0)
                costResidentialOp3UnitSplitted.insert(0,request.POST['gen_Currency'])
                fixedResidentialOp3Unit = '/'.join(costResidentialOp3UnitSplitted)
                
                costCommercialOp3Unit = query.rev_FixedCostCommercialOp3Unit
                costCommercialOp3UnitSplitted = costCommercialOp3Unit.split('/')
                costCommercialOp3UnitSplitted.pop(0)
                costCommercialOp3UnitSplitted.insert(0,request.POST['gen_Currency'])
                fixedCommercialOp3Unit ='/'.join(costCommercialOp3UnitSplitted)
                
                kwhResidentialOp3Unit = query.rev_KwhResidentialOp3Unit
                kwhResidentialOp3UnitSplitted = kwhResidentialOp3Unit.split('/')
                kwhResidentialOp3UnitSplitted.pop(0)
                kwhResidentialOp3UnitSplitted.insert(0,request.POST['gen_Currency'])
                fixedKwhResidentialOp3Unit = '/'.join(kwhResidentialOp3UnitSplitted)
                
                kwhCommercialOp3Unit = query.rev_KwhCommercialOp3Unit
                kwhCommercialOp3UnitSplitted = kwhCommercialOp3Unit.split('/')
                kwhCommercialOp3UnitSplitted.pop(0)
                kwhCommercialOp3UnitSplitted.insert(0,request.POST['gen_Currency'])
                fixedKwhCommercialOp3Unit = '/'.join(kwhCommercialOp3UnitSplitted)
                
            except:

                fixedResidentialOp1Unit = (request.POST['gen_Currency'])
                fixedResidentialOp1Unit = ''.join(fixedResidentialOp1Unit)
                
                fixedCommercialOp1Unit = (request.POST['gen_Currency'])
                fixedCommercialOp1Unit = ''.join(fixedCommercialOp1Unit)
                
                fixedKwhResidentialOp2Unit = (request.POST['gen_Currency'])
                fixedKwhResidentialOp2Unit = ''.join(fixedKwhResidentialOp2Unit)
                
                fixedKwhCommercialOp2Unit = (request.POST['gen_Currency'])
                fixedKwhCommercialOp2Unit = ''.join(fixedKwhCommercialOp2Unit)
                
                fixedResidentialOp3Unit = (request.POST['gen_Currency'])
                fixedResidentialOp3Unit = ''.join(fixedResidentialOp3Unit)
                
                fixedCommercialOp3Unit = (request.POST['gen_Currency'])
                fixedCommercialOp3Unit = ''.join(fixedCommercialOp3Unit)
                
                fixedKwhResidentialOp3Unit = (request.POST['gen_Currency'])
                fixedKwhResidentialOp3Unit = ''.join(fixedKwhResidentialOp3Unit)
                
                fixedKwhCommercialOp3Unit = (request.POST['gen_Currency'])
                fixedKwhCommercialOp3Unit = ''.join(fixedKwhCommercialOp3Unit)
                
            obj, created = R_Rates.objects.update_or_create(
                rev_idProject = Project.objects.get(id = id),
                defaults={'rev_idProject':Project.objects.get(id = id), 'rev_idUser':User.objects.get(id = user.id),
                'rev_FixedCostResidentialOp1Unit': fixedResidentialOp1Unit, 'rev_FixedCostCommercialOp1Unit':fixedCommercialOp1Unit,
                'rev_KwhResidentialOp2Unit':fixedKwhResidentialOp2Unit, 'rev_kwhCommercialOp2Unit':fixedKwhCommercialOp2Unit,
                'rev_FixedCostResidentialOp3Unit':fixedResidentialOp3Unit, 'rev_FixedCostCommercialOp3Unit':fixedCommercialOp3Unit,
                'rev_KwhResidentialOp3Unit':fixedKwhResidentialOp3Unit, 'rev_KwhCommercialOp3Unit':fixedKwhCommercialOp3Unit}
            )

    return redirect('general', id)

@login_required(login_url='login')
def createG_Demography(request, id):

    if request.method == 'POST':
        
        messages.success(request,"Information submitted")
        user = request.user
        obj, created = G_Demography.objects.update_or_create(
            gen_idProject = Project.objects.get(id = id),
            defaults={'gen_idProject':Project.objects.get(id = id),  'gen_idUser':User.objects.get(id = user.id), 'gen_PopulationSettlement': request.POST['gen_PopulationSettlement'], 'gen_PopulationSettlementUnit': request.POST['gen_PopulationSettlementUnit'],
            'gen_PopulationConnected':request.POST['gen_PopulationConnected'], 'gen_PopulationConnectedUnit':request.POST['gen_PopulationConnectedUnit'], 'gen_ResidentialProperties':request.POST['gen_ResidentialProperties'], 'gen_ResidentialPropertiesUnit':request.POST['gen_ResidentialPropertiesUnit'],
            'gen_ResidentialConnected':request.POST['gen_ResidentialConnected'], 'gen_ResidentialConnectedUnit':request.POST['gen_ResidentialConnectedUnit'], 'gen_CommercialProperties':request.POST['gen_CommercialProperties'], 'gen_CommercialPropertiesUnit':request.POST['gen_CommercialPropertiesUnit'],
            'gen_CommercialConnected':request.POST['gen_CommercialConnected'], 'gen_CommercialConnectedUnit':request.POST['gen_CommercialConnectedUnit'], 'gen_Notes':request.POST['gen_Notes'], 'gen_Source':request.POST['gen_Source']},
        )

    return redirect('general', id)

@login_required(login_url='login')
def createG_Income(request, id):

    if request.method == 'POST':
        
        messages.success(request,"Information submitted")
        user = request.user
        obj, created = G_Income.objects.update_or_create(
            gen_idProject = Project.objects.get(id = id),
            defaults={'gen_idProject':Project.objects.get(id = id),  'gen_idUser':User.objects.get(id = user.id), 'gen_ResidentialIncome': request.POST['gen_ResidentialIncome'], 'gen_ResidentialIncomeUnit': request.POST['gen_ResidentialIncomeUnit'],
            'gen_ResidentialWillingness':request.POST['gen_ResidentialWillingness'], 'gen_ResidentialWillingnessUnit':request.POST['gen_ResidentialWillingnessUnit'], 'gen_CommercialIncome':request.POST['gen_CommercialIncome'], 'gen_CommercialIncomeUnit':request.POST['gen_CommercialIncomeUnit'],
            'gen_CommercialWillingness':request.POST['gen_CommercialWillingness'], 'gen_CommercialWillingnessUnit':request.POST['gen_CommercialWillingnessUnit'], 'gen_Notes':request.POST['gen_Notes'], 'gen_Source':request.POST['gen_Source']},
        )

    return redirect('general', id)

@login_required(login_url='login')
def createG_Fuel(request, id):

    if request.method == 'POST':
        
        messages.success(request,"Information submitted")
        user = request.user
        obj, created = G_Fuel.objects.update_or_create(
            gen_idProject = Project.objects.get(id = id),
            defaults={'gen_idProject':Project.objects.get(id = id),  'gen_idUser':User.objects.get(id = user.id), 'gen_CommercialFuelUsed': request.POST['gen_CommercialFuelUsed'],
            'gen_CommercialFuelMonthly':request.POST['gen_CommercialFuelMonthly'], 'gen_CommercialFuelMonthlyUnit':request.POST['gen_CommercialFuelMonthlyUnit'], 'gen_CommercialFuelCost':request.POST['gen_CommercialFuelCost'],
            'gen_CommercialFuelCostUnit':request.POST['gen_CommercialFuelCostUnit'], 'gen_ResidentialFuelUsed':request.POST['gen_ResidentialFuelUsed'], 'gen_ResidentialFuelMonthly':request.POST['gen_ResidentialFuelMonthly'],
            'gen_ResidentialFuelMonthlyUnit':request.POST['gen_ResidentialFuelMonthlyUnit'], 'gen_ResidentialFuelCost':request.POST['gen_ResidentialFuelCost'], 'gen_ResidentialFuelCostUnit':request.POST['gen_ResidentialFuelCostUnit'],
            'gen_Notes':request.POST['gen_Notes'], 'gen_Source':request.POST['gen_Source']},
        )

    return redirect('general', id)

@login_required(login_url='login')
def createG_Discount(request, id):

    if request.method == 'POST':

        messages.success(request,"Information submitted")
        user = request.user
        obj, created = G_Discount.objects.update_or_create(
            gen_idProject = Project.objects.get(id = id),
            defaults={'gen_idProject':Project.objects.get(id = id),  'gen_idUser':User.objects.get(id = user.id),
            'gen_DiscountRate': request.POST['gen_DiscountRate'], 'gen_DiscountRateUnit': request.POST['gen_DiscountRateUnit'],
            'gen_Notes':request.POST['gen_Notes'], 'gen_Source':request.POST['gen_Source']},
        )

    return redirect('general', id)

@login_required(login_url='login')
def createG_Time(request, id):

    if request.method == 'POST':

        messages.success(request,"Information submitted")
        user = request.user
        obj, created = G_Time.objects.update_or_create(
            gen_idProject = Project.objects.get(id = id),
            defaults={'gen_idProject':Project.objects.get(id = id),  'gen_idUser':User.objects.get(id = user.id), 'gen_StartingYear': request.POST['gen_StartingYear'],
            'gen_ProjectionPeriod':request.POST['gen_ProjectionPeriod'], 'gen_ProjectionPeriodUnit':request.POST['gen_ProjectionPeriodUnit'], 
            'gen_MonthsNumber':request.POST['gen_MonthsNumber'], 'gen_MonthsNumberUnit':request.POST['gen_MonthsNumberUnit'],
            'gen_Notes':request.POST['gen_Notes'], 'gen_Source':request.POST['gen_Source']},
        )

    return redirect('general', id)

@login_required(login_url='login')
def createG_Tier(request, id):

    if request.method == 'POST':

        messages.success(request,"Information submitted")
        user = request.user
        obj, created = G_Tier.objects.update_or_create(
            gen_idProject = Project.objects.get(id = id),
            defaults={'gen_idProject':Project.objects.get(id = id),  'gen_idUser':User.objects.get(id = user.id),
            'gen_WorldBankTier': request.POST['gen_WorldBankTier'], 'gen_WorldBankTierUnit': request.POST['gen_WorldBankTierUnit'],
             'gen_Notes':request.POST['gen_Notes'], 'gen_Source':request.POST['gen_Source']},
        )

    return redirect('general', id)


#####################################       PLANT EXPENDITURE FUNCTIONS       #####################################
@login_required(login_url='login')
def plantExpenditure(request, id):

    context = {'id':id}

    #GET CURRENCY FOR UNIT FIELDS
    try:
        currency = G_LocationDetails.objects.get(gen_idProject = id)

        if currency.gen_Currency == '':
            context['currency'] = ("Currency have not been setted")
        else:
            context['currency'] = currency.gen_Currency

    except G_LocationDetails.DoesNotExist:

        context['currency'] = ("Currency have not been setted")

    #GET Details
    try:
        query = P_Details.objects.get(pla_idProject=id)
        context['queryDet'] = query

    except P_Details.DoesNotExist:

        query = P_Details()
    
    #GET Capital
    try:
        query = P_Capital.objects.get(pla_idProject=id)
        context['queryCap'] = query

    except P_Capital.DoesNotExist:

        query = P_Capital()
    
    #Get Operational
    try:
        query = P_Operational.objects.get(pla_idProject=id)
        context['queryOpe'] = query

    except P_Operational.DoesNotExist:

        query = P_Operational()
    
    #Get Replacement
    try:
        query = P_Replacement.objects.get(pla_idProject=id)
        context['queryRep'] = query

    except P_Replacement.DoesNotExist:

        query = P_Replacement()
    
    #Get Subsidy
    try:
        query = P_Subsidy.objects.get(pla_idProject=id)
        context['querySub'] = query

    except P_Subsidy.DoesNotExist:

        query = P_Subsidy()
    
    return render(request, 'base/inputPlantExpenditure.html', context)

@login_required(login_url='login')
def createP_Details(request, id):

    if request.method == 'POST':

        messages.success(request,"Information submitted")
        user = request.user
        obj, created = P_Details.objects.update_or_create(
            pla_idProject = Project.objects.get(id = id),
            defaults={'pla_idProject':Project.objects.get(id = id),  'pla_idUser':User.objects.get(id = user.id), 'pla_PlantSize': request.POST['pla_PlantSize'],
            'pla_PlantSizeUnit': request.POST['pla_PlantSizeUnit'], 'pla_BatterySize':request.POST['pla_BatterySize'],
            'pla_BatterySizeUnit':request.POST['pla_BatterySizeUnit'], 'pla_AnnualDegradation':request.POST['pla_AnnualDegradation'],
            'pla_AnnualDegradationUnit':request.POST['pla_AnnualDegradationUnit'], 'pla_DailyGeneration':request.POST['pla_DailyGeneration'],
            'pla_DailyGenerationUnit':request.POST['pla_DailyGenerationUnit'], 'pla_Notes':request.POST['pla_Notes'], 'pla_Source':request.POST['pla_Source']},
        )

    return redirect('plantExpenditure', id)

@login_required(login_url='login')
def createP_Capital(request, id):

    if request.method == 'POST':

        messages.success(request,"Information submitted")
        user = request.user
        obj, created = P_Capital.objects.update_or_create(
            pla_idProject = Project.objects.get(id = id),
            defaults={'pla_idProject':Project.objects.get(id = id),  'pla_idUser':User.objects.get(id = user.id), 'pla_Land': request.POST['pla_Land'],
            'pla_LandUnit': request.POST['pla_LandUnit'], 'pla_PanelsTurbines':request.POST['pla_PanelsTurbines'], 'pla_PanelsTurbinesUnit':request.POST['pla_PanelsTurbinesUnit'],
            'pla_Switchgear':request.POST['pla_Switchgear'], 'pla_SwitchgearUnit':request.POST['pla_SwitchgearUnit'], 'pla_ProtectionSystem':request.POST['pla_ProtectionSystem'],
            'pla_ProtectionSystemUnit':request.POST['pla_ProtectionSystemUnit'], 'pla_Transformer':request.POST['pla_Transformer'], 'pla_TransformerUnit':request.POST['pla_TransformerUnit'],
            'pla_Wiring':request.POST['pla_Wiring'], 'pla_WiringUnit':request.POST['pla_WiringUnit'], 'pla_Meters':request.POST['pla_Meters'],
            'pla_MetersUnit':request.POST['pla_MetersUnit'], 'pla_Batteries':request.POST['pla_Batteries'], 'pla_BatteriesUnit':request.POST['pla_BatteriesUnit'],
            'pla_Inverters':request.POST['pla_Inverters'], 'pla_InvertersUnit':request.POST['pla_InvertersUnit'], 'pla_ControlCost':request.POST['pla_ControlCost'],
            'pla_ControlCostUnit':request.POST['pla_ControlCostUnit'], 'pla_TransportationCost':request.POST['pla_TransportationCost'],
            'pla_TransportationCostUnit':request.POST['pla_TransportationCostUnit'], 'pla_ConstructionCost':request.POST['pla_ConstructionCost'],
            'pla_ConstructionCostUnit':request.POST['pla_ConstructionCostUnit'], 'pla_AncillaryCost':request.POST['pla_AncillaryCost'],
            'pla_AncillaryCostUnit':request.POST['pla_AncillaryCostUnit'], 'pla_InstallationCost':request.POST['pla_InstallationCost'],
            'pla_InstallationCostUnit':request.POST['pla_InstallationCostUnit'], 'pla_Notes':request.POST['pla_Notes'], 'pla_Source':request.POST['pla_Source']},
        )

    return redirect('plantExpenditure', id)

@login_required(login_url='login')
def createP_Operational(request, id):

    if request.method == 'POST':

        messages.success(request,"Information submitted")
        user = request.user
        obj, created = P_Operational.objects.update_or_create(
            pla_idProject = Project.objects.get(id = id),
            defaults={'pla_idProject':Project.objects.get(id = id),  'pla_idUser':User.objects.get(id = user.id),
            'pla_OperationalExpenditure': request.POST['pla_OperationalExpenditure'], 'pla_OperationalExpenditureUnit': request.POST['pla_OperationalExpenditureUnit'],
            'pla_OMEscalator':request.POST['pla_OMEscalator'], 'pla_OMEscalatorUnit':request.POST['pla_OMEscalatorUnit'],
            'pla_Notes':request.POST['pla_Notes'], 'pla_Source':request.POST['pla_Source']},
        )

    return redirect('plantExpenditure', id)

@login_required(login_url='login')
def createP_Replacement(request, id):

    if request.method == 'POST':

        messages.success(request,"Information submitted")
        user = request.user
        obj, created = P_Replacement.objects.update_or_create(
            pla_idProject = Project.objects.get(id = id),
            defaults={'pla_idProject':Project.objects.get(id = id),  'pla_idUser':User.objects.get(id = user.id), 
            
            'pla_FirstExpansion': request.POST['pla_FirstExpansion'],
            'pla_SecondExpansion':request.POST['pla_SecondExpansion'], 'pla_ThirdExpansion':request.POST['pla_ThirdExpansion'], 

            'pla_FirstPlantAdded':request.POST['pla_FirstPlantAdded'], 'pla_FirstPlantAddedUnit':request.POST['pla_FirstPlantAddedUnit'],
            'pla_FirstTotalExpenditure':request.POST['pla_FirstTotalExpenditure'], 'pla_FirstTotalExpenditureUnit':request.POST['pla_FirstTotalExpenditureUnit'], 
            'pla_FirstBatteriesSize':request.POST['pla_FirstBatteriesSize'], 'pla_FirstBatteriesSizeUnit':request.POST['pla_FirstBatteriesSizeUnit'],
            'pla_FirstBatteriesCost':request.POST['pla_FirstBatteriesCost'], 'pla_FirstBatteriesCostUnit':request.POST['pla_FirstBatteriesCostUnit'],
            'pla_FirstBatteriesReplaced':request.POST['pla_FirstBatteriesReplaced'], 'pla_FirstBatteriesReplacedUnit':request.POST['pla_FirstBatteriesReplacedUnit'],
            'pla_FirstHomesAdded':request.POST['pla_FirstHomesAdded'], 'pla_FirstCommercialAdded':request.POST['pla_FirstCommercialAdded'],
            
            'pla_SecondPlantAdded':request.POST['pla_SecondPlantAdded'], 'pla_SecondPlantAddedUnit':request.POST['pla_SecondPlantAddedUnit'], 
            'pla_SecondTotalExpenditure':request.POST['pla_SecondTotalExpenditure'], 'pla_SecondTotalExpenditureUnit':request.POST['pla_SecondTotalExpenditureUnit'],
            'pla_SecondBatteriesSize':request.POST['pla_SecondBatteriesSize'], 'pla_SecondBatteriesSizeUnit':request.POST['pla_SecondBatteriesSizeUnit'], 
            'pla_SecondBatteriesCost':request.POST['pla_SecondBatteriesCost'], 'pla_SecondBatteriesCostUnit':request.POST['pla_SecondBatteriesCostUnit'],
            'pla_SecondBatteriesReplaced':request.POST['pla_SecondBatteriesReplaced'], 'pla_SecondBatteriesReplacedUnit':request.POST['pla_SecondBatteriesReplacedUnit'],
            'pla_SecondHomesAdded':request.POST['pla_SecondHomesAdded'], 'pla_SecondCommercialAdded':request.POST['pla_SecondCommercialAdded'],

            'pla_ThirdPlantAdded':request.POST['pla_ThirdPlantAdded'], 'pla_ThirdPlantAddedUnit':request.POST['pla_ThirdPlantAddedUnit'],
            'pla_ThirdTotalExpenditure':request.POST['pla_ThirdTotalExpenditure'], 'pla_ThirdTotalExpenditureUnit':request.POST['pla_ThirdTotalExpenditureUnit'], 
            'pla_ThirdBatteriesSize':request.POST['pla_ThirdBatteriesSize'], 'pla_ThirdBatteriesSizeUnit':request.POST['pla_ThirdBatteriesSizeUnit'],
            'pla_ThirdBatteriesCost':request.POST['pla_ThirdBatteriesCost'], 'pla_ThirdBatteriesCostUnit':request.POST['pla_ThirdBatteriesCostUnit'],
            'pla_ThirdBatteriesReplaced':request.POST['pla_ThirdBatteriesReplaced'], 'pla_ThirdBatteriesReplacedUnit':request.POST['pla_ThirdBatteriesReplacedUnit'], 
            'pla_ThirdHomesAdded':request.POST['pla_ThirdHomesAdded'], 'pla_ThirdCommercialAdded':request.POST['pla_ThirdCommercialAdded'], 
            
            'pla_Notes':request.POST['pla_Notes'], 'pla_Source':request.POST['pla_Source']},
        )
        #THIS GOES BEFORE pla_FirstExpansion
        """ 'pla_NumberExpansions': request.POST['pla_NumberExpansions'], """

    return redirect('plantExpenditure', id)

@login_required(login_url='login')
def createP_Subsidy(request, id):

    if request.method == 'POST':

        messages.success(request,"Information submitted")
        user = request.user
        obj, created = P_Subsidy.objects.update_or_create(
            pla_idProject = Project.objects.get(id = id),
            defaults={'pla_idProject':Project.objects.get(id = id),  'pla_idUser':User.objects.get(id = user.id), 
            'pla_SubsidyCapital': request.POST['pla_SubsidyCapital'], 
            'pla_SubsidyCapitalUnit': request.POST['pla_SubsidyCapitalUnit'],
            'pla_SubsidyOperational':request.POST['pla_SubsidyOperational'], 
            'pla_SubsidyOperationalUnit':request.POST['pla_SubsidyOperationalUnit'], 
            'pla_SubsidyReplacement':request.POST['pla_SubsidyReplacement'], 
            'pla_SubsidyReplacementUnit':request.POST['pla_SubsidyReplacementUnit'],
            'pla_Notes':request.POST['pla_Notes'], 'pla_Source':request.POST['pla_Source']},
        )

    return redirect('plantExpenditure', id)


#####################################       REVENUE ELECTRICITY FUNCTIONS       #####################################
@login_required(login_url='login')
def revenueElectricity(request, id):

    context = {'id':id}

    #Get Currency FROM LocationDetails
    try:
        currency = G_LocationDetails.objects.get(gen_idProject = id)
        
        context['currency'] = currency.gen_Currency

    except G_LocationDetails.DoesNotExist:

        context['currency'] = ''
    
    #GET Average
    try:
        query = R_Average.objects.get(rev_idProject=id)
        context['queryAve'] = query

    except R_Average.DoesNotExist:

        query = R_Average()
    
     #GET Growth
    try:
        query = R_Growth.objects.get(rev_idProject=id)
        context['queryGro'] = query

    except R_Growth.DoesNotExist:

        query = R_Growth()
    
     #GET Options
    try:
        query = R_Options.objects.get(rev_idProject=id)
        context['queryOpt'] = query

    except R_Options.DoesNotExist:

        query = R_Options()
    
     #GET Rates
    try:
        query = R_Rates.objects.get(rev_idProject=id)
        context['queryRat'] = query
        
        
        """ costResidentialOp1Unit = query.rev_FixedCostResidentialOp1Unit
        costResidentialOp1UnitSplitted = costResidentialOp1Unit.split('/')
        costResidentialOp1UnitSplitted.pop(0)
        context['fixedResidentialOp1Unit'] = '/'.join(costResidentialOp1UnitSplitted)
        
        costCommercialOp1Unit = query.rev_FixedCostCommercialOp1Unit
        costCommercialOp1UnitSplitted = costCommercialOp1Unit.split('/')
        costCommercialOp1UnitSplitted.pop(0)
        context['fixedCommercialOp1Unit'] = '/'.join(costCommercialOp1UnitSplitted)
        
        kwhResidentialOp2Unit = query.rev_KwhResidentialOp2Unit
        kwhResidentialOp2UnitSplitted = kwhResidentialOp2Unit.split('/')
        kwhResidentialOp2UnitSplitted.pop(0)
        context['fixedKwhResidentialOp2Unit'] = '/'.join(kwhResidentialOp2UnitSplitted)
        
        kwhCommercialOp2Unit = query.rev_kwhCommercialOp2Unit
        kwhCommercialOp2UnitSplitted = kwhCommercialOp2Unit.split('/')
        kwhCommercialOp2UnitSplitted.pop(0)
        context['fixedKwhCommercialOp2Unit'] = '/'.join(kwhCommercialOp2UnitSplitted)
        
        costResidentialOp3Unit = query.rev_FixedCostResidentialOp3Unit
        costResidentialOp3UnitSplitted = costResidentialOp3Unit.split('/')
        costResidentialOp3UnitSplitted.pop(0)
        context['fixedResidentialOp3Unit'] = '/'.join(costResidentialOp3UnitSplitted)
        
        costCommercialOp3Unit = query.rev_FixedCostCommercialOp3Unit
        costCommercialOp3UnitSplitted = costCommercialOp3Unit.split('/')
        costCommercialOp3UnitSplitted.pop(0)
        context['fixedCommercialOp3Unit'] = '/'.join(costCommercialOp3UnitSplitted)
        
        kwhResidentialOp3Unit = query.rev_KwhResidentialOp3Unit
        kwhResidentialOp3UnitSplitted = kwhResidentialOp3Unit.split('/')
        kwhResidentialOp3UnitSplitted.pop(0)
        context['fixedKwhResidentialOp3Unit'] = '/'.join(kwhResidentialOp3UnitSplitted)
        
        kwhCommercialOp3Unit = query.rev_KwhCommercialOp3Unit
        kwhCommercialOp3UnitSplitted = kwhCommercialOp3Unit.split('/')
        kwhCommercialOp3UnitSplitted.pop(0)
        context['fixedKwhCommercialOp3Unit'] = '/'.join(kwhCommercialOp3UnitSplitted) """
        
    except R_Rates.DoesNotExist:

        query = R_Rates()
    
     #GET Changes
    try:
        query = R_Changes.objects.get(rev_idProject=id)
        context['queryCha'] = query

    except R_Changes.DoesNotExist:

        query = R_Changes()

    return render(request, 'base/inputRevenueElectricity.html', context)

@login_required(login_url='login')
def createR_Average(request, id):

    if request.method == 'POST':

        messages.success(request,"Information submitted")
        user = request.user
        obj, created = R_Average.objects.update_or_create(
            rev_idProject = Project.objects.get(id = id),
            defaults={'rev_idProject':Project.objects.get(id = id),  'rev_idUser':User.objects.get(id = user.id), 
            'rev_ResidentialConsump': request.POST['rev_ResidentialConsump'],'rev_ResidentialConsumpUnit':request.POST['rev_ResidentialConsumpUnit'],
            'rev_CommercialConsump':request.POST['rev_CommercialConsump'], 'rev_CommercialConsumpUnit':request.POST['rev_CommercialConsumpUnit'],
            'rev_Notes':request.POST['rev_Notes'], 'rev_Source':request.POST['rev_Source']},
        )
    return redirect('revenueElectricity', id)

@login_required(login_url='login')
def createR_Growth(request, id):

    if request.method == 'POST':

        messages.success(request,"Information submitted")
        user = request.user
        obj, created = R_Growth.objects.update_or_create(
            rev_idProject = Project.objects.get(id = id),
            defaults={'rev_idProject':Project.objects.get(id = id),  'rev_idUser':User.objects.get(id = user.id), 
            'rev_ResidentialGrowth': request.POST['rev_ResidentialGrowth'],'rev_ResidentialGrowthUnit':request.POST['rev_ResidentialGrowthUnit'],
            'rev_CommercialGrowth':request.POST['rev_CommercialGrowth'], 'rev_CommercialGrowthUnit':request.POST['rev_CommercialGrowthUnit'],
            'rev_Notes':request.POST['rev_Notes'], 'rev_Source':request.POST['rev_Source']},
        )
    return redirect('revenueElectricity', id)

@login_required(login_url='login')
def createR_Options(request, id):
    
    if request.method == 'POST':

        messages.success(request,"Information submitted")
        user = request.user
        obj, created = R_Options.objects.update_or_create(
            rev_idProject = Project.objects.get(id = id),
            defaults={'rev_idProject':Project.objects.get(id = id),  'rev_idUser':User.objects.get(id = user.id),
            
            'rev_UnchargedResidentialOp3':request.POST['rev_UnchargedResidentialOp3'], 'rev_UnchargedResidentialOp3Unit':request.POST['rev_UnchargedResidentialOp3Unit'],
            'rev_UnchargedCommercialOp3':request.POST['rev_UnchargedCommercialOp3'], 'rev_UnchargedCommercialOp3Unit':request.POST['rev_UnchargedCommercialOp3Unit'],
            'rev_Notes':request.POST['rev_Notes'], 'rev_Source':request.POST['rev_Source']},
        )
        
        """ print("SOME",request.POST['rev_FixedCostOp1']) """
    #THIS GOES BEFORE "rev_UnchargedResidentialOp3"
    """     'rev_FixedCostOp1':request.POST['rev_FixedCostOp1'],
            'rev_KwhConsumpOp2':request.POST['rev_KwhConsumpOp2'],
            'rev_FixedCostKwhOp3':request.POST['rev_FixedCostKwhOp3'], """

    return redirect('revenueElectricity', id)

@login_required(login_url='login')
def createR_Rates(request, id):

    if request.method == 'POST':
        
        messages.success(request,"Information submitted")
        user = request.user
        obj, created = R_Rates.objects.update_or_create(
            rev_idProject = Project.objects.get(id = id),
            defaults={'rev_idProject':Project.objects.get(id = id),  'rev_idUser':User.objects.get(id = user.id), 
            'rev_FixedCostResidentialOp1': request.POST['rev_FixedCostResidentialOp1'], 'rev_FixedCostResidentialOp1Unit': request.POST['rev_FixedCostResidentialOp1Unit'],
            'rev_FixedCostCommercialOp1':request.POST['rev_FixedCostCommercialOp1'], 'rev_FixedCostCommercialOp1Unit':request.POST['rev_FixedCostCommercialOp1Unit'], 
            'rev_KwhResidentialOp2':request.POST['rev_KwhResidentialOp2'], 'rev_KwhResidentialOp2Unit':request.POST['rev_KwhResidentialOp2Unit'],
            'rev_kwhCommercialOp2':request.POST['rev_kwhCommercialOp2'], 'rev_kwhCommercialOp2Unit':request.POST['rev_kwhCommercialOp2Unit'],
            'rev_FixedCostResidentialOp3':request.POST['rev_FixedCostResidentialOp3'], 'rev_FixedCostResidentialOp3Unit':request.POST['rev_FixedCostResidentialOp3Unit'],
            'rev_FixedCostCommercialOp3':request.POST['rev_FixedCostCommercialOp3'], 'rev_FixedCostCommercialOp3Unit':request.POST['rev_FixedCostCommercialOp3Unit'],
            'rev_KwhResidentialOp3':request.POST['rev_KwhResidentialOp3'], 'rev_KwhResidentialOp3Unit':request.POST['rev_KwhResidentialOp3Unit'],
            'rev_KwhCommercialOp3':request.POST['rev_KwhCommercialOp3'], 'rev_KwhCommercialOp3Unit':request.POST['rev_KwhCommercialOp3Unit'],
            'rev_Notes':request.POST['rev_Notes'], 'rev_Source':request.POST['rev_Source']},
        )        
    return redirect('revenueElectricity', id)

@login_required(login_url='login')
def createR_Changes(request, id):

    if request.method == 'POST':

        messages.success(request,"Information submitted")
        user = request.user
        obj, created = R_Changes.objects.update_or_create(
            rev_idProject = Project.objects.get(id = id),
            defaults={'rev_idProject':Project.objects.get(id = id),  'rev_idUser':User.objects.get(id = user.id), 
            'rev_FirstPriceRise': request.POST['rev_FirstPriceRise'], 'rev_SecondPriceRise': request.POST['rev_SecondPriceRise'],
            'rev_ThirdPriceRise':request.POST['rev_ThirdPriceRise'], 'rev_FourthPriceRise':request.POST['rev_FourthPriceRise'], 
            'rev_FifthPriceRise':request.POST['rev_FifthPriceRise'], 'rev_FirstYearPercentage':request.POST['rev_FirstYearPercentage'],
            'rev_SecondYearPercentage':request.POST['rev_SecondYearPercentage'], 'rev_ThirdYearPercentage':request.POST['rev_ThirdYearPercentage'],
            'rev_FourthYearPercentage':request.POST['rev_FourthYearPercentage'], 'rev_FifthYearPercentage':request.POST['rev_FifthYearPercentage'],
            'rev_Notes':request.POST['rev_Notes'], 'rev_Source':request.POST['rev_Source']},
        )
    return redirect('revenueElectricity', id)


#####################################       CO2 FUNCTIONS       #####################################
@login_required(login_url='login')
def co2(request, id):

    context = {'id':id}

    #GET Co2
    try:
        query = CO2.objects.get(co2_idProject=id)
        context['queryCo2'] = query

    except CO2.DoesNotExist:

        query = CO2()

    return render(request, 'base/inputCo2.html', context)

@login_required(login_url='login')
def createCo2(request, id):

    if request.method == 'POST':

        messages.success(request,"Information submitted")
        user = request.user
        obj, created = CO2.objects.update_or_create(
            co2_idProject = Project.objects.get(id = id),
            defaults={'co2_idProject':Project.objects.get(id = id),  'co2_idUser':User.objects.get(id = user.id), 
            'co2_CurrentFactor': request.POST['co2_CurrentFactor'],'co2_CurrentFactorUnit':request.POST['co2_CurrentFactorUnit'],
            'co2_Diesel':request.POST['co2_Diesel'], 'co2_DieselUnit':request.POST['co2_DieselUnit'],
            'co2_WoodLogs':request.POST['co2_WoodLogs'], 'co2_WoodLogsUnit':request.POST['co2_WoodLogsUnit'],
            'co2_Kerosene':request.POST['co2_Kerosene'], 'co2_KeroseneUnit':request.POST['co2_KeroseneUnit'],
            'co2_ProductionPerLitre':request.POST['co2_ProductionPerLitre'], 'co2_ProductionPerLitreUnit':request.POST['co2_ProductionPerLitreUnit'],
            'co2_EmissionCar':request.POST['co2_EmissionCar'], 'co2_EmissionCarUnit':request.POST['co2_EmissionCarUnit'],
            'co2_Notes':request.POST['co2_Notes'], 'co2_Source':request.POST['co2_Source']},
        )

    return redirect('co2', id)


########################################################       OUTPUT INTERFACES       ##############################################################

@login_required(login_url='login')
def resultsOverview(request, id):

    context = {'id':id}

    #GET DATA FOR: Project Name
    # Project
    objProject = Project.objects.get(id = id)

    prjName = objProject.prj_name

    context['prjName'] = prjName

    #GET DATA FOR: Key Scenario Info
    # LocationDetails
    try:

        objLocationDetails = G_LocationDetails.objects.get(gen_idProject = id)
        objTime = G_Time.objects.get(gen_idProject = id)
        objDiscount = G_Discount.objects.get(gen_idProject = id)
        objDemography = G_Demography.objects.get(gen_idProject = id)

        results = True

    except:

        results = False
    
    if(results):
        settlementName = objLocationDetails.gen_SettlementName
        stateName = objLocationDetails.gen_StateName
        country = objLocationDetails.gen_CountryName
        currency = objLocationDetails.gen_Currency
        
        startingYear = objTime.gen_StartingYear
        projectionPeriod = objTime.gen_ProjectionPeriod
        projectionPeriodUnit = objTime.gen_ProjectionPeriodUnit
        
        discountRate = objDiscount.gen_DiscountRate
        discountRateUnit = objDiscount.gen_DiscountRateUnit
        
        residentialProperties = objDemography.gen_ResidentialProperties
        residentialPropertiesUnit = objDemography.gen_ResidentialPropertiesUnit
        residentialConnected = objDemography.gen_ResidentialConnected
        residentialConnectedUnit = objDemography.gen_ResidentialConnectedUnit
        commercialProperties = objDemography.gen_CommercialProperties
        commercialPropertiesUnit = objDemography.gen_CommercialPropertiesUnit
        commercialConnected = objDemography.gen_CommercialConnected
        commercialConnectedUnit = objDemography.gen_CommercialConnectedUnit

        context['settlementName'] = settlementName
        context['stateName'] = stateName
        context['country'] = country
        context['currency'] = currency
        
        context['startingYear'] = startingYear
        context['projectionPeriod'] = projectionPeriod
        context['projectionPeriodUnit'] = projectionPeriodUnit
        
        context['discountRate'] = round(discountRate,2)
        context['discountRateUnit'] = discountRateUnit
        
        context['residentialProperties'] = "{:,}".format(residentialProperties)
        context['residentialPropertiesUnit'] = residentialPropertiesUnit
        context['residentialConnected'] = "{:,}".format(residentialConnected)
        context['residentialConnectedUnit'] = residentialConnectedUnit
        context['commercialProperties'] = "{:,}".format(commercialProperties)
        context['commercialPropertiesUnit'] = commercialPropertiesUnit
        context['commercialConnected'] = "{:,}".format(commercialConnected)
        context['commercialConnectedUnit'] = commercialConnectedUnit

        #GET DATA FOR: Year-1 Connections GRAPHS
        #  Graph
        residentialNotConnected = residentialProperties - residentialConnected
        context['residentialNotConnected'] = residentialNotConnected
        # Second Graph
        commercialNotConnected = commercialProperties - commercialConnected
        context['commercialNotConnected'] = commercialNotConnected
    
    return render(request, 'base/resultsOverview.html', context)

@login_required(login_url='login')
def resultsCarbon(request, id):

    context = {'id':id}

#GET DATA FOR: Project Name
    # Project
    objProject = Project.objects.get(id = id)

    prjName = objProject.prj_name

    context['prjName'] = prjName

    try:
        objCo2 = CO2.objects.get(co2_idProject = id)
        objFuel = G_Fuel.objects.get(gen_idProject = id)
        objTime = G_Time.objects.get(gen_idProject = id)
        objReplacement = P_Replacement.objects.get(pla_idProject = id)
        objDemography = G_Demography.objects.get(gen_idProject = id)
        objAverage = R_Average.objects.get(rev_idProject = id)
        objGrowth = R_Growth.objects.get(rev_idProject = id)
        
        results = True
        
    except:
        results = False
    
    if(results):
        #Global and views values or units
        residentialFuelUsed =  objFuel.gen_ResidentialFuelUsed #Residential Fuel
        commercialFuelUsed =  objFuel.gen_CommercialFuelUsed #Commercial Fuel
        emissionCarUnit = objCo2.co2_EmissionCarUnit #Unit for show in results
        startingYear = objTime.gen_StartingYear #2020
        keroseneConstant = objCo2.co2_Kerosene #Kerosen constant(0.260)
        woodLogsConstant = objCo2.co2_WoodLogs #Wodd logs constant (52.14)
        dieselConstant = objCo2.co2_Diesel #Diesel constant (2.687)

        context['residentialFuel'] = residentialFuelUsed
        context['commercialFuel'] = commercialFuelUsed
        context['emissionCarUnit'] = emissionCarUnit
        #Global and views values or units
        
    #GET DATA FOR: Emission Results Vs. Current Fuel
        #Data For Calc
        
        projectionPeriod = objTime.gen_ProjectionPeriod #20
        yearFirstExpansion = objReplacement.pla_FirstExpansion #2029
        yearSecondExpansion = objReplacement.pla_SecondExpansion #2039
        yearThirdExpansion = objReplacement.pla_ThirdExpansion #...
        monthsNumber = objTime.gen_MonthsNumber #12
        
        kWhProducedBurned = objCo2.co2_ProductionPerLitre #10.35
        emissionCar = objCo2.co2_EmissionCar #4600
        estimatedConsumpResidential = objAverage.rev_ResidentialConsump #100
        estimatedConsumpCommercial = objAverage.rev_CommercialConsump #100
        growthResidential = (objGrowth.rev_ResidentialGrowth / 100) #0.01
        growthCommercial = (objGrowth.rev_CommercialGrowth / 100) #0.01
        carbonFactor = objCo2.co2_CurrentFactor #0.5

        #Number of residentials (Expansion)
        residentialConnected = objDemography.gen_ResidentialConnected #800
        residentialAddedFirst = objReplacement.pla_FirstHomesAdded #50
        residentialAddedSecond = objReplacement.pla_SecondHomesAdded #...
        residentialAddedThird = objReplacement.pla_ThirdHomesAdded #...

        residentialConnectedFirst = residentialConnected + residentialAddedFirst #850
        residentialConnectedSecond = residentialConnectedFirst + residentialAddedSecond #...
        residentialConnectedThird = residentialConnectedSecond + residentialAddedThird #...

        residentialMonthlyFuel = objFuel.gen_ResidentialFuelMonthly #15
        
        #Number of commercials (Expansion)
        commercialConnected = objDemography.gen_CommercialConnected #12
        commercialAddedFirst = objReplacement.pla_FirstCommercialAdded #20
        commercialAddedSecond = objReplacement.pla_SecondCommercialAdded #...
        commercialAddedThird = objReplacement.pla_ThirdCommercialAdded #...
        
        commercialConnectedFirst = commercialConnected + commercialAddedFirst #32
        commercialConnectedSecond = commercialConnectedFirst + commercialAddedSecond
        commercialConnectedThird = commercialConnectedSecond + commercialAddedThird
        
        commercialMonthlyFuel = objFuel.gen_CommercialFuelMonthly #15
        
        #RESIDENTIAL: Average anual residential/commercial emisions saved
        if (startingYear != 0):
            
            if(residentialFuelUsed == 'Kerosene'):
                constantResidential = keroseneConstant
            elif(residentialFuelUsed == 'Wood'):
                constantResidential = woodLogsConstant
            elif(residentialFuelUsed == 'Diesel'):
                constantResidential = dieselConstant
            else:
                constantResidential = 0
                
            if(commercialFuelUsed == 'Kerosene'):
                constantCommercial = keroseneConstant
            elif(commercialFuelUsed == 'Wood'):
                constantCommercial = woodLogsConstant
            elif(commercialFuelUsed == 'Diesel'):
                constantCommercial = dieselConstant
            else:
                constantCommercial = 0

            sumResidentialEmissions, sumCommercialEmissions = 0 , 0
            startingYearCurrentFuel = startingYear
            
            
            for i in range(projectionPeriod):
                startingYearCurrentFuel += 1

                if(yearFirstExpansion != 0):
                    if(startingYearCurrentFuel < yearFirstExpansion):
                        residentialCalc = residentialMonthlyFuel * constantResidential * kWhProducedBurned * monthsNumber * residentialConnected
                        commercialCalc = commercialMonthlyFuel * constantCommercial * kWhProducedBurned * monthsNumber * commercialConnected
                    if(yearSecondExpansion != 0):
                        if(startingYearCurrentFuel >= yearFirstExpansion and startingYearCurrentFuel < yearSecondExpansion):
                            residentialCalc = residentialMonthlyFuel * constantResidential * kWhProducedBurned * monthsNumber * residentialConnectedFirst
                            commercialCalc = commercialMonthlyFuel * constantCommercial * kWhProducedBurned * monthsNumber * commercialConnectedFirst
                        if(yearThirdExpansion != 0):
                            if(startingYearCurrentFuel >= yearSecondExpansion and startingYearCurrentFuel < yearThirdExpansion):
                                residentialCalc = residentialMonthlyFuel * constantResidential * kWhProducedBurned * monthsNumber * residentialConnectedSecond
                                commercialCalc = commercialMonthlyFuel * constantCommercial * kWhProducedBurned * monthsNumber * commercialConnectedSecond
                            elif(startingYearCurrentFuel >= yearThirdExpansion):
                                residentialCalc = residentialMonthlyFuel * constantResidential * kWhProducedBurned * monthsNumber * residentialConnectedThird
                                commercialCalc = commercialMonthlyFuel * constantCommercial * kWhProducedBurned * monthsNumber * commercialConnectedThird
                        elif(startingYearCurrentFuel >= yearSecondExpansion):
                            residentialCalc = residentialMonthlyFuel * constantResidential * kWhProducedBurned * monthsNumber * residentialConnectedSecond
                            commercialCalc = commercialMonthlyFuel * constantCommercial * kWhProducedBurned * monthsNumber * commercialConnectedSecond
                    elif(startingYearCurrentFuel >= yearFirstExpansion):
                        residentialCalc = residentialMonthlyFuel * constantResidential * kWhProducedBurned * monthsNumber * residentialConnectedFirst
                        commercialCalc = commercialMonthlyFuel * constantCommercial * kWhProducedBurned * monthsNumber * commercialConnectedFirst
                else:
                    residentialCalc = residentialMonthlyFuel * constantResidential * kWhProducedBurned * monthsNumber * residentialConnected
                    commercialCalc = commercialMonthlyFuel * constantCommercial * kWhProducedBurned * monthsNumber * commercialConnected
                    
                sumResidentialEmissions += residentialCalc
                sumCommercialEmissions += commercialCalc
                
            averageResidentialEmissions = sumResidentialEmissions / projectionPeriod
            averageCommercialEmissions = sumCommercialEmissions / projectionPeriod
            
            context['averageResidential'] = "{:,}".format(round(averageResidentialEmissions))
            context['averageCommercial'] = "{:,}".format(round(averageCommercialEmissions))

            #Emissions savings in No. of Cars
            if (averageResidentialEmissions != 0 and averageCommercialEmissions != 0):
                equivalentCars1 = (averageResidentialEmissions + averageCommercialEmissions) / emissionCar

                context['equivalentCars1'] = round(equivalentCars1)
            
            #Total lifetime emissions savings
                totalSavings1 = (averageResidentialEmissions * projectionPeriod) + (averageCommercialEmissions * projectionPeriod)

                context['totalSavings1'] = "{:,}".format(round(totalSavings1)) #VALUE FOR SHOW IN NUMBERS
                context['totalSavings1Chart'] = round(totalSavings1) #VALUE FOR SHOW IN CHART
                
    #GET DATA FOR: Emission Results Vs. Grid

            #Annual emissions savings

            startingYearGrid = startingYear
            sumCarbon = 0
            totalSavings2 = 0 #Total lifetime emissions savings

            for i in range(projectionPeriod):
                startingYearGrid += 1

                if(yearFirstExpansion != 0):
                    if(startingYearGrid < yearFirstExpansion):
                        residentialCalc = residentialConnected * estimatedConsumpResidential * monthsNumber
                        commercialCalc = commercialConnected * estimatedConsumpCommercial * monthsNumber
                    if(yearSecondExpansion != 0):
                        if(startingYearGrid >= yearFirstExpansion and startingYearGrid < yearSecondExpansion):
                            residentialCalc = residentialConnectedFirst * estimatedConsumpResidential * monthsNumber
                            commercialCalc = commercialConnectedFirst * estimatedConsumpCommercial * monthsNumber
                        if(yearThirdExpansion != 0):
                            if(startingYearGrid >= yearSecondExpansion and startingYearGrid < yearThirdExpansion):
                                residentialCalc = residentialConnectedSecond * estimatedConsumpResidential * monthsNumber
                                commercialCalc = commercialConnectedSecond * estimatedConsumpCommercial * monthsNumber
                            elif(startingYearGrid >= yearThirdExpansion):
                                residentialCalc = residentialConnectedThird * estimatedConsumpResidential * monthsNumber
                                commercialCalc = commercialConnectedThird * estimatedConsumpCommercial * monthsNumber
                        elif(startingYearGrid >= yearSecondExpansion):
                            residentialCalc = residentialConnectedSecond * estimatedConsumpResidential * monthsNumber
                            commercialCalc = commercialConnectedSecond * estimatedConsumpCommercial * monthsNumber
                    elif(startingYearGrid >= yearFirstExpansion):
                        residentialCalc = residentialConnectedFirst * estimatedConsumpResidential * monthsNumber
                        commercialCalc = commercialConnectedFirst * estimatedConsumpCommercial * monthsNumber
                else:
                    residentialCalc = residentialConnected * estimatedConsumpResidential * monthsNumber
                    commercialCalc = commercialConnected * estimatedConsumpCommercial * monthsNumber
                

                residentialYearlyConsump = residentialCalc * Decimal(math.pow(1+growthResidential, ((i + 1) - 1)))
                
                commercialYearlyConsump = commercialCalc * Decimal(math.pow(1+growthCommercial, ((i + 1) - 1)))
                
                totalEnergyDemand = residentialYearlyConsump + commercialYearlyConsump

                carbonEmission = totalEnergyDemand * carbonFactor
                
                
                totalSavings2 += carbonEmission #Total lifetime emissions savings

                sumCarbon += carbonEmission
            
            anualEmissions = sumCarbon / projectionPeriod

            context['anualEmissions'] = "{:,}".format(round(anualEmissions))
            
            #Emissions savings in No. of Cars
            equivalentCars2 = anualEmissions / emissionCar

            context['equivalentCars2'] = round(equivalentCars2)

            #Total lifetime emissions savings
            context['totalSavings2'] = "{:,}".format(round(totalSavings2)) #VALUE FOR SHOW IN NUMBERS
            context['totalSavings2Chart'] = round(totalSavings2) #VALUE FOR SHOW IN CHART

    return render(request, 'base/resultsCarbon.html', context)

@login_required(login_url='login')
def resultsEconomic(request, id):

    context = {'id': id}

    #GET DATA FOR: Project Name
    objProject = Project.objects.get(id = id)

    prjName = objProject.prj_name

    context['prjName'] = prjName

    try:
        objLocationDetails = G_LocationDetails.objects.get(gen_idProject = id)
        objDiscount = G_Discount.objects.get(gen_idProject = id)
        objCapital = P_Capital.objects.get(pla_idProject = id)
        objSubsidy = P_Subsidy.objects.get(pla_idProject = id)
        objOperational = P_Operational.objects.get(pla_idProject = id)
        objTime = G_Time.objects.get(gen_idProject = id)
        objReplacement = P_Replacement.objects.get(pla_idProject = id)
        objDetails = P_Details.objects.get(pla_idProject = id)
        objRates = R_Rates.objects.get(rev_idProject = id)
        objFuel = G_Fuel.objects.get(gen_idProject = id)
        objChanges = R_Changes.objects.get(rev_idProject = id)
        objDemography = G_Demography.objects.get(gen_idProject = id)
        objAverage = R_Average.objects.get(rev_idProject = id)
        objGrowth = R_Growth.objects.get(rev_idProject = id)
        objOptions = R_Options.objects.get(rev_idProject = id)
        
        results = True

    except:
        results = False
        
    if(results):
        #Global and views values or units
        currency = objLocationDetails.gen_Currency
        discountRate = objDiscount.gen_DiscountRate #10%
        discountUnit = objDiscount.gen_DiscountRateUnit
        projectionPeriod = objTime.gen_ProjectionPeriod #20
        startingYear = objTime.gen_StartingYear #2020
        batteryUnit = objDetails.pla_BatterySizeUnit
        #Total Capex
        land = objCapital.pla_Land
        panelsTurbines = objCapital.pla_PanelsTurbines
        switchgear= objCapital.pla_Switchgear
        protectionSystem= objCapital.pla_ProtectionSystem
        transformer = objCapital.pla_Transformer
        wiring = objCapital.pla_Wiring
        meters = objCapital.pla_Meters
        batteries = objCapital.pla_Batteries
        inverters = objCapital.pla_Inverters
        controlCost = objCapital.pla_ControlCost
        transportationCost = objCapital.pla_TransportationCost
        constructionCost = objCapital.pla_ConstructionCost
        ancillaryCost = objCapital.pla_AncillaryCost
        #Total Opex - lifetime
        yearlyOperationalExpenditure = objOperational.pla_OperationalExpenditure #200
        subsidyOperationalExpenditure = (objSubsidy.pla_SubsidyOperational / 100) #0
        yearlyOmEscalator = (objOperational.pla_OMEscalator / 100) #0.03
        #Total Repex and upgrade costs - lifetime
        subsidyReplacement = (objSubsidy.pla_SubsidyReplacement / 100) #20%
        yearFirstExpansion = objReplacement.pla_FirstExpansion #2029
        firstTotalExpenditure = objReplacement.pla_FirstTotalExpenditure #2000
        firstCostBatteries = objReplacement.pla_FirstBatteriesCost #1000
        firstCostBatteriesREPEX = objReplacement.pla_FirstBatteriesReplaced #...
        yearSecondExpansion = objReplacement.pla_SecondExpansion #2039
        secondTotalExpenditure = objReplacement.pla_SecondTotalExpenditure #...
        secondCostBatteries = objReplacement.pla_SecondBatteriesCost #...
        secondCostBatteriesREPEX = objReplacement.pla_SecondBatteriesReplaced #800
        yearThirdExpansion = objReplacement.pla_ThirdExpansion #...
        thirdTotalExpenditure = objReplacement.pla_ThirdTotalExpenditure #...
        thirdCostBatteries = objReplacement.pla_ThirdBatteriesCost #...
        thirdCostBatteriesREPEX = objReplacement.pla_ThirdBatteriesReplaced #...
        #Levelised Cost of Energy (LCOE)
        plantSize = objDetails.pla_PlantSize #20
        averageDailyGeneration = objDetails.pla_DailyGeneration #1650
        firstPlantSizeAdded = objReplacement.pla_FirstPlantAdded #20
        secondPlantSizeAdded = objReplacement.pla_SecondPlantAdded #0
        thirdPlantSizeAdded = objReplacement.pla_ThirdPlantAdded #0
        annualDegradation = (objDetails.pla_AnnualDegradation / 100) #0.5
        fixedCostResidentialOp1 = objRates.rev_FixedCostResidentialOp1 #20
        fixedCostResidentialOp1Unit = objRates.rev_FixedCostResidentialOp1Unit
        fixedCostCommercialOp1 = objRates.rev_FixedCostCommercialOp1 #20
        fixedCostCommercialOp1Unit = objRates.rev_FixedCostCommercialOp1Unit
        kWhResidentialOp2 = objRates.rev_KwhResidentialOp2 #0.20
        kWhresidentialOp2Unit = objRates.rev_KwhResidentialOp2Unit
        kWhcommercialOp2 = objRates.rev_kwhCommercialOp2 #0.20
        kWhcommercialOp2Unit = objRates.rev_kwhCommercialOp2Unit
        fixedCostResidentialOp3 = objRates.rev_FixedCostResidentialOp3 #2
        fixedCostCommercialOp3 = objRates.rev_FixedCostCommercialOp3 #2
        kWhResidentialOp3 = objRates.rev_KwhResidentialOp3 #0.15
        kWhCommercialOp3 = objRates.rev_KwhCommercialOp3 #0.15
        #Average annual savings OPTION 1 - RESIDENTIAL/COMMERCIAL
        residentialConnected = objDemography.gen_ResidentialConnected #800
        residentialAddedFirst = objReplacement.pla_FirstHomesAdded #50
        residentialAddedSecond = objReplacement.pla_SecondHomesAdded #...
        residentialAddedThird = objReplacement.pla_ThirdHomesAdded #...
        residencialCostFuel = objFuel.gen_ResidentialFuelCost #20
        commercialConnected = objDemography.gen_CommercialConnected #12
        commercialAddedFirst = objReplacement.pla_FirstCommercialAdded #20
        commercialAddedSecond = objReplacement.pla_SecondCommercialAdded #...
        commercialAddedThird = objReplacement.pla_ThirdCommercialAdded #...
        commercialCostFuel = objFuel.gen_CommercialFuelCost #20
        firstYearPriceRise = objChanges.rev_FirstPriceRise #2025
        firstYearPercentageRise = (objChanges.rev_FirstYearPercentage / 100) #0.01
        secondYearPriceRise = objChanges.rev_SecondPriceRise #2030
        secondYearPercentageRise = (objChanges.rev_SecondYearPercentage / 100) #0.015
        thirdYearPriceRise = objChanges.rev_ThirdPriceRise #2035
        thirdYearPercentageRise = (objChanges.rev_ThirdYearPercentage / 100) #0.015
        fourthYearPriceRise = objChanges.rev_FourthPriceRise #2040
        fourthYearPercentageRise = (objChanges.rev_FourthYearPercentage / 100) #0.015
        fifthYearPriceRise = objChanges.rev_FifthPriceRise #2045
        fifthYearPercentageRise = (objChanges.rev_FifthYearPercentage / 100) #0.015
        monthsNumber = objTime.gen_MonthsNumber #12
        residentialMonthlyFuel = objFuel.gen_ResidentialFuelMonthly #15
        commercialMonthlyFuel = objFuel.gen_CommercialFuelMonthly #15
        #Average annual savings OPTION 2 - RESIDENTIAL/COMMERCIAL
        estimatedConsumpResidential = objAverage.rev_ResidentialConsump #100
        estimatedConsumpCommercial = objAverage.rev_CommercialConsump #100
        growthResidential = (objGrowth.rev_ResidentialGrowth / 100) #0.01
        growthCommercial = (objGrowth.rev_CommercialGrowth / 100) #0.01
        #Average annual savings OPTION 2 - RESIDENTIAL/COMMERCIAL
        unchargedResidential = objOptions.rev_UnchargedResidentialOp3 #12
        unchargedCommercial = objOptions.rev_UnchargedCommercialOp3 #12
        

        context['currency'] = currency
        context['discountRate'] = round(discountRate,2)
        context['discountUnit'] = discountUnit
        context['batteryUnit'] = batteryUnit
        context['projectionPeriod'] = projectionPeriod
        context['fixedCostResidentialOp1'] = round(fixedCostResidentialOp1,2)
        context['fixedCostResidentialOp1Unit'] = fixedCostResidentialOp1Unit
        context['fixedCostCommercialOp1'] = round(fixedCostCommercialOp1,2)
        context['fixedCostCommercialOp1Unit'] = fixedCostCommercialOp1Unit
        context['kWhResidentialOp2'] = round(kWhResidentialOp2,2)
        context['kWhresidentialOp2Unit'] = kWhresidentialOp2Unit
        context['kWhcommercialOp2'] = round(kWhcommercialOp2,2)
        context['kWhcommercialOp2Unit'] = kWhcommercialOp2Unit
        context['fixedCostResidentialOp3'] = round(fixedCostResidentialOp3,2)
        context['fixedCostCommercialOp3'] = round(fixedCostCommercialOp3,2)
        context['kWhResidentialOp3'] = round(kWhResidentialOp3,2)
        context['kWhCommercialOp3'] = round(kWhCommercialOp3,2)
        #Global and views values or units

    #GET DATA FOR: Economic results summary (inc subsidies)

        installationCost = (objCapital.pla_InstallationCost / 100) #0.1
        subsidyCapital = (objSubsidy.pla_SubsidyCapital / 100) #0.2

        sumCapex = (land + panelsTurbines + switchgear + protectionSystem + transformer + wiring + meters + batteries + inverters + controlCost +
                transportationCost + constructionCost + ancillaryCost)

        installationCostCapex = round((sumCapex * installationCost),2)
        parcialCapex = sumCapex + installationCostCapex
        totalCapex = parcialCapex * (1 - subsidyCapital)

        context['totalCapex'] = "{:,}".format(round(totalCapex)) #VALUE FOR SHOW IN NUMBERS
        context['totalCapexChart'] = round(totalCapex) #VALUE FOR SHOW IN CHART

        #Total Opex - lifetime
        yearlyOperationalExpenditureOPEX = yearlyOperationalExpenditure #200
        
        sumOpex, resultOpex = 0,0

        for i in range(projectionPeriod):

            sumOpex += yearlyOperationalExpenditureOPEX
            yearlyOperationalExpenditureOPEX = yearlyOperationalExpenditureOPEX * (1+yearlyOmEscalator) * (1-subsidyOperationalExpenditure)

        resultOpex = sumOpex
        context['totalOpex'] = "{:,}".format(round(resultOpex)) #VALUE FOR SHOW IN NUMBERS
        context['totalOpexChart'] = round(resultOpex) #VALUE FOR SHOW IN CHART

        #Total Repex and upgrade costs - lifetime
        startingYearREPEX = startingYear
        sumREPEX = {}

        for i in range(projectionPeriod):

            startingYearREPEX += 1
            
            if(startingYearREPEX == yearFirstExpansion):
                firstREPEX = (firstTotalExpenditure + firstCostBatteries + firstCostBatteriesREPEX) * (1 - subsidyReplacement)
                sumREPEX['first'] = firstREPEX
            
            if(startingYearREPEX == yearSecondExpansion):
                secondREPEX = (secondTotalExpenditure + secondCostBatteries + secondCostBatteriesREPEX) * (1 - subsidyReplacement)
                sumREPEX['second'] = secondREPEX

            if(startingYearREPEX == yearThirdExpansion):
                thirdREPEX = (thirdTotalExpenditure + thirdCostBatteries + thirdCostBatteriesREPEX) * (1 - subsidyReplacement)
                sumREPEX['third'] = thirdREPEX

        totalREPEX = sum(sumREPEX.values())

        context['totalREPEX'] = "{:,}".format(round(totalREPEX)) #VALUE FOR SHOW IN NUMBERS
        context['totalREPEXChart'] = round(totalREPEX) #VALUE FOR SHOW IN CHART


        #Levelised Cost of Energy (LCOE)
        sumCostDiscount, sumEnergy, sumEnergyFirst, sumEnergySecond, sumEnergyThird = 0, 0, 0, 0, 0
        startingYearLevelised1 = startingYear
        startingYearLevelised2 = startingYear
        yearlyOperationalExpenditureLevelised = yearlyOperationalExpenditure #200
        energyProduced = plantSize * averageDailyGeneration
        energyProducedFirst = firstPlantSizeAdded * averageDailyGeneration
        energyProducedSecond = secondPlantSizeAdded * averageDailyGeneration
        energyProducedThird = thirdPlantSizeAdded * averageDailyGeneration

            #All costs (Discounted)
        for i in range(projectionPeriod):
            startingYearLevelised1 += 1

            if(startingYearLevelised1 == yearFirstExpansion):
                discount = (yearlyOperationalExpenditureLevelised + sumREPEX['first']) * Decimal(1 / math.pow((1+(discountRate/100)), (i+1)))
                sumCostDiscount += discount

            elif(startingYearLevelised1 == yearSecondExpansion):
                discount = (yearlyOperationalExpenditureLevelised + sumREPEX['second']) * Decimal(1 / math.pow((1+(discountRate/100)), (i+1)))
                sumCostDiscount += discount

            elif(startingYearLevelised1 == yearThirdExpansion):
                discount = (yearlyOperationalExpenditureLevelised + sumREPEX['third']) * Decimal(1 / math.pow((1+(discountRate/100)), (i+1)))
                sumCostDiscount += discount

            else:
                discount = yearlyOperationalExpenditureLevelised * Decimal(1 / math.pow((1+(discountRate/100)), (i+1)))
                sumCostDiscount += discount

            yearlyOperationalExpenditureLevelised = yearlyOperationalExpenditureLevelised * (1+yearlyOmEscalator) * (1-subsidyOperationalExpenditure)

            
        allCostsDiscounted = sumCostDiscount + totalCapex

        for i in range(projectionPeriod):
            startingYearLevelised2 += 1

            sumEnergy += energyProduced

            energyProduced = energyProduced * (1 - annualDegradation)

            if(startingYearLevelised2 >= yearFirstExpansion and yearFirstExpansion != 0):
                sumEnergyFirst += energyProducedFirst

                energyProducedFirst = energyProducedFirst * (1 - annualDegradation)

            if(startingYearLevelised2 >= yearSecondExpansion and yearSecondExpansion != 0):
                sumEnergySecond += energyProducedSecond

                energyProducedSecond = energyProducedSecond * (1 - annualDegradation)
            
            if(startingYearLevelised2 >= yearThirdExpansion and yearThirdExpansion != 0):
                sumEnergyThird += energyProducedThird

                energyProducedThird = energyProducedThird * (1 - annualDegradation)
            
        sumTotalEnergyProduced = sumEnergy + sumEnergyFirst + sumEnergySecond + sumEnergyThird

        levelisedCostOfEnergy = allCostsDiscounted / sumTotalEnergyProduced

        context['levelisedCostOfEnergy']=round(levelisedCostOfEnergy, 5)

    #GET DATA FOR: Capex breakdown
        sortedCapexBreakdownListLabels = []
        capexSubsidies = parcialCapex * subsidyCapital
        
        #DATA FOR SORT VALUES AND SHOW IN CAPEX BREAKDOWN CHART
        contextCapex = {'Land':float("{:,}".format(round(land))), 'PV panels, turbines, etc.':float(panelsTurbines), 'Switchgear':float(switchgear), 'Protection system':float(protectionSystem),
                        'Transformer':float(transformer), 'Wiring':float(wiring), 'Meters':float(meters), 'Batteries':float(batteries), 'Inverters':float(inverters), 
                        'Cost of a control setup':float(controlCost), 'Transportation and last mile costs':float(transportationCost), 'Construction and surveys + other upfront project':float(constructionCost), 
                        'Ancillary costs (such as for bulbs, fans ,etc)':float(ancillaryCost), 'Installation costs (at 10% of Capex)':float(installationCostCapex), 'Capex subsidies (at 20% of total Capex)':float(capexSubsidies)}
        
        #DATA FOR SENDING TO TEMPLATE
        context['land'] = "{:,}".format(round(land)) #VALUE FOR SHOW IN NUMBERS
        
        context['panelsTurbines'] = "{:,}".format(round(panelsTurbines))
        context['switchgear'] = "{:,}".format(round(switchgear))
        context['protectionSystem'] = "{:,}".format(round(protectionSystem))
        context['transformer'] = "{:,}".format(round(transformer))
        context['wiring'] = "{:,}".format(round(wiring))
        context['meters'] = "{:,}".format(round(meters))
        context['batteries'] = "{:,}".format(round(batteries))
        context['inverters'] = "{:,}".format(round(inverters))
        context['controlCost'] = "{:,}".format(round(controlCost))
        context['transportationCost'] = "{:,}".format(round(transportationCost))
        context['constructionCost'] = "{:,}".format(round(constructionCost))
        context['ancillaryCost'] = "{:,}".format(round(ancillaryCost))
        context['installationCostCapex'] = "{:,}".format(round(installationCostCapex))
        context['capexSubsidies'] = "{:,}".format(round(capexSubsidies))
        
        context['capexBreakdownList'] = sorted(contextCapex.values(), reverse=True)
 
        # list out keys and values separately
        keyListContextCapex = list(contextCapex.keys())
        valListContextCapex = list(contextCapex.values())


        old = 0
        for i in context['capexBreakdownList']:
            
            if old == i:
                index = valListContextCapex.index(i)
                valListContextCapex.remove(i)
                keyListContextCapex.remove(keyListContextCapex[index])
                
                index = valListContextCapex.index(i)
                key = keyListContextCapex[index]
            else:
                index = valListContextCapex.index(i)

            key = keyListContextCapex[index]

            sortedCapexBreakdownListLabels.append(key)
            
            old = i
            
        context['capexBreakdownListLabels'] = sortedCapexBreakdownListLabels

    #GET DATA FOR: Revenue Options
        #Average annual savings OPTION 1 - RESIDENTIAL/COMMERCIAL
        residentialConnectedFirst = residentialConnected + residentialAddedFirst #850
        residentialConnectedSecond = residentialConnectedFirst + residentialAddedSecond #...
        residentialConnectedThird = residentialConnectedSecond + residentialAddedThird #...

        commercialConnectedFirst = commercialConnected + commercialAddedFirst #32
        commercialConnectedSecond = commercialConnectedFirst + commercialAddedSecond
        commercialConnectedThird = commercialConnectedSecond + commercialAddedThird
        
        startingYearResidentialOp1 = startingYear
        averageAnnualResidentialFuelCost, averageAnnualCommercialFuelCost = 0, 0 #3600 = averageAnnualResidentialFuelCost/averageAnnualCommercialFuelCost
        
        try:
            for i in range(projectionPeriod):
                startingYearResidentialOp1 += 1
                
                if(yearFirstExpansion != 0):
                    if(startingYearResidentialOp1 < yearFirstExpansion):
                        residentialCostYear = monthsNumber * residentialMonthlyFuel * residencialCostFuel * residentialConnected
                        commercialCostYear = monthsNumber * commercialMonthlyFuel * commercialCostFuel * commercialConnected
                        
                        averageAnnualResidentialFuelCost += residentialCostYear / residentialConnected / projectionPeriod
                        averageAnnualCommercialFuelCost += commercialCostYear / commercialConnected / projectionPeriod
                    if(yearSecondExpansion != 0):
                        if(startingYearResidentialOp1 >= yearFirstExpansion and startingYearResidentialOp1 < yearSecondExpansion):
                            residentialCostYear = monthsNumber * residentialMonthlyFuel * residencialCostFuel * residentialConnectedFirst
                            commercialCostYear = monthsNumber * commercialMonthlyFuel * commercialCostFuel * commercialConnectedFirst
                            
                            averageAnnualResidentialFuelCost += residentialCostYear / residentialConnectedFirst / projectionPeriod
                            averageAnnualCommercialFuelCost += commercialCostYear / commercialConnectedFirst / projectionPeriod
                        if(yearThirdExpansion != 0):
                            if(startingYearResidentialOp1 >= yearSecondExpansion and startingYearResidentialOp1 < yearThirdExpansion):
                                residentialCostYear = monthsNumber * residentialMonthlyFuel * residencialCostFuel * residentialConnectedSecond
                                commercialCostYear = monthsNumber * commercialMonthlyFuel * commercialCostFuel * commercialConnectedSecond
                                
                                averageAnnualResidentialFuelCost += residentialCostYear / residentialConnectedSecond / projectionPeriod
                                averageAnnualCommercialFuelCost += commercialCostYear / commercialConnectedSecond / projectionPeriod
                            elif(startingYearResidentialOp1 >= yearThirdExpansion):
                                residentialCostYear = monthsNumber * residentialMonthlyFuel * residencialCostFuel * residentialConnectedThird
                                commercialCostYear = monthsNumber * commercialMonthlyFuel * commercialCostFuel * commercialConnectedThird
                                
                                averageAnnualResidentialFuelCost += residentialCostYear / residentialConnectedThird / projectionPeriod
                                averageAnnualCommercialFuelCost += commercialCostYear / commercialConnectedThird / projectionPeriod
                        elif(startingYearResidentialOp1 >= yearSecondExpansion):
                            residentialCostYear = monthsNumber * residentialMonthlyFuel * residencialCostFuel * residentialConnectedSecond
                            commercialCostYear = monthsNumber * commercialMonthlyFuel * commercialCostFuel * commercialConnectedSecond
                            
                            averageAnnualResidentialFuelCost += residentialCostYear / residentialConnectedSecond / projectionPeriod
                            averageAnnualCommercialFuelCost += commercialCostYear / commercialConnectedSecond / projectionPeriod
                    elif(startingYearResidentialOp1 >= yearFirstExpansion):
                        residentialCostYear = monthsNumber * residentialMonthlyFuel * residencialCostFuel * residentialConnectedFirst
                        commercialCostYear = monthsNumber * commercialMonthlyFuel * commercialCostFuel * commercialConnectedFirst
                        
                        averageAnnualResidentialFuelCost += residentialCostYear / residentialConnectedFirst / projectionPeriod
                        averageAnnualCommercialFuelCost += commercialCostYear / commercialConnectedFirst / projectionPeriod
                else:
                    residentialCostYear = monthsNumber * residentialMonthlyFuel * residencialCostFuel * residentialConnected
                    commercialCostYear = monthsNumber * commercialMonthlyFuel * commercialCostFuel * commercialConnected
                    
                    averageAnnualResidentialFuelCost += residentialCostYear / residentialConnected / projectionPeriod
                    averageAnnualCommercialFuelCost += commercialCostYear / commercialConnected / projectionPeriod

        except:
            averageAnnualResidentialFuelCost = 0
            averageAnnualCommercialFuelCost = 0
        
        #Vars FOR OPTION 1
        option1 = True
        activationNo = True
        activationFirst = False
        activationSecond = False
        activationThird = False
        activationFourth = False
        activationFifth = False
        startingYearResidentialBillsOp1 = startingYear
        count = 1
        averageResidentialBills, averageCommercialBills = 0, 0
        
        residentialRevenueNoPriceRise = fixedCostResidentialOp1 * monthsNumber
        commercialRevenueNoPriceRise = fixedCostCommercialOp1 * monthsNumber

        residentialRevenueRiseFirst = residentialRevenueNoPriceRise * (1 + firstYearPercentageRise)
        residentialRevenueRiseSecond = residentialRevenueRiseFirst * (1 + secondYearPercentageRise)
        residentialRevenueRiseThird = residentialRevenueRiseSecond * (1 + thirdYearPercentageRise)
        residentialRevenueRiseFourth = residentialRevenueRiseThird * (1 + fourthYearPercentageRise)
        residentialRevenueRiseFifth = residentialRevenueRiseFourth * (1 + fifthYearPercentageRise)
        
        commercialRevenueRiseFirst = commercialRevenueNoPriceRise * (1 + firstYearPercentageRise)
        commercialRevenueRiseSecond = commercialRevenueRiseFirst * (1 + secondYearPercentageRise)
        commercialRevenueRiseThird = commercialRevenueRiseSecond * (1 + thirdYearPercentageRise)
        commercialRevenueRiseFourth = commercialRevenueRiseThird * (1 + fourthYearPercentageRise)
        commercialRevenueRiseFifth = commercialRevenueRiseFourth * (1 + fifthYearPercentageRise)
        
        
        if(option1):
            
            for i in range(projectionPeriod):
                
                startingYearResidentialBillsOp1 += 1

                if(activationNo):
                    if(startingYearResidentialBillsOp1 == firstYearPriceRise or (i+1) == projectionPeriod):
                        averageResidentialBills += residentialRevenueNoPriceRise * count
                        averageCommercialBills +=  commercialRevenueNoPriceRise * count
                        activationNo = False
                        activationFirst = True
                        count = 0
                
                if(activationFirst and firstYearPriceRise != 0 and firstYearPriceRise >= startingYear):
                    if(startingYearResidentialBillsOp1 == secondYearPriceRise or (i+1) == projectionPeriod):
                        averageResidentialBills += residentialRevenueRiseFirst * count
                        averageCommercialBills +=  commercialRevenueRiseFirst * count
                        activationFirst = False
                        activationSecond = True
                        count = 0
                
                if(activationSecond and secondYearPriceRise != 0 and secondYearPriceRise >= firstYearPriceRise):
                    if(startingYearResidentialBillsOp1 == thirdYearPriceRise or (i+1) == projectionPeriod):
                        averageResidentialBills += residentialRevenueRiseSecond * count
                        averageCommercialBills +=  commercialRevenueRiseSecond * count
                        activationSecond = False
                        activationThird = True
                        count = 0
                    
                if(activationThird and thirdYearPriceRise != 0 and thirdYearPriceRise >= secondYearPriceRise):
                    if(startingYearResidentialBillsOp1 == fourthYearPriceRise or (i+1) == projectionPeriod):
                        averageResidentialBills += residentialRevenueRiseThird * count
                        averageCommercialBills +=  commercialRevenueRiseThird * count
                        activationThird = False
                        activationFourth = True
                        count = 0
                        
                if(activationFourth and fourthYearPriceRise != 0 and fourthYearPriceRise >= thirdYearPriceRise):
                    if(startingYearResidentialBillsOp1 == fifthYearPriceRise or (i+1) == projectionPeriod):
                        averageResidentialBills += residentialRevenueRiseFourth * count
                        averageCommercialBills +=  commercialRevenueRiseFourth * count
                        activationFourth = False
                        activationFifth = True
                        count = 0
                
                if(activationFifth and fifthYearPriceRise != 0 and fifthYearPriceRise >= fourthYearPriceRise):
                    if((i+1) == projectionPeriod):
                        averageResidentialBills += residentialRevenueRiseFifth * count
                        averageCommercialBills +=  commercialRevenueRiseFifth * count
                        activationFifth = False
                        activationNo = True
                        
                count += 1

            averageAnnualResidentialBillSavingOp1 = averageAnnualResidentialFuelCost - (averageResidentialBills / projectionPeriod)
            averageAnnualCommercialBillSavingOp1 = averageAnnualCommercialFuelCost - (averageCommercialBills / projectionPeriod)
            
            context['averageAnnualResidentialBillSavingOp1'] = "{:,}".format(round(averageAnnualResidentialBillSavingOp1)) #VALUE FOR SHOW IN NUMBERS
            context['averageAnnualCommercialBillSavingOp1'] = "{:,}".format(round(averageAnnualCommercialBillSavingOp1)) #VALUE FOR SHOW IN NUMBERS
            
        #Pre-tax NPV-IRR OPTION 1 
            startingYearPretax1 = startingYear
            currentResidentials = residentialConnected
            currentCommercials = commercialConnected
            currentResidentialFixedCost = residentialRevenueNoPriceRise
            currentCommercialFixedCost = commercialRevenueNoPriceRise
            netCashflowOption1 = []
            netCashflowOption1.append(-totalCapex)
            expansion, sumNetCashflowDiscounted = 0, 0
            yearlyOperationalExpenditureOption1 = yearlyOperationalExpenditure #200
            cumulativeYears = [startingYearPretax1]
            currentCumulativeDiscountCashflowOption1 = (-totalCapex)
            cumulativeDiscountCashflowOption1 = []
            cumulativeDiscountCashflowOption1.append(float(-totalCapex))

            
            for i in range(projectionPeriod):
                
                startingYearPretax1 += 1
                expansion = 0
                
                if(startingYearPretax1 == yearFirstExpansion and yearFirstExpansion != 0 and yearFirstExpansion > startingYear):
                    currentResidentials = residentialConnectedFirst
                    currentCommercials = commercialConnectedFirst
                    
                    expansion = (firstTotalExpenditure + firstCostBatteries + firstCostBatteriesREPEX) * (1 - subsidyReplacement)
                    
                elif(startingYearPretax1 == yearSecondExpansion and yearFirstExpansion != 0 and yearFirstExpansion > startingYear and yearSecondExpansion != 0 and yearSecondExpansion > yearFirstExpansion):
                    currentResidentials = residentialConnectedSecond
                    currentCommercials = commercialConnectedSecond
                    
                    expansion = (secondTotalExpenditure + secondCostBatteries + secondCostBatteriesREPEX) * (1 - subsidyReplacement)
                
                elif(startingYearPretax1 == yearThirdExpansion and yearFirstExpansion != 0 and yearFirstExpansion > startingYear and yearSecondExpansion != 0 and yearSecondExpansion > yearFirstExpansion
                    and yearThirdExpansion != 0 and yearThirdExpansion > yearSecondExpansion):
                    currentResidentials = residentialConnectedThird
                    currentCommercials = commercialConnectedThird
                    
                    expansion = (thirdTotalExpenditure + thirdCostBatteries + thirdCostBatteriesREPEX) * (1 - subsidyReplacement)
                    
                    
                if(startingYearPretax1 == (firstYearPriceRise+1) and firstYearPriceRise != 0 and firstYearPriceRise > startingYear):

                    currentResidentialFixedCost = residentialRevenueRiseFirst
                    currentCommercialFixedCost = commercialRevenueRiseFirst
                elif(startingYearPretax1 == (secondYearPriceRise+1) and firstYearPriceRise != 0 and firstYearPriceRise > startingYear and secondYearPriceRise != 0 and secondYearPriceRise > firstYearPriceRise):
                    
                    currentResidentialFixedCost = residentialRevenueRiseSecond
                    currentCommercialFixedCost = commercialRevenueRiseSecond
                elif(startingYearPretax1 == (thirdYearPriceRise+1) and firstYearPriceRise != 0 and firstYearPriceRise > startingYear and secondYearPriceRise != 0 and secondYearPriceRise > firstYearPriceRise
                    and thirdYearPriceRise != 0 and thirdYearPriceRise > secondYearPriceRise):
                    
                    currentResidentialFixedCost = residentialRevenueRiseThird
                    currentCommercialFixedCost = commercialRevenueRiseThird
                elif(startingYearPretax1 == (fourthYearPriceRise+1) and firstYearPriceRise != 0 and firstYearPriceRise > startingYear and secondYearPriceRise != 0 and secondYearPriceRise > firstYearPriceRise
                    and thirdYearPriceRise != 0 and thirdYearPriceRise > secondYearPriceRise and fourthYearPriceRise != 0 and fourthYearPriceRise > thirdYearPriceRise):
                    
                    currentResidentialFixedCost = residentialRevenueRiseFourth
                    currentCommercialFixedCost = commercialRevenueRiseFourth
                
                elif(startingYearPretax1 == (fifthYearPriceRise+1) and firstYearPriceRise != 0 and firstYearPriceRise > startingYear and secondYearPriceRise != 0 and secondYearPriceRise > firstYearPriceRise
                    and thirdYearPriceRise != 0 and thirdYearPriceRise > secondYearPriceRise and fourthYearPriceRise != 0 and fourthYearPriceRise > thirdYearPriceRise
                    and fifthYearPriceRise != 0 and fifthYearPriceRise > fourthYearPriceRise):
                    
                    currentResidentialFixedCost = residentialRevenueRiseFifth
                    currentCommercialFixedCost = residentialRevenueRiseFifth
                    
                    
                cumulativeYears.append(startingYearPretax1) #Years for NPV-IRR line chart
                context['cumulativeYears'] = cumulativeYears
                
                totalRevenueOption1 = (currentResidentialFixedCost * currentResidentials) + (currentCommercialFixedCost * currentCommercials)
            
                currentDiscountRateOption1 = Decimal((1 / math.pow((1 + (discountRate/100)), (i+1))))

                netCashflowDiscountedOption1 = (totalRevenueOption1 - yearlyOperationalExpenditureOption1 - expansion) * currentDiscountRateOption1

                currentNetCashflowOption1 = totalRevenueOption1 - (yearlyOperationalExpenditureOption1 + expansion)
                
                yearlyOperationalExpenditureOption1 = (yearlyOperationalExpenditureOption1) * (1 + yearlyOmEscalator) * (1 - subsidyOperationalExpenditure)

                currentCumulativeDiscountCashflowOption1 = currentCumulativeDiscountCashflowOption1 + netCashflowDiscountedOption1

                cumulativeDiscountCashflowOption1.append(float(round(currentCumulativeDiscountCashflowOption1, 2)))

                sumNetCashflowDiscounted += netCashflowDiscountedOption1

                netCashflowOption1.append(round(currentNetCashflowOption1, 2))
                
            preTaxNPVOption1 = round((sumNetCashflowDiscounted - totalCapex))
            preTaxIRROption1 =  round(npf.irr(netCashflowOption1), 3) * 100
            
            context['preTaxNPVOption1'] = "{:,}".format(preTaxNPVOption1) #VALUE FOR SHOW IN NUMBERS
            context['preTaxIRROption1'] = "{:,}".format(preTaxIRROption1) #VALUE FOR SHOW IN NUMBERS
            context['preTaxNPVOption1Chart'] = preTaxNPVOption1 #VALUE FOR SHOW IN CHART
            context['preTaxIRROption1Chart'] = preTaxIRROption1 #VALUE FOR SHOW IN CHART
            
            context['cumulativeDiscountCashflowOption1'] = cumulativeDiscountCashflowOption1

        #Average annual savings OPTION 2 - RESIDENTIAL/COMMERCIAL
        option2 = True
        if(option2):
            startingYearResidentialBillsOp2 = startingYear
            
            
            
            residentialKwhRiseFirst = kWhResidentialOp2 * (1 + firstYearPercentageRise) #0.2020
            residentialKwhRiseSecond = residentialKwhRiseFirst * (1 + secondYearPercentageRise) #0.2050
            residentialKwhRiseThird = residentialKwhRiseSecond * (1 + thirdYearPercentageRise) #0.2081
            residentialKwhRiseFourth = residentialKwhRiseThird * (1 + fourthYearPercentageRise) #0.2112
            residentialKwhRiseFifth = residentialKwhRiseFourth * (1 + fifthYearPercentageRise) #0.2144
            
            commercialKwhRiseFirst = kWhcommercialOp2 * (1 + firstYearPercentageRise) #0.2020
            commercialKwhRiseSecond = commercialKwhRiseFirst * (1 + secondYearPercentageRise) #0.2050
            commercialKwhRiseThird = commercialKwhRiseSecond * (1 + thirdYearPercentageRise) #0.2081
            commercialKwhRiseFourth = commercialKwhRiseThird * (1 + fourthYearPercentageRise) #0.2112
            commercialKwhRiseFifth = commercialKwhRiseFourth * (1 + fifthYearPercentageRise) #0.2144
            
            sum1YearlyResidentialRevenue, sum1YearlyCommercialRevenue, sum2ResidentialProperties, sum2CommercialProperties  = 0, 0, 0, 0
            
            sumProductResidential, sumProductCommercial, residentialYearlyConsump, commercialYearlyConsump = 0, 0, 0, 0
        
            try:
                for i in range(projectionPeriod):
                    startingYearResidentialBillsOp2 += 1

                    if(yearFirstExpansion != 0):
                        if(startingYearResidentialBillsOp2 < yearFirstExpansion):
                            residentialCalc = residentialConnected * estimatedConsumpResidential * monthsNumber
                            commercialCalc = commercialConnected * estimatedConsumpCommercial * monthsNumber
                            sum2ResidentialProperties = 1/residentialConnected
                            sum2CommercialProperties = 1/commercialConnected
                        if(yearSecondExpansion != 0):
                            if(startingYearResidentialBillsOp2 >= yearFirstExpansion and startingYearResidentialBillsOp2 < yearSecondExpansion):
                                residentialCalc = residentialConnectedFirst * estimatedConsumpResidential * monthsNumber
                                commercialCalc = commercialConnectedFirst * estimatedConsumpCommercial * monthsNumber
                                sum2ResidentialProperties = 1/residentialConnectedFirst
                                sum2CommercialProperties = 1/commercialConnectedFirst
                            if(yearThirdExpansion != 0):
                                if(startingYearResidentialBillsOp2 >= yearSecondExpansion and startingYearResidentialBillsOp2 < yearThirdExpansion):
                                    residentialCalc = residentialConnectedSecond * estimatedConsumpResidential * monthsNumber
                                    commercialCalc = commercialConnectedSecond * estimatedConsumpCommercial * monthsNumber
                                    sum2ResidentialProperties = 1/residentialConnectedSecond
                                    sum2CommercialProperties = 1/commercialConnectedSecond
                                elif(startingYearResidentialBillsOp2 >= yearThirdExpansion):
                                    residentialCalc = residentialConnectedThird * estimatedConsumpResidential * monthsNumber
                                    commercialCalc = commercialConnectedThird * estimatedConsumpCommercial * monthsNumber
                                    sum2ResidentialProperties = 1/residentialConnectedThird
                                    sum2CommercialProperties = 1/commercialConnectedThird
                            elif(startingYearResidentialBillsOp2 >= yearSecondExpansion):
                                residentialCalc = residentialConnectedSecond * estimatedConsumpResidential * monthsNumber
                                commercialCalc = commercialConnectedSecond * estimatedConsumpCommercial * monthsNumber
                                sum2ResidentialProperties = 1/residentialConnectedSecond
                                sum2CommercialProperties = 1/commercialConnectedSecond
                        elif(startingYearResidentialBillsOp2 >= yearFirstExpansion):
                            residentialCalc = residentialConnectedFirst * estimatedConsumpResidential * monthsNumber
                            commercialCalc = commercialConnectedFirst * estimatedConsumpCommercial * monthsNumber
                            sum2ResidentialProperties = 1/residentialConnectedFirst
                            sum2CommercialProperties = 1/commercialConnectedFirst
                    else:
                        residentialCalc = residentialConnected * estimatedConsumpResidential * monthsNumber
                        commercialCalc = commercialConnected * estimatedConsumpCommercial * monthsNumber
                        sum2ResidentialProperties = 1/residentialConnected
                        sum2CommercialProperties = 1/commercialConnected
                
                    residentialYearlyConsump = residentialCalc * Decimal(math.pow(1+growthResidential, ((i + 1) - 1))) #960000
                    commercialYearlyConsump = commercialCalc * Decimal(math.pow(1+growthCommercial, ((i + 1) - 1))) #14400
                    
                    if(startingYearResidentialBillsOp2 <= firstYearPriceRise):
                        sum1YearlyResidentialRevenue = residentialYearlyConsump * kWhResidentialOp2
                        sum1YearlyCommercialRevenue = commercialYearlyConsump * kWhcommercialOp2
                        
                    elif(startingYearResidentialBillsOp2 > firstYearPriceRise and startingYearResidentialBillsOp2 <= secondYearPriceRise):
                        sum1YearlyResidentialRevenue = residentialYearlyConsump * residentialKwhRiseFirst
                        sum1YearlyCommercialRevenue = commercialYearlyConsump * commercialKwhRiseFirst
                        
                    elif(startingYearResidentialBillsOp2 > secondYearPriceRise and startingYearResidentialBillsOp2 <= thirdYearPriceRise):
                        sum1YearlyResidentialRevenue = residentialYearlyConsump * residentialKwhRiseSecond
                        sum1YearlyCommercialRevenue = commercialYearlyConsump * commercialKwhRiseSecond
                        
                    elif(startingYearResidentialBillsOp2 > thirdYearPriceRise and startingYearResidentialBillsOp2 <= fourthYearPriceRise):
                        sum1YearlyResidentialRevenue = residentialYearlyConsump * residentialKwhRiseThird
                        sum1YearlyCommercialRevenue = commercialYearlyConsump * commercialKwhRiseThird
                        
                    elif(startingYearResidentialBillsOp2 > fourthYearPriceRise and startingYearResidentialBillsOp2 <= fifthYearPriceRise):
                        sum1YearlyResidentialRevenue = residentialYearlyConsump * residentialKwhRiseFourth
                        sum1YearlyCommercialRevenue = commercialYearlyConsump * commercialKwhRiseFourth
                    
                    elif(startingYearResidentialBillsOp2 > fifthYearPriceRise):
                        sum1YearlyResidentialRevenue = residentialYearlyConsump * residentialKwhRiseFifth
                        sum1YearlyCommercialRevenue = commercialYearlyConsump * commercialKwhRiseFifth
                        
                    sumProductResidential += (round(sum1YearlyResidentialRevenue) * Decimal(sum2ResidentialProperties))
                    sumProductCommercial += (round(sum1YearlyCommercialRevenue) * Decimal(sum2CommercialProperties))
                    
            except:
                sumProductResidential = 0
                sumProductCommercial = 0
            
            averageAnnualResidentialBills = sumProductResidential / projectionPeriod
            averageAnnualCommercialBills = sumProductCommercial / projectionPeriod

            averageAnnualResidentialBillSavingOp2 = averageAnnualResidentialFuelCost - averageAnnualResidentialBills
            averageAnnualCommercialBillSavingOp2 = averageAnnualCommercialFuelCost - averageAnnualCommercialBills
            
            context['averageAnnualResidentialBillSavingOp2'] = "{:,}".format(round(averageAnnualResidentialBillSavingOp2)) #VALUE FOR SHOW IN NUMBERS
            context['averageAnnualCommercialBillSavingOp2'] = "{:,}".format(round(averageAnnualCommercialBillSavingOp2)) #VALUE FOR SHOW IN NUMBERS


        #Pre-tax NPV-IRR OPTION 2
            startingYearPretax2 = startingYear
            netCashflowDiscountedOption2 = 0
            yearlyOperationalExpenditureOption2 = yearlyOperationalExpenditure #200
            netCashflowOption2 = []
            netCashflowOption2.append(-totalCapex)
            currentCumulativeDiscountCashflowOption2 = -totalCapex
            cumulativeDiscountCashflowOption2 = []
            cumulativeDiscountCashflowOption2.append(float(-totalCapex))
            
            currentEnergyRequiredResidentials = residentialConnected * monthsNumber * estimatedConsumpResidential
            currentEnergyRequiredCommercials = commercialConnected * monthsNumber * estimatedConsumpCommercial
            
            currentKwhConsumedResidential = kWhResidentialOp2
            currentKwhConsumedCommercial = kWhcommercialOp2
            
            for i in range(projectionPeriod):
                
                startingYearPretax2 += 1
                expansion = 0
                
                if(startingYearPretax2 == yearFirstExpansion and yearFirstExpansion != 0 and yearFirstExpansion > startingYear):
                    currentEnergyRequiredResidentials = residentialConnectedFirst * monthsNumber * estimatedConsumpResidential
                    currentEnergyRequiredCommercials = commercialConnectedFirst * monthsNumber * estimatedConsumpCommercial
                    
                    expansion = (firstTotalExpenditure + firstCostBatteries + firstCostBatteriesREPEX) * (1 - subsidyReplacement)
                    
                elif(startingYearPretax2 == yearSecondExpansion and yearFirstExpansion != 0 and yearFirstExpansion > startingYear and yearSecondExpansion != 0 and yearSecondExpansion > yearFirstExpansion):
                    currentEnergyRequiredResidentials = residentialConnectedSecond * monthsNumber * estimatedConsumpResidential
                    currentEnergyRequiredCommercials = commercialConnectedSecond * monthsNumber * estimatedConsumpCommercial
                    
                    expansion = (secondTotalExpenditure + secondCostBatteries + secondCostBatteriesREPEX) * (1 - subsidyReplacement)
                
                elif(startingYearPretax2 == yearThirdExpansion and yearFirstExpansion != 0 and yearFirstExpansion > startingYear and yearSecondExpansion != 0 and yearSecondExpansion > yearFirstExpansion
                    and yearThirdExpansion != 0 and yearThirdExpansion > yearSecondExpansion):
                    currentEnergyRequiredResidentials = residentialConnectedThird * monthsNumber * estimatedConsumpResidential
                    currentEnergyRequiredCommercials = commercialConnectedThird * monthsNumber * estimatedConsumpCommercial
                    
                    expansion = (thirdTotalExpenditure + thirdCostBatteries + thirdCostBatteriesREPEX) * (1 - subsidyReplacement)
            
                if(startingYearPretax2 == (firstYearPriceRise+1) and firstYearPriceRise != 0 and firstYearPriceRise > startingYear):

                    currentKwhConsumedResidential = residentialKwhRiseFirst
                    currentKwhConsumedCommercial = commercialKwhRiseFirst
                    
                elif(startingYearPretax2 == (secondYearPriceRise+1) and firstYearPriceRise != 0 and firstYearPriceRise > startingYear and secondYearPriceRise != 0 and secondYearPriceRise > firstYearPriceRise):
                    
                    currentKwhConsumedResidential = residentialKwhRiseSecond
                    currentKwhConsumedCommercial = commercialKwhRiseSecond
                    
                elif(startingYearPretax2 == (thirdYearPriceRise+1) and firstYearPriceRise != 0 and firstYearPriceRise > startingYear and secondYearPriceRise != 0 and secondYearPriceRise > firstYearPriceRise
                    and thirdYearPriceRise != 0 and thirdYearPriceRise > secondYearPriceRise):
                    
                    currentKwhConsumedResidential = residentialKwhRiseThird
                    currentKwhConsumedCommercial = commercialKwhRiseThird
                    
                elif(startingYearPretax2 == (fourthYearPriceRise+1) and firstYearPriceRise != 0 and firstYearPriceRise > startingYear and secondYearPriceRise != 0 and secondYearPriceRise > firstYearPriceRise
                    and thirdYearPriceRise != 0 and thirdYearPriceRise > secondYearPriceRise and fourthYearPriceRise != 0 and fourthYearPriceRise > thirdYearPriceRise):
                    
                    currentKwhConsumedResidential = residentialKwhRiseFourth
                    currentKwhConsumedCommercial = commercialKwhRiseFourth
                
                elif(startingYearPretax2 == (fifthYearPriceRise+1) and firstYearPriceRise != 0 and firstYearPriceRise > startingYear and secondYearPriceRise != 0 and secondYearPriceRise > firstYearPriceRise
                    and thirdYearPriceRise != 0 and thirdYearPriceRise > secondYearPriceRise and fourthYearPriceRise != 0 and fourthYearPriceRise > thirdYearPriceRise
                    and fifthYearPriceRise != 0 and fifthYearPriceRise > fourthYearPriceRise):
                    
                    currentKwhConsumedResidential = residentialKwhRiseFifth
                    currentKwhConsumedCommercial = commercialKwhRiseFifth
                
                
                energyPostIncreaseResidential = currentEnergyRequiredResidentials * Decimal(math.pow((1 + growthResidential),i))
                energyPostIncreaseCommercial = currentEnergyRequiredCommercials * Decimal(math.pow((1 + growthCommercial),i))
                
                residentialRevenue = energyPostIncreaseResidential * currentKwhConsumedResidential
                commercialRenevue = energyPostIncreaseCommercial * currentKwhConsumedCommercial

                totalRevenueOption2 = residentialRevenue + commercialRenevue
                
                currentDiscountRate = Decimal((1 / math.pow((1 + (discountRate/100)), (i+1))))
                
                netCashflowDiscountedOption2 += (totalRevenueOption2 - yearlyOperationalExpenditureOption2 - expansion) * currentDiscountRate
                
                currentNetCashflowOption2 = totalRevenueOption2 - yearlyOperationalExpenditureOption2

                currentNetCashflowDiscountedOption2 = (totalRevenueOption2 - yearlyOperationalExpenditureOption2 - expansion) * currentDiscountRate

                currentCumulativeDiscountCashflowOption2 = currentCumulativeDiscountCashflowOption2 + currentNetCashflowDiscountedOption2

                cumulativeDiscountCashflowOption2.append(float(currentCumulativeDiscountCashflowOption2))

                yearlyOperationalExpenditureOption2 = (yearlyOperationalExpenditureOption2) * (1 + yearlyOmEscalator) * (1 - subsidyOperationalExpenditure)
                
                netCashflowOption2.append(currentNetCashflowOption2)
            
            preTaxNPVOption2 = round((netCashflowDiscountedOption2 - totalCapex))
            preTaxIRROption2 = round((npf.irr(netCashflowOption2) * 100),1)
            
            context['preTaxNPVOption2'] = "{:,}".format(preTaxNPVOption2) #VALUE FOR SHOW IN NUMBERS
            context['preTaxIRROption2'] = "{:,}".format(preTaxIRROption2) #VALUE FOR SHOW IN NUMBERS
            context['preTaxNPVOption2Chart'] = preTaxNPVOption2 #VALUE FOR SHOW IN CHART
            context['preTaxIRROption2Chart'] = preTaxIRROption2 #VALUE FOR SHOW IN CHART
            
            context['cumulativeDiscountCashflowOption2'] = cumulativeDiscountCashflowOption2
    
        #Average annual savings OPTION 3 - RESIDENTIAL/COMMERCIAL
        option3 = True
        if(option3):
            startingYearResidentialBillsOp3 = startingYear
            
            residentialYearlyConsump, commercialYearlyConsump, consumPostConsumFixedCostResidential, consumPostConsumFixedCostCommercial = 0, 0, Decimal(0), Decimal(0)
            countYearNoRise, countYearRiseFirst, countYearRiseSecond, countYearRiseThird, countYearRiseFourth, countYearRiseFifth = 0, 0, 0, 0, 0, 0
            sumResidentialConnected, sumCommercialConnected = Decimal(0), Decimal(0)
                      
            #Part 1
            residentialKwhRiseFirstOp3 = kWhResidentialOp3 * (1+firstYearPercentageRise) #0.1515
            residentialKwhRiseSecondOp3 = residentialKwhRiseFirstOp3 * (1+secondYearPercentageRise) #0.1538
            residentialKwhRiseThirdOp3 = residentialKwhRiseSecondOp3 * (1+thirdYearPercentageRise) #0.1561
            residentialKwhRiseFourthOp3 = residentialKwhRiseThirdOp3 * (1+fourthYearPercentageRise) #0.1584
            residentialKwhRiseFifthOp3 = residentialKwhRiseFourthOp3 * (1+fifthYearPercentageRise) #0.1608
            
            commercialKwhRiseFirstOp3 = kWhCommercialOp3 * (1+firstYearPercentageRise) #0.1515
            commercialKwhRiseSecondOp3 = commercialKwhRiseFirstOp3 * (1+secondYearPercentageRise) #0.1538
            commercialKwhRiseThirdOp3 = commercialKwhRiseSecondOp3 * (1+thirdYearPercentageRise) #0.1561
            commercialKwhRiseFourthOp3 = commercialKwhRiseThirdOp3 * (1+fourthYearPercentageRise) #0.1584
            commercialKwhRiseFifthOp3 = commercialKwhRiseFourthOp3 * (1+fifthYearPercentageRise) #0.1608
            
            #Part2
            residentialFixedCostNoRiseOp3 = fixedCostResidentialOp3 * monthsNumber #24
            residentialFixedCostRiseFirstOp3 =  residentialFixedCostNoRiseOp3 * (1+firstYearPercentageRise) #24.24
            residentialFixedCostRiseSecondOp3 = residentialFixedCostRiseFirstOp3 * (1+secondYearPercentageRise) #24.60
            residentialFixedCostRiseThirdOp3 = residentialFixedCostRiseSecondOp3 * (1+thirdYearPercentageRise) #24.97
            residentialFixedCostRiseFourthOp3 = residentialFixedCostRiseThirdOp3 * (1+fourthYearPercentageRise) #25.35
            residentialFixedCostRiseFifthOp3 = residentialFixedCostRiseFourthOp3 * (1+fifthYearPercentageRise) #25.73
            
            commercialFixedCostNoRiseOp3 = fixedCostCommercialOp3 * monthsNumber #24
            commercialFixedCostRiseFirstOp3 =  commercialFixedCostNoRiseOp3 * (1+firstYearPercentageRise) #24.24
            commercialFixedCostRiseSecondOp3 = commercialFixedCostRiseFirstOp3 * (1+secondYearPercentageRise) #24.60
            commercialFixedCostRiseThirdOp3 = commercialFixedCostRiseSecondOp3 * (1+thirdYearPercentageRise) #24.97
            commercialFixedCostRiseFourthOp3 = commercialFixedCostRiseThirdOp3 * (1+fourthYearPercentageRise) #25.35
            commercialFixedCostRiseFifthOp3 = commercialFixedCostRiseFourthOp3 * (1+fifthYearPercentageRise) #25.73
            
            if(unchargedResidential < estimatedConsumpResidential):
                valueResidentials = unchargedResidential
                valueCommercials = unchargedCommercial
            else:
                valueResidentials = estimatedConsumpResidential
                valueCommercials = estimatedConsumpCommercial
                
            for i in range(projectionPeriod):
                
                startingYearResidentialBillsOp3 += 1

                if(yearFirstExpansion != 0):
                    if(startingYearResidentialBillsOp3 < yearFirstExpansion):
                        residentialCalc = residentialConnected * estimatedConsumpResidential * monthsNumber
                        commercialCalc = commercialConnected * estimatedConsumpCommercial * monthsNumber
                        numberResidentialsConnected = residentialConnected
                        numberCommercialsConnected = commercialConnected
                        sumResidentialConnected += residentialConnected
                        sumCommercialConnected += commercialConnected
                        
                    if(yearSecondExpansion != 0):
                        if(startingYearResidentialBillsOp3 >= yearFirstExpansion and startingYearResidentialBillsOp3 < yearSecondExpansion):
                            residentialCalc = residentialConnectedFirst * estimatedConsumpResidential * monthsNumber
                            commercialCalc = commercialConnectedFirst * estimatedConsumpCommercial * monthsNumber
                            numberResidentialsConnected = residentialConnectedFirst
                            numberCommercialsConnected = commercialConnectedFirst
                            sumResidentialConnected += residentialConnectedFirst
                            sumCommercialConnected += commercialConnectedFirst
                            
                        if(yearThirdExpansion != 0):
                            if(startingYearResidentialBillsOp3 >= yearSecondExpansion and startingYearResidentialBillsOp3 < yearThirdExpansion):
                                residentialCalc = residentialConnectedSecond * estimatedConsumpResidential * monthsNumber
                                commercialCalc = commercialConnectedSecond * estimatedConsumpCommercial * monthsNumber
                                numberResidentialsConnected = residentialConnectedSecond
                                numberCommercialsConnected = commercialConnectedSecond
                                sumResidentialConnected += residentialConnectedSecond
                                sumCommercialConnected += commercialConnectedSecond
                                
                            elif(startingYearResidentialBillsOp3 >= yearThirdExpansion):
                                residentialCalc = residentialConnectedThird * estimatedConsumpResidential * monthsNumber
                                commercialCalc = commercialConnectedThird * estimatedConsumpCommercial * monthsNumber
                                numberResidentialsConnected = residentialConnectedThird
                                numberCommercialsConnected = commercialConnectedThird
                                sumResidentialConnected += residentialConnectedThird
                                sumCommercialConnected += commercialConnectedThird
                                
                        elif(startingYearResidentialBillsOp3 >= yearSecondExpansion):
                            residentialCalc = residentialConnectedSecond * estimatedConsumpResidential * monthsNumber
                            commercialCalc = commercialConnectedSecond * estimatedConsumpCommercial * monthsNumber
                            numberResidentialsConnected = residentialConnectedSecond
                            numberCommercialsConnected = commercialConnectedSecond
                            sumResidentialConnected += residentialConnectedSecond
                            sumCommercialConnected += commercialConnectedSecond
                            
                    elif(startingYearResidentialBillsOp3 >= yearFirstExpansion):
                        residentialCalc = residentialConnectedFirst * estimatedConsumpResidential * monthsNumber
                        commercialCalc = commercialConnectedFirst * estimatedConsumpCommercial * monthsNumber
                        numberResidentialsConnected = residentialConnectedFirst
                        numberCommercialsConnected = commercialConnectedFirst
                        sumResidentialConnected += residentialConnectedFirst
                        sumCommercialConnected += commercialConnectedFirst
                else:
                    residentialCalc = residentialConnected * estimatedConsumpResidential * monthsNumber
                    commercialCalc = commercialConnected * estimatedConsumpCommercial * monthsNumber
                    numberResidentialsConnected = residentialConnected
                    numberCommercialsConnected = commercialConnected
                    sumResidentialConnected += residentialConnected
                    sumCommercialConnected += commercialConnected
        
                residentialYearlyConsump = round(residentialCalc * Decimal(math.pow(1+growthResidential, ((i + 1) - 1))),2) #960000
                commercialYearlyConsump = round(commercialCalc * Decimal(math.pow(1+growthCommercial, ((i + 1) - 1))),2) #14400
        
                
                annualConsumFixedCostResidential = valueResidentials * monthsNumber * numberResidentialsConnected
                annualConsumFixedCostCommercial = valueCommercials * monthsNumber * numberCommercialsConnected
                
                if((residentialYearlyConsump-annualConsumFixedCostResidential) > 0 and (commercialYearlyConsump - annualConsumFixedCostCommercial) > 0):
                    consumPostConsumFixedCostResidential += residentialYearlyConsump - annualConsumFixedCostResidential #Formula missed in the last two years of projection (257 AC:AD)
                    consumPostConsumFixedCostCommercial += commercialYearlyConsump - annualConsumFixedCostCommercial #Formula missed in the last two years of projection (258 AC:AD)
                
                if(firstYearPriceRise != 0):
                    if(startingYearResidentialBillsOp3 <= firstYearPriceRise):
                        countYearNoRise += 1
                        
                    if(secondYearPriceRise != 0):
                        if(startingYearResidentialBillsOp3 > firstYearPriceRise and startingYearResidentialBillsOp3 <= secondYearPriceRise):
                            countYearRiseFirst += 1
                            
                        if(thirdYearPriceRise != 0):
                            if(startingYearResidentialBillsOp3 > secondYearPriceRise and startingYearResidentialBillsOp3 <= thirdYearPriceRise):
                                countYearRiseSecond += 1
                                
                            if(fourthYearPriceRise != 0):
                                if(startingYearResidentialBillsOp3 > thirdYearPriceRise and startingYearResidentialBillsOp3 <= fourthYearPriceRise):
                                    countYearRiseThird += 1
                                    
                                if(fifthYearPriceRise != 0):
                                    if(startingYearResidentialBillsOp3 > fourthYearPriceRise and startingYearResidentialBillsOp3 <= fifthYearPriceRise):
                                        countYearRiseFourth += 1
                                        
                                    elif(startingYearResidentialBillsOp3 > fifthYearPriceRise):
                                        countYearRiseFifth += 1
                                        
                                elif(startingYearResidentialBillsOp3 > fourthYearPriceRise):
                                    countYearRiseFourth += 1
                                    
                            elif(startingYearResidentialBillsOp3 > thirdYearPriceRise):
                                countYearRiseThird += 1
                                
                        elif(startingYearResidentialBillsOp3 > secondYearPriceRise):
                            countYearRiseSecond += 1
                            
                    elif(startingYearResidentialBillsOp3 > firstYearPriceRise):
                        countYearRiseFirst += 1
                else:
                    countYearNoRise += 1

            sumKwhRiseResidential = kWhResidentialOp3 * countYearNoRise
            sumKwhRiseResidential += residentialKwhRiseFirstOp3 * countYearRiseFirst
            sumKwhRiseResidential += residentialKwhRiseSecondOp3 * countYearRiseSecond
            sumKwhRiseResidential += residentialKwhRiseThirdOp3 * countYearRiseThird
            sumKwhRiseResidential += residentialKwhRiseFourthOp3 * countYearRiseFourth
            sumKwhRiseResidential += residentialKwhRiseFifthOp3 * countYearRiseFifth
            
            sumKwhRiseCommercial = kWhCommercialOp3 * countYearNoRise
            sumKwhRiseCommercial += commercialKwhRiseFirstOp3 * countYearRiseFirst
            sumKwhRiseCommercial += commercialKwhRiseSecondOp3 * countYearRiseSecond
            sumKwhRiseCommercial += commercialKwhRiseThirdOp3 * countYearRiseThird
            sumKwhRiseCommercial += commercialKwhRiseFourthOp3 * countYearRiseFourth
            sumKwhRiseCommercial += commercialKwhRiseFifthOp3 * countYearRiseFifth
            
            averageAnnualResidentialBillsOption3_1 = ((consumPostConsumFixedCostResidential/projectionPeriod) * sumKwhRiseResidential) / projectionPeriod
            averageAnnualCommercialBillsOption3_1 = ((consumPostConsumFixedCostCommercial/projectionPeriod) * sumKwhRiseCommercial) / projectionPeriod
            
            sumFixedCostResidential = residentialFixedCostNoRiseOp3 * countYearNoRise
            sumFixedCostResidential += residentialFixedCostRiseFirstOp3 * countYearRiseFirst
            sumFixedCostResidential += residentialFixedCostRiseSecondOp3 * countYearRiseSecond
            sumFixedCostResidential += residentialFixedCostRiseThirdOp3 * countYearRiseThird
            sumFixedCostResidential += residentialFixedCostRiseFourthOp3 * countYearRiseFourth
            sumFixedCostResidential += residentialFixedCostRiseFifthOp3 * countYearRiseFifth
            
            sumFixedCostCommercial = commercialFixedCostNoRiseOp3 * countYearNoRise
            sumFixedCostCommercial += commercialFixedCostRiseFirstOp3 * countYearRiseFirst
            sumFixedCostCommercial += commercialFixedCostRiseSecondOp3 * countYearRiseSecond
            sumFixedCostCommercial += commercialFixedCostRiseThirdOp3 * countYearRiseThird
            sumFixedCostCommercial += commercialFixedCostRiseFourthOp3 * countYearRiseFourth
            sumFixedCostCommercial += commercialFixedCostRiseFifthOp3 * countYearRiseFifth
            
            try:
                averageAnnualResidentialBillsOp3_total = (averageAnnualResidentialBillsOption3_1 / (sumResidentialConnected/projectionPeriod)) + (sumFixedCostResidential / projectionPeriod)
                averageAnnualCommercialBillsOp3_total = (averageAnnualCommercialBillsOption3_1 / (sumCommercialConnected/projectionPeriod)) + (sumFixedCostCommercial / projectionPeriod)
            except:
                averageAnnualResidentialBillsOp3_total = (sumFixedCostResidential / projectionPeriod)
                averageAnnualCommercialBillsOp3_total = (sumFixedCostCommercial / projectionPeriod)
            
            averageAnnualResidentialBillSavingOp3 = averageAnnualResidentialFuelCost - averageAnnualResidentialBillsOp3_total
            averageAnnualCommercialBillSavingOp3 = averageAnnualCommercialFuelCost - averageAnnualCommercialBillsOp3_total
             
            context['averageAnnualResidentialBillSavingOp3'] = "{:,}".format(round(averageAnnualResidentialBillSavingOp3)) #VALUE FOR SHOW IN NUMBERS
            context['averageAnnualCommercialBillSavingOp3'] = "{:,}".format(round(averageAnnualCommercialBillSavingOp3)) #VALUE FOR SHOW IN NUMBERS
            
        #Pre-tax NPV-IRR OPTION 3
            startingYearPretax3 = startingYear
            currentRevenuePriceRisePerKwhResidentials = kWhResidentialOp3
            currentRevenuePriceRisePerKwhCommercials = kWhCommercialOp3
            currentResidentialFixedCost = residentialFixedCostNoRiseOp3
            currentCommercialFixedCost = commercialFixedCostNoRiseOp3
            yearlyOperationalExpenditureOption3 = yearlyOperationalExpenditure #200
            currentResidentials = residentialConnected
            currentCommercials = commercialConnected
            currentEnergyRequiredResidentials = residentialConnected * monthsNumber * estimatedConsumpResidential
            currentEnergyRequiredCommercials = commercialConnected * monthsNumber * estimatedConsumpResidential
            currentNetCashflowDiscountedOption3 = 0
            netCashflowOption3 = []
            netCashflowOption3.append(-totalCapex)
            currentCumulativeDiscountCashflowOption3 = -totalCapex
            cumulativeDiscountCashflowOption3 = []
            cumulativeDiscountCashflowOption3.append(float(-totalCapex))
            

            for i in range(projectionPeriod):
                
                startingYearPretax3 += 1
                expansion = 0
                
                if(
                startingYearPretax3 == yearFirstExpansion and yearFirstExpansion != 0 and yearFirstExpansion > startingYear):
                    currentResidentials = residentialConnectedFirst
                    currentCommercials = commercialConnectedFirst

                    currentEnergyRequiredResidentials = residentialConnectedFirst * monthsNumber * estimatedConsumpResidential
                    currentEnergyRequiredCommercials = commercialConnectedFirst * monthsNumber * estimatedConsumpCommercial

                    expansion = (firstTotalExpenditure + firstCostBatteries + firstCostBatteriesREPEX) * (1 - subsidyReplacement)
                elif(startingYearPretax3 == yearSecondExpansion and yearFirstExpansion != 0 and yearFirstExpansion > startingYear and yearSecondExpansion != 0 and yearSecondExpansion > yearFirstExpansion):
                    currentResidentials = residentialConnectedSecond
                    currentCommercials = commercialConnectedSecond

                    currentEnergyRequiredResidentials = residentialConnectedSecond * monthsNumber * estimatedConsumpResidential
                    currentEnergyRequiredCommercials = commercialConnectedSecond * monthsNumber * estimatedConsumpCommercial
                    
                    expansion = (secondTotalExpenditure + secondCostBatteries + secondCostBatteriesREPEX) * (1 - subsidyReplacement)
                elif(startingYearPretax3 == yearThirdExpansion and yearFirstExpansion != 0 and yearFirstExpansion > startingYear and yearSecondExpansion != 0 and yearSecondExpansion > yearFirstExpansion
                    and yearThirdExpansion != 0 and yearThirdExpansion > yearSecondExpansion):
                    currentResidentials = residentialConnectedThird
                    currentCommercials = commercialConnectedThird

                    currentEnergyRequiredResidentials = residentialConnectedThird * monthsNumber * estimatedConsumpResidential
                    currentEnergyRequiredCommercials = commercialConnectedThird * monthsNumber * estimatedConsumpCommercial
                    
                    expansion = (thirdTotalExpenditure + thirdCostBatteries + thirdCostBatteriesREPEX) * (1 - subsidyReplacement)
            
            
                if(startingYearPretax3 == (firstYearPriceRise + 1) and firstYearPriceRise != 0 and firstYearPriceRise > startingYear):
                    currentResidentialFixedCost = residentialFixedCostRiseFirstOp3
                    currentCommercialFixedCost = commercialFixedCostRiseFirstOp3

                    currentRevenuePriceRisePerKwhResidentials = residentialKwhRiseFirstOp3
                    currentRevenuePriceRisePerKwhCommercials = commercialKwhRiseFirstOp3
                    
                elif(startingYearPretax3 == (secondYearPriceRise + 1) and firstYearPriceRise != 0 and firstYearPriceRise > startingYear and secondYearPriceRise != 0 and secondYearPriceRise > firstYearPriceRise):
                    currentResidentialFixedCost = residentialFixedCostRiseSecondOp3
                    currentCommercialFixedCost = commercialFixedCostRiseSecondOp3

                    currentRevenuePriceRisePerKwhResidentials = residentialKwhRiseSecondOp3
                    currentRevenuePriceRisePerKwhCommercials = commercialKwhRiseSecondOp3
                    
                elif(startingYearPretax3 == (thirdYearPriceRise + 1) and firstYearPriceRise != 0 and firstYearPriceRise > startingYear and secondYearPriceRise != 0 and secondYearPriceRise > firstYearPriceRise
                    and thirdYearPriceRise != 0 and thirdYearPriceRise > secondYearPriceRise):
                    currentResidentialFixedCost = residentialFixedCostRiseThirdOp3
                    currentCommercialFixedCost = commercialFixedCostRiseThirdOp3

                    currentRevenuePriceRisePerKwhResidentials = residentialKwhRiseThirdOp3
                    currentRevenuePriceRisePerKwhCommercials = commercialKwhRiseThirdOp3
                    
                elif(startingYearPretax3 == fourthYearPriceRise + 1 and firstYearPriceRise != 0 and firstYearPriceRise > startingYear and secondYearPriceRise != 0 and secondYearPriceRise > firstYearPriceRise
                    and thirdYearPriceRise != 0 and thirdYearPriceRise > secondYearPriceRise and fourthYearPriceRise != 0 and fourthYearPriceRise > thirdYearPriceRise):
                    currentResidentialFixedCost = residentialFixedCostRiseFourthOp3
                    currentCommercialFixedCost = commercialFixedCostRiseFourthOp3

                    currentRevenuePriceRisePerKwhResidentials = residentialKwhRiseFourthOp3
                    currentRevenuePriceRisePerKwhCommercials = commercialKwhRiseFourthOp3
                    
                elif(startingYearPretax3 == fifthYearPriceRise + 1 and firstYearPriceRise != 0 and firstYearPriceRise > startingYear and secondYearPriceRise != 0 and secondYearPriceRise > firstYearPriceRise
                    and thirdYearPriceRise != 0 and thirdYearPriceRise > secondYearPriceRise and fourthYearPriceRise != 0 and fourthYearPriceRise > thirdYearPriceRise
                    and fifthYearPriceRise != 0 and fifthYearPriceRise > fourthYearPriceRise):
                    currentResidentialFixedCost = residentialFixedCostRiseFifthOp3
                    currentCommercialFixedCost = commercialFixedCostRiseFifthOp3

                    currentRevenuePriceRisePerKwhResidentials = residentialKwhRiseFifthOp3
                    currentRevenuePriceRisePerKwhCommercials = commercialKwhRiseFifthOp3

            
                currentYearlyRevenueFixedCost = (currentResidentials * currentResidentialFixedCost) + (currentCommercials * currentCommercialFixedCost)

                currentAnualConsumptionCoveredResidentials = valueResidentials * monthsNumber * currentResidentials
                currentAnualConsumptionCoveredCommercials = valueCommercials * monthsNumber * currentCommercials
                
                energyPostIncreaseResidentialOp3 = currentEnergyRequiredResidentials * Decimal(math.pow((1 + growthResidential), i))
                energyPostIncreaseCommercialOp3 = currentEnergyRequiredCommercials * Decimal(math.pow((1 + growthCommercial), i))
            
                currentDiscountRateOp3 = Decimal((1 / math.pow((1 + (discountRate/100)), (i+1))))
                
                currentYearlyPostConsumptionResidentials = energyPostIncreaseResidentialOp3 - currentAnualConsumptionCoveredResidentials
                currentYearlyPostConsumptionCommercials = energyPostIncreaseCommercialOp3 - currentAnualConsumptionCoveredCommercials
                
                currentYearlyRevenuePerKwh = (currentRevenuePriceRisePerKwhResidentials * currentYearlyPostConsumptionResidentials) + (currentRevenuePriceRisePerKwhCommercials * currentYearlyPostConsumptionCommercials)
                
                currentTotalOption3Revenue = currentYearlyRevenueFixedCost + currentYearlyRevenuePerKwh
                
                currentNetCashflowDiscountedOption3 += (currentTotalOption3Revenue - yearlyOperationalExpenditureOption3 - expansion) * currentDiscountRateOp3

                currentCumulativeDiscountCashflowOption3 = currentCumulativeDiscountCashflowOption3 + ((currentTotalOption3Revenue - yearlyOperationalExpenditureOption3 - expansion) * currentDiscountRateOp3)

                cumulativeDiscountCashflowOption3.append(float(round(currentCumulativeDiscountCashflowOption3, 2)))

                
                
                currentNetCashflowOption3 = currentTotalOption3Revenue - yearlyOperationalExpenditureOption3
                
                yearlyOperationalExpenditureOption3 = (yearlyOperationalExpenditureOption3) * (1 + yearlyOmEscalator) * (1 - subsidyOperationalExpenditure)
                
                netCashflowOption3.append(currentNetCashflowOption3)
                
        preTaxNPVOption3 = round(currentNetCashflowDiscountedOption3 - totalCapex)
        preTaxIRROption3 = round(npf.irr(netCashflowOption3), 3) * 100

        context['preTaxNPVOption3'] = "{:,}".format(preTaxNPVOption3) #VALUE FOR SHOW IN NUMBERS
        context['preTaxIRROption3'] = "{:,}".format(preTaxIRROption3) #VALUE FOR SHOW IN NUMBERS
        context['preTaxNPVOption3Chart'] = preTaxNPVOption3 #VALUE FOR SHOW IN CHART
        context['preTaxIRROption3Chart'] = preTaxIRROption3 #VALUE FOR SHOW IN CHART
        
        context['cumulativeDiscountCashflowOption3'] = cumulativeDiscountCashflowOption3
    
    return render(request, 'base/resultsEconomic.html', context)

