from django.db import models
from django.core.validators import RegexValidator

class ModelField:
    def createAddress ():
        return models.CharField("Address", max_length = 100, default = None)
    
    def createCpf ():
        return models.CharField("CPF",max_length = 11, default = None)
    
    def createDate (label):
        return models.DateField(label, default = None)
    
    def createPhone ():
        phone_regex = RegexValidator(regex=r'\( \d{2} \) \d{4,5} - \d{4}', message="Informe um telefone válido. Exemplos: (99)99999-9999; (99)9999-9999")
        return models.CharField("Phone Number", max_length = 18, default = None, validators = [phone_regex])

