from django.db import models
import typing
import copy
from django.db.models import Q
from django.contrib.auth.models import User
# from accounts.models import User
# from capitalism.settings import AUTH_USER_MODEL
# from polymorphic.models import PolymorphicModel

Owner=typing.NewType("Owner",models.Model) # to allow forward reference in class 'Commodity'

class Simulation(models.Model):
    user=models.ForeignKey(User,default=None,null=True,on_delete=models.CASCADE)
    name=models.CharField(max_length=50)
    time_stamp=models.IntegerField(default=0)
    state=models.CharField(max_length=20, default="TEMPLATE") # Either TEMPLATE or ACTIVE
    periods_per_year=models.SmallIntegerField(default=1)
    population_growth_rate = models.FloatField(default=1)
    investment_ratio = models.FloatField(default=1)
    labour_supply_response = models.CharField(max_length=50, default="UNDEFINED")
    price_response_type = models.CharField(max_length=50, default="UNDEFINED")
    melt_response_type = models.CharField(max_length=50, null=True, blank=True,default=None)
    currency_symbol = models.CharField(max_length=2, default="$")
    quantity_symbol = models.CharField(max_length=2, default="#")
    melt=models.FloatField(null=False, blank=False,default=1)    

    class Meta:ordering = ['pk'] 
    def __str__(self):return f'{self.name}({str(self.pk)})'

    #Make a deep clone of myself and all associated objects
    def clone(self,user):
        print(f'The simulation {self.name} of type {self.state} owned by {self.user} is cloning itself at the request of user {user}')
        report(self,1,f'cloning the simulation {self.name}')
# Pick up the children of this simulation before cloning the simulation itself
        new_commodities=Commodity.objects.filter(simulation=self) 
# Now clone the simulation so the new cloned objects can point to it
        self.state='ACTIVE'
        self.user=user
        self.time_stamp=self.time_stamp+1
        self.pk=None
        self.save()
        print(f'created new simulation {self.name} of type {self.state} owned by {self.user}')
# clone the commodities first
        for commodity in new_commodities:
            commodity.pk=None
            commodity.simulation=self
            commodity.save()        
            print(f' Cloned commodity {commodity.name} for user {self.user}. ID is {commodity.pk}')
# Now clone the children recursively
        for commodity in new_commodities:
            new_industries= Industry.objects.filter(commodity=commodity)
            new_social_classes=SocialClass.objects.filter(commodity=commodity)
            for industry in new_industries:
                new_stocks=Stock.objects.filter(owner=industry)
                new_industry=copy.deepcopy(industry)
                new_industry.pk=None
                new_industry.id=None
                new_industry.commodity=commodity 
                new_industry.simulation=self
                new_industry.save()                
                print(f'  Cloned industry {new_industry.name} for user {self.user}. ID is {new_industry.pk}')
                for stock in new_stocks:
                    new_stock=copy.deepcopy(stock)
                    new_stock.pk=None
                    new_stock.id=None
                    new_stock.owner=new_industry
                    # old_stock=Stock.objects.get(name=new_stock.name,time_stamp=????)
#TODO find the commodity
                    new_stock.simulation=self
                    new_stock.save()
                    print(f'   Cloned stock of {new_stock.commodity.name} of type {new_stock.usage_type} for industry {industry.name} with old ID {stock.id} and new ID {new_stock.id}' )
            for social_class in new_social_classes:
                new_stocks=Stock.objects.filter(owner=social_class)
                new_social_class=copy.deepcopy(social_class)
                new_social_class.pk=None
                new_social_class.id=None
                new_social_class.commodity=commodity
                new_social_class.simulation=self
                new_social_class.save()                
                print(f'  Cloned social class {new_social_class.name} for user {self.user}. ID is {new_social_class.id}')
                for stock in new_stocks:
                   new_stock=copy.deepcopy(stock)
                   new_stock.pk=None
                   new_stock.id=None
                   new_stock.owner=new_social_class
#TODO find the commodity
                   new_stock.simulation=self
                   new_stock.save()
                   print(f'   Cloned stock of {new_stock.commodity.name} of type {new_stock.usage_type} for social class {social_class.name} with old ID {stock.id} and new ID {new_stock.id}')

        return
    
class Commodity(models.Model):
    name = models.CharField(max_length=255, default="UNDEFINED")
    simulation = models.ForeignKey(Simulation, related_name='commodities', default=None,on_delete=models.CASCADE)
    origin = models.CharField(max_length=255,default="UNDEFINED")
    usage = models.CharField(max_length=255, default="UNDEFINED")
    size = models.FloatField(default=0)
    total_value = models.FloatField(default=0)
    total_price = models.FloatField(default=0)
    unit_value = models.FloatField(default=1)
    unit_price = models.FloatField(default=1)
    turnover_time = models.FloatField(default=360)
    demand = models.FloatField(default=0)
    supply = models.FloatField(default=0)
    allocation_ratio = models.FloatField(default=1)
    display_order = models.IntegerField(null=True, default=1)
    image_name = models.CharField(max_length=255, default="UNDEFINED")
    tooltip = models.CharField(max_length=255, default="UNDEFINED")
    monetarily_effective_demand=models.FloatField(default=0)
    investment_proportion=models.FloatField(default=0)

    class Meta:
        verbose_name_plural = 'Commodities'   
        ordering = ['simulation','pk',] 

    def __str__(self):return f'{self.name}({str(self.pk)})'
    @property
    def link(self): return f'<a href = "/commodities/{self.id}">{self.name}</a>'

    def constrain_demand(self):
        report(self.simulation,2,f'Demand for {self.name} is {self.demand} and supply is {self.supply}')
        if self.supply==0:
            report(self.simulation,1,f"Zero Supply of {self.link}")
            self.alllocation_ratio=0
        else:
            self.allocation_ratio=self.demand/self.supply
        #we could do without allocation_ratio altogether but for the user to see what is going on, it is useful
        self.demand=self.demand*self.allocation_ratio
        self.save()
        report(self.simulation,2,f'Demand for {self.link} has been constrained by supply to {self.demand}')

class Owner(models.Model):
    name = models.CharField(max_length=255,default="UNDEFINED")
    # simulation = models.ForeignKey(Simulation, related_name='owners', on_delete=models.CASCADE)
    # simulation_number=models.IntegerField(default=1)
    commodity = models.ForeignKey(Commodity, null=True, related_name='producers',on_delete=models.CASCADE, default=None) # Many industries per commodity

    class Meta:
        ordering = ['pk'] 

    def __str__(self):return f'{self.name}({str(self.id)})'
    @property
    def link(self): return f'<a href = "/owners/{self.id}">{self.name}</a>'
    @property
    def sales_stock(self):return self.stocks.get(usage_type="Sales")
    @property
    def money_stock(self):
        # print(f'{self.name} is looking for his money stock')
        # candidates=Stock.objects.filter(owner=self,usage_type="Money")
        # print(f'candidates are {candidates}')
        return Stock.objects.get(owner=self,usage_type="Money")
    def productive_stocks(self):return self.stocks.filter(usage_type="Production")
    def consuming_stocks(self): return self.stocks.filter(usage_type="Consumption")
    #TODO this should be consumption only but test first

class Industry(Owner):
    simulation = models.ForeignKey(Simulation, related_name='industries', default=1, on_delete=models.CASCADE)
    output_scale = models.IntegerField(null=True,default=1)
    output_growth_rate = models.IntegerField(null=True,default=1)
    initial_capital=models.FloatField(null=True,default=0)
    work_in_progress=models.FloatField(null=True,default=0)
    current_capital=models.FloatField(null=True,default=0)
    profit=models.FloatField(null=True,default=0)
    profit_rate=models.FloatField(default=0)

    class Meta:
        verbose_name_plural = 'Industries'
        ordering = ['pk',] 

    def __str__(self):return f'[Ind {str(self.pk)} from Sim {str(self.simulation.pk)}]'
    @property
    def link(self): return f'<a href = "/industries/{self.id}">{self.name}</a>'

    def set_demand(self):# set the demand for all stocks to restore productive or reproductive capacity to the required level
        report(self.simulation,2,f'Set demand for industry {self.link}')
        for ss in self.consuming_stocks():
            sc=ss.commodity
            so=ss.owner
            sr=self.output_scale*self.commodity.turnover_time*ss.requirement/self.simulation.periods_per_year 
            ss.demand=sr #TODO -ss.size
            ss.save()
            report(self.simulation,3,f'Demand for {ss.link} of {sc.link} owned by {so.link} has been increased by {sr} to {ss.demand}')

    def produce(self):
        sim=self.simulation
        report(sim,2,f'{self.link} is producing')
        ss=self.sales_stock
        ssc=ss.commodity
        report (sim,3,f'{ss.link} of {ssc.link} before production is {ss.size} with value {ss.value}')
        for s in self.productive_stocks():
            stock_c=s.commodity
            report (sim,4,f'processing productive stock of {stock_c.link} with size {s.size} and value {s.value}' )
            # Use up the stock required to produce
            if s.commodity.name=="Labour Power":
                used_up_value=s.size #TODO modify this if production is constrained by allowable output scale
                s.size-=used_up_value
                report(sim,4,f'Labour Power adds it size {used_up_value}')
            else:
                used_up_value=s.value
                s.value-=used_up_value
                s.size-=used_up_value/ssc.unit_value
                report(sim,4,f'{stock_c.link} transfers its value {used_up_value} and its size becomes {s.size}')
            s.save()
            ss.value+=used_up_value
            ss.size=self.output_scale
            report (sim,3,f'Sales value becomes {ss.value}')
        report(sim,3,f'Sales value is being set to {ss.value}')
        ss.save()


class SocialClass(Owner):
    simulation = models.ForeignKey(Simulation, related_name='socialclasses', default=1, on_delete=models.CASCADE)
    population = models.IntegerField(null=True,default=1000)
    participation_ratio = models.FloatField(null=True,default=1)
    consumption_ratio = models.FloatField(null=True,default=1)
    revenue = models.FloatField(null=True,default=0)
    assets = models.FloatField(null=True,default=0)

    class Meta:
        verbose_name_plural = 'Social Classes'   
        ordering = ['pk',] 

    def __str__(self): return f'{str(self.pk)}: {self.name} [Simulation {self.simulation.pk}: {self.simulation.name}]'
    @property
    def link(self): return f'<a href = "/social_classes/{self.id}">{self.name}</a>'

    def set_demand(self):# set the demand for all stocks to restore productive or reproductive capacity to the required level
        report(self.simulation,2,f"Set demand and supply for class {self.link}")
        for ss in self.consuming_stocks():
            sr=self.population*self.consumption_ratio*ss.requirement/self.simulation.periods_per_year
            sc=ss.commodity 
            so=ss.owner
            ss.demand=sr #TODO -ss.size
            ss.save()
            report(self.simulation,3,
                f'Demand for {ss.link}({ss.id}) of {sc.link}({sc.id}) owned by {so.link} has been increased by {sr} to {ss.demand}')

    def reproduce(self):
        sim=self.simulation.id
        ss=self.sales_stock
        ssc=ss.commodity
        report(sim,2,f'Social Class {self.link} producing {ssc.link} is reproducing')
        report (sim,2,f'Sales stock size of {ssc.link} before production is {ss.size} with value {ss.value}')
        # Just consume. There is no value transfer because reproduction is external to production
        for s in self.consuming_stocks():
            stock_c=s.commodity
            report(sim,3,f'Consuming stock of {stock_c.link} whose size is {s.size}')
            s.size=0 #eat everything available
            s.save()
        if ss.usage_type=="Production":
             report(sim,3,f'Replenishing Labour Power to {self.population}')
             ss.size=self.population*ss.requirement
             report(sim,3,f'Supply of Labour Power has reached {ss.size}')
        ss.save()

class Stock(models.Model):
    name=models.CharField(max_length=200,null=False,default="UNDEFINED")
    simulation = models.ForeignKey(Simulation, on_delete=models.CASCADE)
    commodity = models.ForeignKey(Commodity,related_name="commodity_stock",on_delete=models.CASCADE)
    usage_type  =models.CharField(max_length=255,null=True, default="UNDEFINED")  #! sales, productive, consumption, money
    owner=models.ForeignKey(Owner,related_name='stocks',on_delete=models.CASCADE)
    size = models.FloatField( null= True,default=0)
    requirement = models.FloatField( default=0) # flow per unit of output
    value = models.FloatField( default=0)
    price = models.FloatField( default=0)
    demand=models.FloatField( default=0)
    monetary_demand=models.FloatField(default=0) #! Convenience field - should normally be simply set to demand * commodity.unit_price   
 
    class Meta:ordering = ['simulation','usage_type','pk'] 
    def __str__(self):return f'{str(self.pk)}: [Simulation {self.simulation.pk}: {self.simulation.name}]'
    @property
    def link(self): return f'<a href = "/stocks/{self.id}">{self.usage_type} stock {self.pk}</a>'

    def owner_money_stock(self):
        owner=self.owner
        return owner.money_stock
    
class Buyer(models.Model):
    simulation=models.ForeignKey(Simulation,on_delete=models.CASCADE, related_name='BuyerSimulation',null=True)
    purchaseStock=models.ForeignKey(Stock, on_delete=models.CASCADE, related_name='BuyerStock',null=False)
    moneyStock=models.ForeignKey(Stock, on_delete=models.CASCADE,related_name='BuyerMoneyStock', null=False)
    @property
    def link(self): return f'<a href = "/buyers/{self.id}">{self.name}</a>'
    def owner(self): return self.purchaseStock.owner

class Seller(models.Model):
    simulation=models.ForeignKey(Simulation,on_delete=models.CASCADE, related_name='SellerSimulation',null=True)
    salesStock=models.ForeignKey(Stock,on_delete=models.CASCADE,related_name='SellerStock',null=False)
    moneyStock=models.ForeignKey(Stock, on_delete=models.CASCADE,related_name='SellerMoneyStock', null=False)
    @property
    def link(self): return f'<a href = "/sellers/{self.id}">{self.name}</a>'
    def owner(self): return self.salesStock.owner

class Trace(models.Model):
    simulation=models.ForeignKey(Simulation,null=True, default=None,on_delete=models.CASCADE)
    project_id = models.IntegerField(default=0, null=False)
    level = models.IntegerField(default=0, null=False)
    message = models.CharField(max_length=250, null=False)

def report(simulation, level, message): 
    entry = Trace(
        simulation=simulation, 
        level=level, 
        message=message
        )
    entry.save()
