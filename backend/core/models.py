from django.contrib.auth.models import User
from .utils import ModelField

# Create your models here.
class ClientUser (User):
    fieldCreator = ModelField
    cpf = fieldCreator.createCpf()
    address = fieldCreator.createAddress()
    phone = fieldCreator.createPhone()
    bornDate = fieldCreator.createDate("Born Date")

    def __str__ (self):
        return self.cpf

    class Meta:
        verbose_name = "Client"