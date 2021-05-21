from django.contrib.auth.models import User
from .utils import ModelField
from .utils import UserFacade
from abc import abstractmethod

@abstractmethod
def getTemplatesLocation(self):
    pass
UserFacade.addMethodToUser('getTemplatesLocation', getTemplatesLocation)

class ClientUser (User):
    fieldCreator = ModelField
    cpf = fieldCreator.createCpf()
    address = fieldCreator.createAddress()
    phone = fieldCreator.createPhone()
    bornDate = fieldCreator.createDate("Born Date")

    def getTemplatesLocation(self):
        return "core/user/client/"

    def __str__ (self):
        return self.cpf

    class Meta:
        verbose_name = "Client"