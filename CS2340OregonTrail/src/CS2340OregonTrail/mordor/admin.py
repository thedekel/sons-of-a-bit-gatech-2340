from mordor.models import Party, Character, Store, Item, Wagon, Location, Event, Profession
from django.contrib import  admin

admin.site.register(Party)
admin.site.register(Profession)
admin.site.register(Character)
admin.site.register(Store)
admin.site.register(Item)
admin.site.register(Wagon)
admin.site.register(Location)
admin.site.register(Event)