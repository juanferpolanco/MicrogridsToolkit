from django.urls import path, re_path, register_converter
from . import views
from .views import *
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views
from base.encryptID import HashIdConverter

register_converter(HashIdConverter, "hashid")

urlpatterns = [
    #USERS
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('', MenuView.as_view(),name='menu'),
    path('changePassword/', CustomPasswordChangeView.as_view(), name='changePassword'),
    path('register/', RegisterPage.as_view(), name='register'),

    path("password_reset/", auth_views.PasswordResetView.as_view(template_name="base/password_reset.html"), name="password_reset"),
    path("password_reset/done/",auth_views.PasswordResetDoneView.as_view(template_name="base/password_reset_sent.html"),name="password_reset_done"),
    path("reset/<uidb64>/<token>/",auth_views.PasswordResetConfirmView.as_view(template_name="base/password_reset_form.html"),name="password_reset_confirm",),
    path("reset/done/",auth_views.PasswordResetCompleteView.as_view(template_name="base/password_reset_done.html"),name="password_reset_complete",),
    #PROJECTS
    path('project-list/', listProject, name='project-list'),
    path('project-create/', createProject, name='project-create'),
    path('project-edit/<hashid:id>', editProject, name='project-edit'),
    path('project-details/<hashid:id>', projectDetails, name='project-details'),
    path('project-delete/<hashid:id>', deleteProject, name='project-delete'),
    
    
    #GENERAL
    path('project-details/general/<hashid:id>', general, name='general'),
    path('generalLoc/<hashid:id>', createG_LocationDetails, name='generalLocation'),
    path('generalDem/<hashid:id>', createG_Demography, name='generalDemography'),
    path('generalInc/<hashid:id>', createG_Income, name='generalIncome'),
    path('generalFue/<hashid:id>', createG_Fuel, name='generalFuel'),
    path('generalDis/<hashid:id>', createG_Discount, name='generalDiscount'),
    path('generalTim/<hashid:id>', createG_Time, name='generalTime'),
    path('generalTie/<hashid:id>', createG_Tier, name='generalTier'),
    #PLANT_EXPENDITURE
    path('project-details/plantExpenditure/<hashid:id>', plantExpenditure, name='plantExpenditure'),
    path('plantDet/<hashid:id>', createP_Details, name='plantDetails'),
    path('plantCap/<hashid:id>', createP_Capital, name='plantCapital'),
    path('plantOpe/<hashid:id>', createP_Operational, name='plantOperational'),
    path('plantRep/<hashid:id>', createP_Replacement, name='plantReplacement'),
    path('plantSub/<hashid:id>', createP_Subsidy, name='plantSubsidy'),
    #REVENUE_ELECTRICITY
    path('project-details/revenueElectricity/<hashid:id>', revenueElectricity, name='revenueElectricity'),
    path('revenueAve/<hashid:id>', createR_Average, name='revenueAverage'),
    path('revenueGro/<hashid:id>', createR_Growth, name='revenueGrowth'),
    path('revenueOpt/<hashid:id>', createR_Options, name='revenueOptions'),
    path('revenueRat/<hashid:id>', createR_Rates, name='revenueRates'),
    path('revenueCha/<hashid:id>', createR_Changes, name='revenueChanges'),
    #CO2
    path('project-details/co2/<hashid:id>', co2, name = 'co2'),
    path('co2Carbon/<hashid:id>', createCo2, name = 'co2Carbon'),
    
    #Results
    path('project-details/resultsOverview/<hashid:id>', resultsOverview, name='resultsOverview'),
    path('project-details/resultsCarbon/<hashid:id>', resultsCarbon, name='resultsCarbon'),
    path('project-details/resultsEconomic/<hashid:id>', resultsEconomic, name='resultsEconomic'),
    
]
