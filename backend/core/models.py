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

    def getServices(self):
        return Service.objects.filter(clientUser=self)

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
    observation = ModelField.createCharField("Observation", 5000, null=True)
    phone = ModelField.createPhoneField()
    
    def getServices(self):
        return Service.objects.filter(event__partner=self)

    def getTemplatesLocation(self):
        return 'core/user/partner/'
    
    class Meta:
        verbose_name = "Partner"

class Event(models.Model):
    address = ModelField.createCharField("Address", 100)
    arrival = ModelField.createDateField("Arrival Date") # Vai chegar lá
    departure = ModelField.createDateField("Departure Date") # Vai sair de lá
    partner = ModelField.createForeignKey(PartnerUser)
    
    class Meta:
        verbose_name = "Event"
        ordering = ['arrival']

class Service(models.Model):
    statusChoices = (
        ("Order placed" , "Order placed"),
        ("order on the way" , "order on the way"),
        ("Order Delivered", "Order Delivered"),
        ("Request under Analysis", "Request under Analysis"),
        ("Taxed order", "Taxed order"),
        ("address not found", "address not found"),
        ("Problems in sending", "Problems in sending")
    )

    itemDescription = ModelField.createCharField("Item Description", 300)
    quantity =  ModelField.createIntergerField("Quantity")
    productStatus = ModelField.createCharField("Product Status", 100, choices=statusChoices)
    problemDescription = ModelField.createTextField("Problem Description")
    itemValue = ModelField.createFloatField("Item Value")
    impost = ModelField.createFloatField("Impost") #fixedTax
    dynamicRate = ModelField.createFloatField("Dynamic Rate") #dynamicTax
    amount = ModelField.createFloatField("Amount") #totalValue
    address = ModelField.createCharField("Address", 100)
    requestDate = ModelField.createDateField("Request Date")
    orderPlacementDate = ModelField.createDateField("Order Placement Date")
    deliveryDate = ModelField.createDateField("Delivery Date") 
    taxation = ModelField.createBooleanField("Taxation")
    clientUser = ModelField.createForeignKey(ClientUser)
    event = ModelField.createForeignKey(Event)
    clientFeedback = ModelField.createTextField("Feedback")
    