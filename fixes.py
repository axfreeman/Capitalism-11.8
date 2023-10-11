# various pieces of code, executed from the shell, mainly to deal with database problems arising from nonswappable model changes

from economy.models import *
from django.contrib.contenttypes.models import ContentType
from django.core.management import call_command


# see https://django-polymorphic.readthedocs.io/en/stable/migrating.html
# def po():
#     new_ct = ContentType.objects.get_for_model(Owner)
#     Owner.objects.filter(polymorphic_ctype__isnull=True).update(
#         polymorphic_ctype=new_ct
#     )
#     return

def set_stock_names():
    for stock in Stock.objects.all():
        stock.name=stock.owner.name.strip()+'-'+stock.commodity.name.strip()+' '+stock.usage_type.strip()
        stock.save()
    #little test

# Doesn't work - use psq script 'dumpdb.ps1'
def dumpdb():
    call_command('dumpdata', 'economy.simulation', '>simulation.json')
    call_command('dumpdata', 'economy.commodity', '>commodity.json')
    call_command('dumpdata', 'economy.owner', '>owner.json')
    call_command('dumpdata', 'economy.industry','>industry.json')
    call_command('dumpdata', 'economy.socialclass','>socialclass.json')
    call_command('dumpdata', 'economy.stock','>stock.json')
    return

def owner_ideefix():
    for owner in Owner.objects.all():
        owner.simulation_number=owner.simulation.id
        owner.save()
    return

def industry_simulation_fix():
    for industry in Industry.objects.all():
        owner=Owner.objects.get(pk=industry.pk)
        simulation_number=owner.simulation_number
        simulation=Simulation.objects.get(pk=simulation_number)
        industry.simulation=simulation
        industry.save()
    for sc in SocialClass.objects.all():
        owner=Owner.objects.get(pk=industry.pk)
        simulation_number=owner.simulation_number
        simulation=Simulation.objects.get(pk=simulation_number)
        sc.simulation=simulation
        sc.save()
def do():
    ind_ct = ContentType.objects.get_for_model(Industry)
    soc_ct = ContentType.objects.get_for_model(SocialClass)
    ind_objects = Owner.objects.filter(
        Q(name="Department I")
            | Q(name="Department II")
            | Q(name="Department IIa")
            | Q(name="Department IIb")
            | Q(name="Department Ia")
            | Q(name="Department Ib")
            | Q(name="Means of Production")
            | Q(name="Consumption")
            | Q(name="Circulating")
            | Q(name="Fixed")
        )
    ind_objects.update(polymorphic_ctype=11)
    soc_objects = Owner.objects.filter(polymorphic_ctype=8)
    for soc in soc_objects:
        print(soc.name)
    soc_objects.update(polymorphic_ctype=12)
    return



def di():
    for socialclass in SocialClass.objects.all():
        simulation = socialclass.simulation
        commodity = Commodity.objects.get(simulation=simulation, name="Labour Power")
        if socialclass.name == "Workers":
            socialclass.commodity = commodity
            socialclass.save()
            print(socialclass.commodity)


def du():
    for stock in Stock.objects.filter(usage_type="Consumption"):
        owner_id = stock.owner_fk.id
        stockclass = SocialClass.objects.get(pk=owner_id)
        print(f"the owner of {stock.id} is {stockclass.name}")
        stock.requirements = stockclass.population
        stock.save()


def da():
    for sim in Simulation.objects.all():
        cs = Commodity(
            name="Capital Services", origin="Social", usage="Production", simulation=sim
        )
        cs.save()
        print(f"Created {cs}")


def de():
    for sim in Simulation.objects.all():
        cap = SocialClass.objects.get(name="Capitalists", simulation=sim)
        com = Commodity.objects.get(simulation=sim, name="Capital Services")
        com.usage = "Useless"
        cap.commodity = com
        print(f"Modifying {cap} using {com}")
        cap.save()
        com.save()


def doa():
    for stock in Stock.objects.filter(usage_type="Consumption"):
        print(f"stock of {stock.commodity.name} has usage type {stock.usage_type}")
        stock.usage_type = "Production"
        stock.save()


def trader():
    sim = Simulation.objects.get(id=1)
    buyers = []
    sellers = []
    for s in Owner.objects.filter(simulation=sim):
        c = s.commodity_stock.all()
        buyers.append(c)
    print(buyers)
    pass


# used once only to convert 'requirement' to 'per unit of output requirement' for industries
def dob():
    for ind in Industry.objects.all():
        for s in ind.stocks.all():
            #            print (ind, s.requirement, s.owner.name,s.owner.output_scale)
            new_requirement = s.requirement / ind.output_scale
            print(f"{s.requirement}  needs {new_requirement}")
            s.requirement = new_requirement
            s.save()


# used once only to convert 'requirement' to 'per unit of population requirement' for social classes
def doc():
    for sc in SocialClass.objects.all():
        print(sc, sc.name, sc.population)
        for s in sc.stocks.all():
            new_requirement = s.requirement / sc.population
            print(f"{s.requirement}  needs {new_requirement}")
            s.requirement = new_requirement
            s.save()

'''
Some fixes

Get-Content .\test.txt | Set-Content -Encoding utf8 test-utf8.txt

foreach ($file in get-ChildItem *.txt) {
    Echo $file.name
    Get-Content $file | Set-Content -Encoding utf8 ("$file.name" +".sql")
 }

 NB

 Set-ExecutionPolicy Unrestricted -Scope CurrentUser

 type .\(file name) to run
'''