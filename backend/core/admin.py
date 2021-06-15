from django.contrib import admin
from .models import ClientUser, PartnerUser, Event

# Register your models here.
admin.site.register(ClientUser)
admin.site.register(PartnerUser)
admin.site.register(Event)