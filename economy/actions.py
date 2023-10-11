from .models import *
from django.shortcuts import render, redirect
from django.core.management import call_command
from django.shortcuts import render, redirect
from django.core.management import call_command
from .tests import totalMoney


def create_simulation_from_project(user,simulation_id):
    this_simulation=Simulation.objects.get(state='TEMPLATE',pk=simulation_id)# there must only always be one of these
    print(f'Creating simulation from template with id {this_simulation.id} for user {user}')
    this_simulation.clone(user)
    return

def restart_trace(request):
    simulation=Simulation.objects.get(user=request.user)
    report(simulation,1,"DELETING ALL TRACE REPORTS")
    Trace.objects.all().delete()
    return redirect("/economy")

def admin_reset(request):
    #COMPLETE RESET - SHOULD ONLY BE AVAILABLE TO ADMINS
    print("WIPING OUT ALL DATA AND REINITIALIZING")
    Trace.objects.all().delete()
    Industry.objects.all().delete()
    SocialClass.objects.all().delete()
    Commodity.objects.all().delete()
    Owner.objects.all().delete()
    Stock.objects.all().delete()
    Simulation.objects.all().delete() #TODO this should cascade all others - doesn't seem to happen that way
    call_command('loaddata', 'fixtures/simulation.json')
    call_command('loaddata', 'fixtures/commodity.json')
    call_command('loaddata', 'fixtures/owner.json')
    call_command('loaddata', 'fixtures/industry.json')
    call_command('loaddata', 'fixtures/socialclass.json')
    call_command('loaddata', 'fixtures/stock.json')
    return redirect("/economy")

#Once for all initialisation for new user
def setup(request):
    simulation=Simulation.objects.get(user=request.user)
    report(simulation,1,"SETUP")
    initialise_demand_and_supply(simulation)    
    # Create the buyer and seller list once for all
    report(simulation,2,"Creating a list of buyers and sellers")
    Seller.objects.all().delete()
    for s in Stock.objects.filter(simulation=simulation,usage_type="Sales"):
        o=s.owner
        c=s.commodity
        m=s.owner_money_stock()
        report(simulation,3,f'Adding seller {s.link} together with {m.link} owned by {o.link} selling {c.link}')
        seller=Seller(simulation=s.simulation,salesStock=s,moneyStock=m)
        seller.save()


    Buyer.objects.all().delete()
    for s in Stock.objects.filter(Q(usage_type="Production") | Q(usage_type="Consumption"),simulation__pk=1):
        m=s.owner_money_stock()
        o=s.owner
        c=s.commodity
        report(simulation,3,f' Adding buyer {s.link} together with {m.link} owned by {o.link} buying {c.link}')
        buyer=Buyer(simulation=s.simulation,purchaseStock=s,moneyStock=m)
        buyer.save()
    # initialise the commodities from the stocks
    set_commodities_from_stocks(simulation)
    return redirect("/economy")

def initialise_demand_and_supply(simulation):
    for c in Commodity.objects.filter(simulation=simulation):c.demand=c.supply=c.allocation_ratio=0;c.save()
    for s in Stock.objects.filter(simulation=simulation):
        s.demand=s.supply=0
        s.save()

def set_demand_and_supply(request):
    # step 1: tell all industries to register their needs in their productive stocks
    simulation=Simulation.objects.get(user=request.user)
    report(simulation,1,"CALCULATING DEMAND AND SUPPLY FOR INDUSTRIES")
    initialise_demand_and_supply(simulation)
    for industry in Industry.objects.filter(simulation=simulation):
        industry.set_demand()
        oc=industry.commodity # commodity that this owner supplies
        ns=industry.sales_stock.size 
        report(simulation,2,f'{industry.link} has added {ns:.0f} to the supply {oc.supply:.0f} of {oc.link}')  
        oc.supply+=ns
        oc.save()

    # step 1: tell all social classes to  register their needs in their productive stocks
    report(simulation,1,"CALCULATING DEMAND AND SUPPLY FOR SOCIAL CLASSES")
    for sc in SocialClass.objects.filter(simulation=simulation):
        sc.set_demand()
        oc=sc.commodity # commodity that this owner supplies
        ns=sc.sales_stock.size 
        report(simulation,2,f'Add {ns} to supply {oc.supply} of  {oc.link} from {sc.link}')  
        oc.supply+=ns
        oc.save()

    # step 3: for each commodity, add up the total demand by asking all its stocks what they need
    report(simulation,1,"ADDING UP DEMAND FROM INDUSTRIES")
    for c in Commodity.objects.filter(simulation=simulation):
        report(simulation,1,f'Calculating total demand for {c.link}')
        d=0
        for s in c.commodity_stock.all():
            so=s.owner
            report(simulation,2,f'Demand for {c.link} from {s.link} of type {s.usage_type} with owner {so.link} is {s.demand}')
            d+=s.demand
        report (simulation,1,f'Total demand for {c.link} is {d}')
        c.demand=d
        c.save()
    # step 4: constrain demand
    report(simulation,1,'CONSTRAINING DEMAND')
    for c in Commodity.objects.filter(simulation=simulation):
        if (c.usage=="PRODUCTIVE".strip()) or (c.usage=="CONSUMPTION".strip()):
            c.constrain_demand()
    set_commodities_from_stocks(simulation)
    return redirect("/economy")

def trade(request):
    simulation=Simulation.objects.get(user=request.user)
    for seller in Seller.objects.filter(simulation=simulation):
        ss=seller.salesStock
        c=ss.commodity
        report(simulation,1,f'seller {ss.link} is looking for buyers of {c.link} and can sell {ss.size}')
        for buyer in Buyer.objects.filter(simulation=1,purchaseStock__commodity=c):
            bp=buyer.purchaseStock
            report(simulation,2,f'buyer {bp.link} is buying {bp.demand} ')
            buy(buyer,seller)
    set_commodities_from_stocks(simulation)
    return redirect("/economy")
    
def buy(buyer,seller):
    bo=buyer.owner()
    so=seller.owner()
    bp=buyer.purchaseStock
    commodity=seller.salesStock.commodity
    unitPrice=commodity.unit_price
    unitValue=commodity.unit_value
    amount=bp.demand
    report(buyer.simulation.pk,3,f'{bo.link} will buy {amount} from {so.link} at price {unitPrice} and value {unitValue}')
    buyer.purchaseStock.size+=amount
    buyer.purchaseStock.demand-=amount
    seller.salesStock.size=0
    if  buyer.moneyStock.id==seller.moneyStock.id:
        #This workaround seems to be necessary because of the behaviour of the db interface
        report (1,4,"Money stocks are the same so no transfer effected")
    else:
        seller.moneyStock.size+=amount*unitPrice
        buyer.moneyStock.size-=amount*unitPrice
    # we do not modify the value or price attributes of either stock here, because we recalculate prices and values as a distinct operation, immediately after this step
    buyer.purchaseStock.save()
    seller.salesStock.save()
    buyer.moneyStock.save()
    seller.moneyStock.save()
    report(buyer.simulation.id,1,f"TOTAL MONEY IS NOW {totalMoney(1)}")


def set_commodities_from_stocks(simulation):
    report(simulation,1,"RECALCULATING COMMODITY VALUES, PRICES AND DEMAND, FROM STOCKS")
    for c in Commodity.objects.filter(simulation__id=1):
        uv=c.unit_price
        up=c.unit_value
        c.size=0
        c.total_value=0
        c.total_price=0
        c.demand=0
        report(simulation,2,f'Evaluating all stocks of {c.link} with unit value {uv} and unit price {up}')
        for s in Stock.objects.filter(commodity=c,simulation=c.simulation):
            report(simulation,3,f'{c.link} starts with size {c.size}, value {c.total_value} and price {c.total_price}')
            s.value=s.size*uv
            s.price=s.size*up
            report(simulation,4,f'{s.link} of usage type {s.usage_type} with owner {s.owner.link} adds {s.size} with value {s.value} and price {s.price}')
            s.save()
            c.size+=s.size
            c.total_value+=s.value
            c.total_price+=s.price
            c.demand+=s.demand
            report(simulation,4,
                f'This brings {c.link} to size {c.size}, value {c.total_value}, price {c.total_price} and demand {c.demand}')
        c.save()
        report(simulation,2,
            f'{c.link} now has size {c.size}, value {c.total_value} and price {c.total_price}. Demand is {c.demand} and supply{c.supply}')

def produce(request):
    simulation=Simulation.objects.get(user=request.user)
    report(simulation,1,'PRODUCTION')
    for ind in Industry.objects.filter(simulation__id=1):
        ind.produce()
    for soc in SocialClass.objects.filter(simulation__id=1):
        soc.reproduce()
    return redirect("/economy")


