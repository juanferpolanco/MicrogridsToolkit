from contextlib import nullcontext
from os import truncate
from queue import Empty
from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.db.models.fields import DecimalField
from django.core.exceptions import ValidationError
from django.core.validators import DecimalValidator, MinValueValidator
from django.urls import reverse
from base.encryptID import h_encode

# Create your models here.

class Project(models.Model):
    prj_user = models.ForeignKey(User, null=True, blank=True, on_delete=CASCADE)
    prj_name = models.CharField(max_length=100, null=True)
    prj_description = models.TextField(null=True, blank=True)
    prj_datecreated = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.prj_name

###############################################################       GENERAL     ####################################################################

class G_LocationDetails(models.Model):
    gen_idProject = models.ForeignKey (Project, blank=True, on_delete=CASCADE)
    gen_idUser = models.ForeignKey (User, blank=True, on_delete=CASCADE)
    gen_SettlementName = models.CharField (max_length=50, null=True)
    gen_StateName = models.CharField (max_length=50, null=True)
    gen_CountryName = models.CharField (max_length=50, null=True)
    gen_Currency = models.CharField (max_length=5, null=True)
    gen_Notes = models.TextField (null=True, blank=True)
    gen_Source = models.TextField (null=True, blank=True)

class G_Demography(models.Model):
    gen_idProject = models.ForeignKey (Project, null=True, blank=True, on_delete=CASCADE)
    gen_idUser = models.ForeignKey (User, null=True, blank=True, on_delete=CASCADE)
    gen_PopulationSettlement = models.IntegerField (null=True, blank=True)
    gen_PopulationSettlementUnit = models.CharField (max_length=50, null=True, blank=True)
    gen_PopulationConnected = models.IntegerField (null=True, blank=True)
    gen_PopulationConnectedUnit = models.CharField (max_length=50, null=True, blank=True)
    gen_ResidentialProperties = models.IntegerField (null=True, blank=True)
    gen_ResidentialPropertiesUnit = models.CharField (max_length=50, null=True, blank=True)
    gen_ResidentialConnected = models.IntegerField (null=True, blank=True)
    gen_ResidentialConnectedUnit = models.CharField (max_length=50, null=True, blank=True)
    gen_CommercialProperties = models.IntegerField (null=True, blank=True)
    gen_CommercialPropertiesUnit = models.CharField (max_length=50, null=True, blank=True)
    gen_CommercialConnected = models.IntegerField (null=True, blank=True)
    gen_CommercialConnectedUnit = models.CharField (max_length=50, null=True, blank=True)   
    gen_Notes = models.TextField (null=True, blank=True)
    gen_Source = models.TextField (null=True, blank=True)
    
    def save(self, *args, **kwargs):
        
        #FOR SAVING EMPTY INPUT IN INTEGER FIELDS
        if self.gen_PopulationSettlement == '' or self.gen_PopulationSettlement is None:
            self.gen_PopulationSettlement = 0
        
        if self.gen_PopulationConnected == '' or self.gen_PopulationConnected is None:
            self.gen_PopulationConnected = 0
        
        if self.gen_ResidentialProperties == '' or self.gen_ResidentialProperties is None:
            self.gen_ResidentialProperties = 0
        
        if self.gen_ResidentialConnected == '' or self.gen_ResidentialConnected is None:
            self.gen_ResidentialConnected = 0

        if self.gen_CommercialProperties == '' or self.gen_CommercialProperties is None:
            self.gen_CommercialProperties = 0
        
        if self.gen_CommercialConnected == '' or self.gen_CommercialConnected is None:
            self.gen_CommercialConnected = 0
            
        super(G_Demography, self).save(*args, **kwargs)


class G_Income(models.Model):
    gen_idProject = models.ForeignKey (Project, null=True, blank=True, on_delete=CASCADE)
    gen_idUser = models.ForeignKey (User, null=True, blank=True, on_delete=CASCADE)
    gen_ResidentialIncome = models.DecimalField (max_digits=10, decimal_places=2, null=True, blank=True, validators=[DecimalValidator])
    gen_ResidentialIncomeUnit = models.CharField (max_length=50, null=True, blank=True)
    gen_ResidentialWillingness = models.DecimalField (max_digits=10, decimal_places=2, null=True, blank=True, validators=[DecimalValidator])
    gen_ResidentialWillingnessUnit = models.CharField (max_length=50, null=True, blank=True)
    gen_CommercialIncome = models.DecimalField (max_digits=10, decimal_places=2, null=True, blank=True, validators=[DecimalValidator])
    gen_CommercialIncomeUnit = models.CharField (max_length=50, null=True, blank=True)  
    gen_CommercialWillingness = models.DecimalField (max_digits=10, decimal_places=2, null=True, blank=True, validators=[DecimalValidator])
    gen_CommercialWillingnessUnit = models.CharField (max_length=50, null=True, blank=True)  
    gen_Notes = models.TextField (null=True, blank=True)
    gen_Source = models.TextField (null=True, blank=True)

    def save(self, *args, **kwargs):
        
        #FOR SAVING EMPTY INPUT IN DECIMAL FIELDS
        if self.gen_ResidentialIncome == '' or self.gen_ResidentialIncome is None:
            self.gen_ResidentialIncome = 0
        
        if self.gen_ResidentialWillingness == '' or self.gen_ResidentialWillingness is None:
            self.gen_ResidentialWillingness = 0
        
        if self.gen_CommercialIncome == '' or self.gen_CommercialIncome is None:
            self.gen_CommercialIncome = 0
        
        if self.gen_CommercialWillingness == '' or self.gen_CommercialWillingness is None:
            self.gen_CommercialWillingness = 0
            
        super(G_Income, self).save(*args, **kwargs)

class G_Fuel(models.Model):
    gen_idProject = models.ForeignKey (Project, null=True, blank=True, on_delete=CASCADE)
    gen_idUser = models.ForeignKey (User, null=True, blank=True, on_delete=CASCADE)
    gen_CommercialFuelUsed = models.CharField (max_length=20, null=True, blank=True)
    gen_CommercialFuelMonthly = models.DecimalField (max_digits=10, decimal_places=2, null=True, blank=True, validators=[DecimalValidator])
    gen_CommercialFuelMonthlyUnit = models.CharField (max_length=50, null=True, blank=True)
    gen_CommercialFuelCost = models.DecimalField (max_digits=10, decimal_places=2, null=True, blank=True, validators=[DecimalValidator])
    gen_CommercialFuelCostUnit = models.CharField (max_length=50, null=True, blank=True)
    gen_ResidentialFuelUsed = models.CharField (max_length=20, null=True, blank=True)
    gen_ResidentialFuelMonthly = models.DecimalField (max_digits=10, decimal_places=2, null=True, blank=True, validators=[DecimalValidator])
    gen_ResidentialFuelMonthlyUnit = models.CharField (max_length=50, null=True, blank=True)
    gen_ResidentialFuelCost = models.DecimalField (max_digits=10, decimal_places=2, null=True, blank=True, validators=[DecimalValidator])
    gen_ResidentialFuelCostUnit = models.CharField (max_length=50, null=True, blank=True)
    gen_Notes = models.TextField (null=True, blank=True)
    gen_Source = models.TextField (null=True, blank=True)

    def save(self, *args, **kwargs):

        #FOR SAVING EMPTY INPUT IN DECIMAL FIELDS
        if self.gen_CommercialFuelMonthly == '' or self.gen_CommercialFuelMonthly is None:
            self.gen_CommercialFuelMonthly = 0
        
        if self.gen_CommercialFuelCost == '' or self.gen_CommercialFuelCost is None:
            self.gen_CommercialFuelCost = 0
        
        if self.gen_ResidentialFuelMonthly == '' or self.gen_ResidentialFuelMonthly is None:
            self.gen_ResidentialFuelMonthly = 0
            
        if self.gen_ResidentialFuelCost == '' or self.gen_ResidentialFuelCost is None:
            self.gen_ResidentialFuelCost = 0    
            
        super(G_Fuel, self).save(*args, **kwargs)

class G_Discount(models.Model):
    gen_idProject = models.ForeignKey (Project, null=True, blank=True, on_delete=CASCADE)
    gen_idUser = models.ForeignKey (User, null=True, blank=True, on_delete=CASCADE)
    gen_DiscountRate = models.DecimalField (max_digits=10, decimal_places=2, null=True, blank=True, validators=[DecimalValidator])
    gen_DiscountRateUnit = models.CharField (max_length=50, null=True, blank=True)
    gen_Notes = models.TextField (null=True, blank=True)
    gen_Source = models.TextField (null=True, blank=True)

    def save(self, *args, **kwargs):

        #FOR SAVING EMPTY INPUT IN DECIMAL FIELDS
        if self.gen_DiscountRate == '' or self.gen_DiscountRate is None:
            self.gen_DiscountRate = 0
        
        super(G_Discount, self).save(*args, **kwargs)

class G_Time(models.Model):
    gen_idProject = models.ForeignKey (Project, null=True, blank=True, on_delete=CASCADE)
    gen_idUser = models.ForeignKey (User, null=True, blank=True, on_delete=CASCADE)
    gen_StartingYear = models.IntegerField(null=True, blank=True)
    gen_ProjectionPeriod = models.IntegerField(null=True, blank=True)
    gen_ProjectionPeriodUnit = models.CharField (max_length=50, null=True, blank=True)
    gen_MonthsNumber = models.IntegerField(null=True, blank=True)
    gen_MonthsNumberUnit = models.CharField (max_length=50, null=True, blank=True)
    gen_Notes = models.TextField (null=True, blank=True)
    gen_Source = models.TextField (null=True, blank=True)
    
    def save(self, *args, **kwargs):

        #FOR SAVING EMPTY INPUT IN DECIMAL FIELDS
        if self.gen_StartingYear == '' or self.gen_StartingYear is None:
            self.gen_StartingYear = 0
        
        if self.gen_ProjectionPeriod == '' or self.gen_ProjectionPeriod is None:
            self.gen_ProjectionPeriod = 0
        
        if self.gen_MonthsNumber == '' or self.gen_MonthsNumber is None:
            self.gen_MonthsNumber = 0
        
        super(G_Time, self).save(*args, **kwargs)

class G_Tier(models.Model):
    gen_idProject = models.ForeignKey (Project, null=True, blank=True, on_delete=CASCADE)
    gen_idUser = models.ForeignKey (User, null=True, blank=True, on_delete=CASCADE)
    gen_WorldBankTier = models.CharField (max_length=50, null=True, blank=True)
    gen_WorldBankTierUnit = models.CharField (max_length=50, null=True, blank=True)
    gen_Notes = models.TextField (null=True, blank=True)
    gen_Source = models.TextField (null=True, blank=True)

###############################################################       PLAN EXPENDITURE     ####################################################################

class P_Details(models.Model):
    pla_idProject = models.ForeignKey (Project, null=True, blank=True, on_delete=CASCADE)
    pla_idUser = models.ForeignKey (User, null=True, blank=True, on_delete=CASCADE)
    pla_PlantSize = models.DecimalField (max_digits=10, decimal_places=2, null=True, blank=True, validators=[DecimalValidator])
    pla_PlantSizeUnit = models.CharField (max_length=50, null=True, blank=True)
    pla_BatterySize = models.DecimalField (max_digits=10, decimal_places=2, null=True, blank=True, validators=[DecimalValidator])
    pla_BatterySizeUnit = models.CharField (max_length=50, null=True, blank=True)
    pla_AnnualDegradation = models.DecimalField (max_digits=10, decimal_places=2, null=True, blank=True, validators=[DecimalValidator])
    pla_AnnualDegradationUnit = models.CharField (max_length=50, null=True, blank=True)
    pla_DailyGeneration = models.DecimalField (max_digits=10, decimal_places=2, null=True, blank=True, validators=[DecimalValidator])
    pla_DailyGenerationUnit = models.CharField (max_length=50, null=True, blank=True)
    pla_Notes = models.TextField (null=True, blank=True)
    pla_Source = models.TextField (null=True, blank=True)

    def save(self, *args, **kwargs):

        #FOR SAVING EMPTY INPUT IN DECIMAL FIELDS
        if self.pla_PlantSize == '':
            self.pla_PlantSize = 0

        if self.pla_BatterySize == '':
            self.pla_BatterySize = 0
        
        if self.pla_AnnualDegradation == '':
            self.pla_AnnualDegradation = 0
        
        if self.pla_DailyGeneration == '':
            self.pla_DailyGeneration = 0
        
        super(P_Details, self).save(*args, **kwargs)

class P_Capital(models.Model):
    pla_idProject = models.ForeignKey (Project, null=True, blank=True, on_delete=CASCADE)
    pla_idUser = models.ForeignKey (User, null=True, blank=True, on_delete=CASCADE)
    pla_Land = models.DecimalField (max_digits=10, decimal_places=2, null=True, blank=True, validators=[DecimalValidator])
    pla_LandUnit = models.CharField (max_length=50, null=True, blank=True)
    pla_PanelsTurbines = models.DecimalField (max_digits=10, decimal_places=2, null=True, blank=True, validators=[DecimalValidator])
    pla_PanelsTurbinesUnit = models.CharField (max_length=50, null=True, blank=True)
    pla_Switchgear = models.DecimalField (max_digits=10, decimal_places=2, null=True, blank=True, validators=[DecimalValidator])
    pla_SwitchgearUnit = models.CharField (max_length=50, null=True, blank=True)
    pla_ProtectionSystem = models.DecimalField (max_digits=10, decimal_places=2, null=True, blank=True, validators=[DecimalValidator])
    pla_ProtectionSystemUnit = models.CharField (max_length=50, null=True, blank=True)
    pla_Transformer = models.DecimalField (max_digits=10, decimal_places=2, null=True, blank=True, validators=[DecimalValidator])
    pla_TransformerUnit = models.CharField (max_length=50, null=True, blank=True)
    pla_Wiring = models.DecimalField (max_digits=10, decimal_places=2, null=True, blank=True, validators=[DecimalValidator])
    pla_WiringUnit = models.CharField (max_length=50, null=True, blank=True)
    pla_Meters = models.DecimalField (max_digits=10, decimal_places=2, null=True, blank=True, validators=[DecimalValidator])
    pla_MetersUnit = models.CharField (max_length=50, null=True, blank=True)
    pla_Batteries = models.DecimalField (max_digits=10, decimal_places=2, null=True, blank=True, validators=[DecimalValidator])
    pla_BatteriesUnit = models.CharField (max_length=50, null=True, blank=True)
    pla_Inverters = models.DecimalField (max_digits=10, decimal_places=2, null=True, blank=True, validators=[DecimalValidator])
    pla_InvertersUnit = models.CharField (max_length=50, null=True, blank=True)
    pla_ControlCost = models.DecimalField (max_digits=10, decimal_places=2, null=True, blank=True, validators=[DecimalValidator])
    pla_ControlCostUnit = models.CharField (max_length=50, null=True, blank=True)
    pla_TransportationCost = models.DecimalField (max_digits=10, decimal_places=2, null=True, blank=True, validators=[DecimalValidator])
    pla_TransportationCostUnit = models.CharField (max_length=50, null=True, blank=True)
    pla_ConstructionCost = models.DecimalField (max_digits=10, decimal_places=2, null=True, blank=True, validators=[DecimalValidator])
    pla_ConstructionCostUnit = models.CharField (max_length=50, null=True, blank=True)
    pla_AncillaryCost = models.DecimalField (max_digits=10, decimal_places=2, null=True, blank=True, validators=[DecimalValidator])
    pla_AncillaryCostUnit = models.CharField (max_length=50, null=True, blank=True)
    pla_InstallationCost = models.DecimalField (max_digits=10, decimal_places=2, null=True, blank=True, validators=[DecimalValidator])
    pla_InstallationCostUnit = models.CharField (max_length=50, null=True, blank=True)
    pla_Notes = models.TextField (null=True, blank=True)
    pla_Source = models.TextField (null=True, blank=True)

    def save(self, *args, **kwargs):

        #FOR SAVING EMPTY INPUT IN DECIMAL FIELDS
        if self.pla_Land == '' or self.pla_Land is None:
            self.pla_Land = 0

        if self.pla_PanelsTurbines == '' or self.pla_PanelsTurbines is None:
            self.pla_PanelsTurbines = 0
        
        if self.pla_Switchgear == '' or self.pla_Switchgear is None:
            self.pla_Switchgear = 0
        
        if self.pla_ProtectionSystem == '' or self.pla_ProtectionSystem is None:
            self.pla_ProtectionSystem = 0
        
        if self.pla_Transformer == '' or self.pla_Transformer is None:
            self.pla_Transformer = 0
        
        if self.pla_Wiring == '' or self.pla_Wiring is None:
            self.pla_Wiring = 0

        if self.pla_Meters == '' or self.pla_Meters is None:
            self.pla_Meters = 0
        
        if self.pla_Batteries == '' or self.pla_Batteries is None:
            self.pla_Batteries = 0

        if self.pla_Inverters == '' or self.pla_Inverters is None:
            self.pla_Inverters = 0

        if self.pla_ControlCost == '' or self.pla_ControlCost is None:
            self.pla_ControlCost = 0

        if self.pla_TransportationCost == '' or self.pla_TransportationCost is None:
            self.pla_TransportationCost = 0

        if self.pla_ConstructionCost == '' or self.pla_ConstructionCost is None:
            self.pla_ConstructionCost = 0

        if self.pla_AncillaryCost == '' or self.pla_AncillaryCost is None:
            self.pla_AncillaryCost = 0

        if self.pla_InstallationCost == '' or self.pla_InstallationCost is None:
            self.pla_InstallationCost = 0
        
        super(P_Capital, self).save(*args, **kwargs)

class P_Operational(models.Model):
    pla_idProject = models.ForeignKey (Project, null=True, blank=True, on_delete=CASCADE)
    pla_idUser = models.ForeignKey (User, null=True, blank=True, on_delete=CASCADE)
    pla_OperationalExpenditure = models.DecimalField (max_digits=10, decimal_places=2, null=True, blank=True, validators=[DecimalValidator])
    pla_OperationalExpenditureUnit = models.CharField (max_length=50, null=True, blank=True)
    pla_OMEscalator = models.DecimalField (max_digits=10, decimal_places=2, null=True, blank=True, validators=[DecimalValidator])
    pla_OMEscalatorUnit = models.CharField (max_length=50, null=True, blank=True)
    pla_Notes = models.TextField (null=True, blank=True)
    pla_Source = models.TextField (null=True, blank=True)

    def save(self, *args, **kwargs):

        #FOR SAVING EMPTY INPUT IN DECIMAL FIELDS
        if self.pla_OperationalExpenditure == '' or self.pla_OperationalExpenditure is None:
            self.pla_OperationalExpenditure = 0

        if self.pla_OMEscalator == '' or self.pla_OMEscalator is None:
            self.pla_OMEscalator = 0

        super(P_Operational, self).save(*args, **kwargs)
    
class P_Replacement(models.Model):
    pla_idProject = models.ForeignKey (Project, null=True, blank=True, on_delete=CASCADE)
    pla_idUser = models.ForeignKey (User, null=True, blank=True, on_delete=CASCADE)
    pla_NumberExpansions = models.IntegerField (null=True, blank=True)
    pla_FirstExpansion = models.IntegerField (null=True, blank=True)
    pla_SecondExpansion = models.IntegerField (null=True, blank=True)
    pla_ThirdExpansion = models.IntegerField (null=True, blank=True)
    pla_FirstPlantAdded = models.DecimalField (max_digits=10, decimal_places=2, null=True, blank=True, validators=[DecimalValidator])
    pla_FirstPlantAddedUnit = models.CharField (max_length=50, null=True, blank=True) 
    pla_FirstTotalExpenditure = models.DecimalField (max_digits=10, decimal_places=2, null=True, blank=True, validators=[DecimalValidator])
    pla_FirstTotalExpenditureUnit = models.CharField (max_length=50, null=True, blank=True)
    pla_FirstBatteriesSize = models.DecimalField (max_digits=10, decimal_places=2, null=True, blank=True, validators=[DecimalValidator])
    pla_FirstBatteriesSizeUnit = models.CharField (max_length=50, null=True, blank=True)
    pla_FirstBatteriesCost = models.DecimalField (max_digits=10, decimal_places=2, null=True, blank=True, validators=[DecimalValidator])
    pla_FirstBatteriesCostUnit = models.CharField (max_length=50, null=True, blank=True)
    pla_FirstBatteriesReplaced = models.DecimalField (max_digits=10, decimal_places=2, null=True, blank=True, validators=[DecimalValidator])
    pla_FirstBatteriesReplacedUnit = models.CharField (max_length=50, null=True, blank=True)
    pla_FirstHomesAdded = models.IntegerField (null=True, blank=True)
    pla_FirstCommercialAdded = models.IntegerField (null=True, blank=True)
    pla_SecondPlantAdded = models.DecimalField (max_digits=10, decimal_places=2, null=True, blank=True, validators=[DecimalValidator])
    pla_SecondPlantAddedUnit = models.CharField (max_length=50, null=True, blank=True)
    pla_SecondTotalExpenditure = models.DecimalField (max_digits=10, decimal_places=2, null=True, blank=True, validators=[DecimalValidator])
    pla_SecondTotalExpenditureUnit = models.CharField (max_length=50, null=True, blank=True)
    pla_SecondBatteriesSize = models.DecimalField (max_digits=10, decimal_places=2, null=True, blank=True, validators=[DecimalValidator])
    pla_SecondBatteriesSizeUnit = models.CharField (max_length=50, null=True, blank=True)
    pla_SecondBatteriesCost = models.DecimalField (max_digits=10, decimal_places=2, null=True, blank=True, validators=[DecimalValidator])
    pla_SecondBatteriesCostUnit = models.CharField (max_length=50, null=True, blank=True)
    pla_SecondBatteriesReplaced = models.DecimalField (max_digits=10, decimal_places=2, null=True, blank=True, validators=[DecimalValidator])
    pla_SecondBatteriesReplacedUnit = models.CharField (max_length=50, null=True, blank=True)
    pla_SecondHomesAdded = models.IntegerField (null=True, blank=True)
    pla_SecondCommercialAdded = models.IntegerField (null=True, blank=True)
    pla_ThirdPlantAdded = models.DecimalField (max_digits=10, decimal_places=2, null=True, blank=True, validators=[DecimalValidator])
    pla_ThirdPlantAddedUnit = models.CharField (max_length=50, null=True, blank=True)
    pla_ThirdTotalExpenditure = models.DecimalField (max_digits=10, decimal_places=2, null=True, blank=True, validators=[DecimalValidator])
    pla_ThirdTotalExpenditureUnit = models.CharField (max_length=50, null=True, blank=True)
    pla_ThirdBatteriesSize = models.DecimalField (max_digits=10, decimal_places=2, null=True, blank=True, validators=[DecimalValidator])
    pla_ThirdBatteriesSizeUnit = models.CharField (max_length=50, null=True, blank=True)
    pla_ThirdBatteriesCost = models.DecimalField (max_digits=10, decimal_places=2, null=True, blank=True, validators=[DecimalValidator])
    pla_ThirdBatteriesCostUnit = models.CharField (max_length=50, null=True, blank=True)
    pla_ThirdBatteriesReplaced = models.DecimalField (max_digits=10, decimal_places=2, null=True, blank=True, validators=[DecimalValidator])
    pla_ThirdBatteriesReplacedUnit = models.CharField (max_length=50, null=True, blank=True)
    pla_ThirdHomesAdded = models.IntegerField (null=True, blank=True)
    pla_ThirdCommercialAdded = models.IntegerField (null=True, blank=True)
    pla_Notes = models.TextField (null=True, blank=True)
    pla_Source = models.TextField (null=True, blank=True)

    def save(self, *args, **kwargs):

        #FOR SAVING EMPTY INPUT IN DECIMAL FIELDS
        if self.pla_FirstPlantAdded == '' or self.pla_FirstPlantAdded is None:
            self.pla_FirstPlantAdded = 0
            
        if self.pla_FirstTotalExpenditure == '' or self.pla_FirstTotalExpenditure is None:
            self.pla_FirstTotalExpenditure = 0
        
        if self.pla_FirstBatteriesSize == '' or self.pla_FirstBatteriesSize is None:
            self.pla_FirstBatteriesSize = 0
        
        if self.pla_FirstBatteriesCost == '' or self.pla_FirstBatteriesCost is None:
            self.pla_FirstBatteriesCost = 0
        
        if self.pla_FirstBatteriesReplaced == '' or self.pla_FirstBatteriesReplaced is None:
            self.pla_FirstBatteriesReplaced = 0
        
        if self.pla_SecondPlantAdded == '' or self.pla_SecondPlantAdded is None:
            self.pla_SecondPlantAdded = 0

        if self.pla_SecondTotalExpenditure == '' or self.pla_SecondTotalExpenditure is None:
            self.pla_SecondTotalExpenditure = 0
        
        if self.pla_SecondBatteriesSize == '' or self.pla_SecondBatteriesSize is None:
            self.pla_SecondBatteriesSize = 0

        if self.pla_SecondBatteriesCost == '' or self.pla_SecondBatteriesCost is None:
            self.pla_SecondBatteriesCost = 0

        if self.pla_SecondBatteriesReplaced == '' or self.pla_SecondBatteriesReplaced is None:
            self.pla_SecondBatteriesReplaced = 0

        if self.pla_ThirdPlantAdded == '' or self.pla_ThirdPlantAdded is None:
            self.pla_ThirdPlantAdded = 0

        if self.pla_ThirdTotalExpenditure == '' or self.pla_ThirdTotalExpenditure is None:
            self.pla_ThirdTotalExpenditure = 0

        if self.pla_ThirdBatteriesSize == '' or self.pla_ThirdBatteriesSize is None:
            self.pla_ThirdBatteriesSize = 0

        if self.pla_ThirdBatteriesCost == '' or self.pla_ThirdBatteriesCost is None:
            self.pla_ThirdBatteriesCost = 0

        if self.pla_ThirdBatteriesReplaced == '' or self.pla_ThirdBatteriesReplaced is None:
            self.pla_ThirdBatteriesReplaced = 0

        #FOR SAVING EMPTY INPUT IN INTEGER FIELDS
        if self.pla_NumberExpansions == ''or self.pla_NumberExpansions is None:
            self.pla_NumberExpansions = 0

        if self.pla_FirstExpansion == '' or self.pla_FirstExpansion is None:
            self.pla_FirstExpansion = 0
            
        if self.pla_SecondExpansion == '' or self.pla_SecondExpansion is None:
            self.pla_SecondExpansion = 0
            
        if self.pla_ThirdExpansion == '' or self.pla_ThirdExpansion is None:
            self.pla_ThirdExpansion = 0
        
        if self.pla_FirstHomesAdded == '' or self.pla_FirstHomesAdded is None:
            self.pla_FirstHomesAdded = 0
        
        if self.pla_FirstCommercialAdded == '' or self.pla_FirstCommercialAdded is None:
            self.pla_FirstCommercialAdded = 0
        
        if self.pla_SecondHomesAdded == '' or self.pla_SecondHomesAdded is None:
            self.pla_SecondHomesAdded = 0
        
        if self.pla_SecondCommercialAdded == '' or self.pla_SecondCommercialAdded is None:
            self.pla_SecondCommercialAdded = 0
        
        if self.pla_ThirdHomesAdded == '' or self.pla_ThirdHomesAdded is None:
            self.pla_ThirdHomesAdded = 0
        
        if self.pla_ThirdCommercialAdded == '' or self.pla_ThirdCommercialAdded is None:
            self.pla_ThirdCommercialAdded = 0
        
        super(P_Replacement, self).save(*args, **kwargs)

class P_Subsidy(models.Model):
    pla_idProject = models.ForeignKey (Project, null=True, blank=True, on_delete=CASCADE)
    pla_idUser = models.ForeignKey (User, null=True, blank=True, on_delete=CASCADE)
    pla_SubsidyCapital = models.DecimalField (max_digits=10, decimal_places=2, null=True, blank=True, validators=[DecimalValidator])
    pla_SubsidyCapitalUnit = models.CharField (max_length=50, null=True, blank=True)
    pla_SubsidyOperational = models.DecimalField (max_digits=10, decimal_places=2, null=True, blank=True, validators=[DecimalValidator])
    pla_SubsidyOperationalUnit = models.CharField (max_length=50, null=True, blank=True)
    pla_SubsidyReplacement = models.DecimalField (max_digits=10, decimal_places=2, null=True, blank=True, validators=[DecimalValidator])
    pla_SubsidyReplacementUnit = models.CharField (max_length=50, null=True, blank=True)
    pla_Notes = models.TextField (null=True, blank=True)
    pla_Source = models.TextField (null=True, blank=True) 
    
    def save(self, *args, **kwargs):

        #FOR SAVING EMPTY INPUT IN DECIMAL FIELDS
        if self.pla_SubsidyCapital == '':
            self.pla_SubsidyCapital = 0

        if self.pla_SubsidyOperational == '':
            self.pla_SubsidyOperational = 0

        if self.pla_SubsidyReplacement == '':
            self.pla_SubsidyReplacement = 0

        super(P_Subsidy, self).save(*args, **kwargs)

###############################################################       REVENUE ELECTRICITY     ####################################################################

class R_Average(models.Model):
    rev_idProject = models.ForeignKey (Project, null=True, blank=True, on_delete=CASCADE)
    rev_idUser = models.ForeignKey (User, null=True, blank=True, on_delete=CASCADE)
    rev_ResidentialConsump = models.DecimalField (max_digits=10, decimal_places=2, null=True, blank=True, validators=[DecimalValidator])
    rev_ResidentialConsumpUnit = models.CharField (max_length=50, null=True, blank=True)
    rev_CommercialConsump = models.DecimalField (max_digits=10, decimal_places=2, null=True, blank=True, validators=[DecimalValidator])
    rev_CommercialConsumpUnit = models.CharField (max_length=50, null=True, blank=True)
    rev_Notes = models.TextField (null=True, blank=True)
    rev_Source = models.TextField (null=True, blank=True) 

    def save(self, *args, **kwargs):

        #FOR SAVING EMPTY INPUT IN DECIMAL FIELDS
        if self.rev_ResidentialConsump == '':
            self.rev_ResidentialConsump = 0

        if self.rev_CommercialConsump == '':
            self.rev_CommercialConsump = 0

        super(R_Average, self).save(*args, **kwargs)

class R_Growth(models.Model):
    rev_idProject = models.ForeignKey (Project, null=True, blank=True, on_delete=CASCADE)
    rev_idUser = models.ForeignKey (User, null=True, blank=True, on_delete=CASCADE)
    rev_ResidentialGrowth = models.DecimalField (max_digits=10, decimal_places=2, null=True, blank=True, validators=[DecimalValidator])
    rev_ResidentialGrowthUnit = models.CharField (max_length=50, null=True, blank=True)
    rev_CommercialGrowth = models.DecimalField (max_digits=10, decimal_places=2, null=True, blank=True, validators=[DecimalValidator])
    rev_CommercialGrowthUnit = models.CharField (max_length=50, null=True, blank=True)
    rev_Notes = models.TextField (null=True, blank=True)
    rev_Source = models.TextField (null=True, blank=True)

    def save(self, *args, **kwargs):

        #FOR SAVING EMPTY INPUT IN DECIMAL FIELDS
        if self.rev_ResidentialGrowth == '':
            self.rev_ResidentialGrowth = 0

        if self.rev_CommercialGrowth == '':
            self.rev_CommercialGrowth = 0

        super(R_Growth, self).save(*args, **kwargs)

class R_Options(models.Model):
    rev_idProject = models.ForeignKey (Project, null=True, blank=True, on_delete=CASCADE)
    rev_idUser = models.ForeignKey (User, null=True, blank=True, on_delete=CASCADE)
    """ rev_FixedCostOp1 = models.BooleanField(null=True, blank=True, default=False) """
    rev_FixedCostOp1 = models.BooleanField(null=True, blank=True)
    rev_KwhConsumpOp2 = models.BooleanField(null=True, blank=True)
    rev_FixedCostKwhOp3 = models.BooleanField(null=True, blank=True)
    rev_UnchargedResidentialOp3 = models.DecimalField (max_digits=10, decimal_places=2, null=True, blank=True, validators=[DecimalValidator])
    rev_UnchargedResidentialOp3Unit = models.CharField (max_length=50, null=True, blank=True)
    rev_UnchargedCommercialOp3 = models.DecimalField (max_digits=10, decimal_places=2, null=True, blank=True, validators=[DecimalValidator])
    rev_UnchargedCommercialOp3Unit = models.CharField (max_length=50, null=True, blank=True)
    rev_Notes = models.TextField (null=True, blank=True)
    rev_Source = models.TextField (null=True, blank=True)

    def save(self, *args, **kwargs):

        #FOR SAVING EMPTY INPUT IN DECIMAL FIELDS
        if self.rev_UnchargedResidentialOp3 == '':
            self.rev_UnchargedResidentialOp3 = 0

        if self.rev_UnchargedCommercialOp3 == '':
            self.rev_UnchargedCommercialOp3 = 0

        super(R_Options, self).save(*args, **kwargs)

class R_Rates(models.Model):
    rev_idProject = models.ForeignKey (Project, null=True, blank=True, on_delete=CASCADE)
    rev_idUser = models.ForeignKey (User, null=True, blank=True, on_delete=CASCADE)
    rev_FixedCostResidentialOp1 = models.DecimalField (max_digits=10, decimal_places=2, blank=True, validators=[DecimalValidator])
    rev_FixedCostResidentialOp1Unit = models.CharField (max_length=50, null=True, blank=True)
    rev_FixedCostCommercialOp1 = models.DecimalField (max_digits=10, decimal_places=2, null=True, blank=True, validators=[DecimalValidator])
    rev_FixedCostCommercialOp1Unit = models.CharField (max_length=50, null=True, blank=True)
    rev_KwhResidentialOp2 = models.DecimalField (max_digits=10, decimal_places=2, null=True, blank=True, validators=[DecimalValidator])
    rev_KwhResidentialOp2Unit = models.CharField (max_length=50, null=True, blank=True)
    rev_kwhCommercialOp2 = models.DecimalField (max_digits=10, decimal_places=2, null=True, blank=True, validators=[DecimalValidator])
    rev_kwhCommercialOp2Unit = models.CharField (max_length=50, null=True, blank=True)
    rev_FixedCostResidentialOp3 = models.DecimalField (max_digits=10, decimal_places=2, null=True, blank=True, validators=[DecimalValidator])
    rev_FixedCostResidentialOp3Unit = models.CharField (max_length=50, null=True, blank=True)
    rev_FixedCostCommercialOp3 = models.DecimalField (max_digits=10, decimal_places=2, null=True, blank=True, validators=[DecimalValidator])
    rev_FixedCostCommercialOp3Unit = models.CharField (max_length=50, null=True, blank=True)
    rev_KwhResidentialOp3 = models.DecimalField (max_digits=10, decimal_places=2, null=True, blank=True, validators=[DecimalValidator])
    rev_KwhResidentialOp3Unit = models.CharField (max_length=50, null=True, blank=True)
    rev_KwhCommercialOp3 = models.DecimalField (max_digits=10, decimal_places=2, null=True, blank=True, validators=[DecimalValidator])
    rev_KwhCommercialOp3Unit = models.CharField (max_length=50, null=True, blank=True)
    rev_Notes = models.TextField (null=True, blank=True)
    rev_Source = models.TextField (null=True, blank=True)

    def save(self, *args, **kwargs):

        #FOR SAVING EMPTY INPUT IN DECIMAL FIELDS
        if self.rev_FixedCostResidentialOp1 == '' or self.rev_FixedCostResidentialOp1 is None:
            self.rev_FixedCostResidentialOp1 = 0

        if self.rev_FixedCostCommercialOp1 == '' or self.rev_FixedCostCommercialOp1 is None:
            self.rev_FixedCostCommercialOp1 = 0
        
        if self.rev_KwhResidentialOp2 == '' or self.rev_KwhResidentialOp2 is None:
            self.rev_KwhResidentialOp2 = 0
        
        if self.rev_kwhCommercialOp2 == '' or self.rev_kwhCommercialOp2 is None:
            self.rev_kwhCommercialOp2 = 0
        
        if self.rev_FixedCostResidentialOp3 == '' or self.rev_FixedCostResidentialOp3 is None:
            self.rev_FixedCostResidentialOp3 = 0
        
        if self.rev_FixedCostCommercialOp3 == '' or self.rev_FixedCostCommercialOp3 is None:
            self.rev_FixedCostCommercialOp3 = 0

        if self.rev_KwhResidentialOp3 == '' or self.rev_KwhResidentialOp3 is None:
            self.rev_KwhResidentialOp3 = 0
        
        if self.rev_KwhCommercialOp3 == '' or self.rev_KwhCommercialOp3 is None:
            self.rev_KwhCommercialOp3 = 0
            
        super(R_Rates, self).save(*args, **kwargs)

class R_Changes(models.Model):
    rev_idProject = models.ForeignKey (Project, null=True, blank=True, on_delete=CASCADE)
    rev_idUser = models.ForeignKey (User, null=True, blank=True, on_delete=CASCADE)
    rev_FirstPriceRise = models.IntegerField (null=True, blank=True)
    rev_SecondPriceRise = models.IntegerField (null=True, blank=True)
    rev_ThirdPriceRise = models.IntegerField (null=True, blank=True)
    rev_FourthPriceRise = models.IntegerField (null=True, blank=True)
    rev_FifthPriceRise = models.IntegerField (null=True, blank=True)
    rev_FirstYearPercentage = models.DecimalField (max_digits=10, decimal_places=2, null=True, blank=True, validators=[DecimalValidator])
    rev_SecondYearPercentage = models.DecimalField (max_digits=10, decimal_places=2, null=True, blank=True, validators=[DecimalValidator])
    rev_ThirdYearPercentage = models.DecimalField (max_digits=10, decimal_places=2, null=True, blank=True, validators=[DecimalValidator])
    rev_FourthYearPercentage = models.DecimalField (max_digits=10, decimal_places=2, null=True, blank=True, validators=[DecimalValidator])
    rev_FifthYearPercentage = models.DecimalField (max_digits=10, decimal_places=2, null=True, blank=True, validators=[DecimalValidator])
    rev_Notes = models.TextField (null=True, blank=True)
    rev_Source = models.TextField (null=True, blank=True)

    def save(self, *args, **kwargs):

        #FOR SAVING EMPTY INPUT IN DECIMAL FIELDS
        if self.rev_FirstYearPercentage == '' or self.rev_FirstYearPercentage is None:
            self.rev_FirstYearPercentage = 0

        if self.rev_SecondYearPercentage == '' or self.rev_SecondYearPercentage is None:
            self.rev_SecondYearPercentage = 0
        
        if self.rev_ThirdYearPercentage == '' or self.rev_ThirdYearPercentage is None:
            self.rev_ThirdYearPercentage = 0
        
        if self.rev_FourthYearPercentage == '' or self.rev_FourthYearPercentage is None:
            self.rev_FourthYearPercentage = 0
        
        if self.rev_FifthYearPercentage == '' or self.rev_FifthYearPercentage is None:
            self.rev_FifthYearPercentage = 0
        
        #FOR SAVING EMPTY INPUT IN INTEGER FIELDS
        if self.rev_FirstPriceRise == '' or self.rev_FirstPriceRise is None:
            self.rev_FirstPriceRise = 0

        if self.rev_SecondPriceRise == '' or self.rev_SecondPriceRise is None:
            self.rev_SecondPriceRise = 0
        
        if self.rev_ThirdPriceRise == '' or self.rev_ThirdPriceRise is None:
            self.rev_ThirdPriceRise = 0
        
        if self.rev_FourthPriceRise == '' or self.rev_FourthPriceRise is None:
            self.rev_FourthPriceRise = 0
        
        if self.rev_FifthPriceRise == '' or self.rev_FifthPriceRise is None:
            self.rev_FifthPriceRise = 0
            
        super(R_Changes, self).save(*args, **kwargs)

###############################################################     CO2     ####################################################################

class CO2(models.Model):
    co2_idProject = models.ForeignKey (Project, null=True, blank=True, on_delete=CASCADE)
    co2_idUser = models.ForeignKey (User, null=True, blank=True, on_delete=CASCADE)
    co2_CurrentFactor = models.DecimalField (max_digits=10, decimal_places=3, null=True, blank=True, validators=[DecimalValidator])
    co2_CurrentFactorUnit = models.CharField (max_length=50, null=True, blank=True)
    co2_Diesel = models.DecimalField (max_digits=10, decimal_places=3, null=True, blank=True, validators=[DecimalValidator])
    co2_DieselUnit = models.CharField (max_length=50, null=True, blank=True)
    co2_WoodLogs = models.DecimalField (max_digits=10, decimal_places=3, null=True, blank=True, validators=[DecimalValidator])
    co2_WoodLogsUnit = models.CharField (max_length=50, null=True, blank=True)
    co2_Kerosene = models.DecimalField (max_digits=10, decimal_places=3, null=True, blank=True, validators=[DecimalValidator])
    co2_KeroseneUnit = models.CharField (max_length=50, null=True, blank=True)
    co2_ProductionPerLitre = models.DecimalField (max_digits=10, decimal_places=3, null=True, blank=True, validators=[DecimalValidator])
    co2_ProductionPerLitreUnit = models.CharField (max_length=50, null=True, blank=True)
    co2_EmissionCar = models.DecimalField (max_digits=10, decimal_places=3, null=True, blank=True, validators=[DecimalValidator])
    co2_EmissionCarUnit = models.CharField (max_length=50, null=True, blank=True)
    co2_Notes = models.TextField (null=True, blank=True)
    co2_Source = models.TextField (null=True, blank=True)

    def save(self, *args, **kwargs):

        #FOR SAVING EMPTY INPUT IN DECIMAL FIELDS
        if self.co2_CurrentFactor == '':
            self.co2_CurrentFactor = 0

        if self.co2_Diesel == '':
            self.co2_Diesel = 0
        
        if self.co2_WoodLogs == '':
            self.co2_WoodLogs = 0
        
        if self.co2_Kerosene == '':
            self.co2_Kerosene = 0
        
        if self.co2_ProductionPerLitre == '':
            self.co2_ProductionPerLitre = 0

        if self.co2_EmissionCar == '':
            self.co2_EmissionCar = 0
        
        super(CO2, self).save(*args, **kwargs)