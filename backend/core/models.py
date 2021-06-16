from django.contrib.auth.models import User
from django.db import models
from .facade import ModelField
from .facade import UserFacade
from abc import abstractmethod

@abstractmethod
def getTemplatesLocation(self):
    pass
UserFacade.addMethodToUser('getTemplatesLocation', getTemplatesLocation)

class ClientUser (User):
    cpf = ModelField.createCharField("CPF", 11)
    address = ModelField.createCharField("Address", 100)
    phone = ModelField.createPhoneField()
    bornDate = ModelField.createDateField("Born Date")

    def getTemplatesLocation(self):
        return "core/user/client/"

    def __str__ (self):
        return self.cpf

    class Meta:
        verbose_name = "Client"


class PartnerUser (User):
    nationality = ModelField.createCharField("Nationality", 50)
    # document = ModelField.createFileField()
    validation = ModelField.createBooleanField("Validation")
    assessmentSum = ModelField.createIntergerField("Assessment Sum")
    assessmentCount = ModelField.createIntergerField("Assessment Count")
    observation = ModelField.createCharField("Observation", 5000)
    phone = ModelField.createPhoneField()

    def getTemplatesLocation(self):
        return 'core/user/partner/'
    
    class Meta:
        verbose_name = "Partner"

class Event(models.Model):
    address = ModelField.createCharField("Address", 100)
    arrival =  ModelField.createDateField("Arrival Date")
    departure =  ModelField.createDateField("Departure Date")
    partner = ModelField.createForeignKey(PartnerUser)

    class Meta:
        verbose_name = "Event"