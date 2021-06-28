from django.contrib.auth.models import User
from django.db import models
from .facade import ModelField, UserFacade
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
    arrival = ModelField.createDateField("Arrival Date")
    departure = ModelField.createDateField("Departure Date")
    partner = ModelField.createForeignKey(PartnerUser)
    
    class Meta:
        verbose_name = "Event"
        ordering = ['departure']

class Service(models.Model):
    itemDescription = ModelField.createCharField("Item Description", 300)
    quantity =  ModelField.createIntergerField("Quantity")
    productStatus = ModelField.createCharField("Product Status", 100)
    problemDescription = ModelField.createCharField("Problem Description", 200)
    itemValue = ModelField.createFloatField("Item Value")
    impost = ModelField.createFloatField("Impost")
    dynamicRate = ModelField.createFloatField("Dynamic Rate")
    amount = ModelField.createFloatField("Amount")
    address = ModelField.createCharField("Address", 100)
    requestDate = ModelField.createDateField("Request Date")
    orderPlacementDate = ModelField.createDateField("Order Placement Date")
    deliveryDate = ModelField.createDateField("Delivery Date")
    taxation = ModelField.createBooleanField("Taxation")
    clientUser = ModelField.createForeignKey(ClientUser)
    event = ModelField.createForeignKey(Event)
