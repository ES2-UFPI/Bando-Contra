from django.contrib import admin
from .models import ClientUser, PartnerUser

# Register your models here.
admin.site.register(ClientUser)
admin.site.register(PartnerUser)