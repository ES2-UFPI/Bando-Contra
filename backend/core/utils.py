from django.db import models
from django.core.validators import RegexValidator
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User

class ModelField:
    def createAddress ():
        return models.CharField("Address", max_length = 100, default = None)
    
    def createCpf ():
        return models.CharField("CPF",max_length = 11, default = None)
    
    def createDate (label):
        return models.DateField(label, default = None)
    
    def createPhone ():
        phone_regex = RegexValidator(regex=r'\(\d{2}\)\d{4,5}-\d{4}', message="Informe um telefone válido. Exemplos: (99)99999-9999; (99)9999-9999")
        return models.CharField("Phone Number", max_length = 18, default = None, validators = [phone_regex])

class ShortcutsFacade:
    @staticmethod
    def callRender(request, template, data={}):
        return render(request, template, data)

class UserFacade:
    @staticmethod
    def addMethodToUser(methodName,method):
        User.add_to_class(methodName, method)

    @staticmethod
    def getUser(userModel, username):
        return get_object_or_404(userModel, username=username)

class UserContext:
    def __init__(self, user):
        self._user = user

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, user):
        self._user = user
    
    def detailView(self, request):
        result = self._user.getTemplatesLocation() + "detail.html"
        data = {'user': self._user}
        return ShortcutsFacade.callRender(request, result, data)