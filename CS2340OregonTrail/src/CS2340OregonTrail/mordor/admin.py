from mordor.models import Party, Character, Store, Item, Wagon, Location, Event, Profession, BaseItem
from django.contrib import  admin
"""
@author: Alex Williams, Anthony Taormina, Daniel Whatley, Stephen Roca, Yuval Dekel
"""
admin.site.register(Party)
admin.site.register(Profession)
admin.site.register(Character)
admin.site.register(Store)
admin.site.register(BaseItem)
admin.site.register(Item)
admin.site.register(Wagon)
admin.site.register(Location)
admin.site.register(Event)