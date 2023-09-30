from django.contrib import admin
from .models import Simulation,Commodity,Owner,Industry,SocialClass,Stock,Buyer,Seller, Trace

admin.site.register(Simulation)
admin.site.register(Commodity)
admin.site.register(Owner)
admin.site.register(Industry)
admin.site.register(SocialClass)
admin.site.register(Stock)
admin.site.register(Buyer)
admin.site.register(Seller)
admin.site.register(Trace)
