from django.db import models
from django.core.validators import RegexValidator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from .storage import OverwriteStorage
from django import forms
from django.http import HttpResponse, Http404
from django.core.validators import MaxValueValidator, MinValueValidator

STORAGE=OverwriteStorage(location="_private/users/documents")

class ModelField:
    
    @staticmethod
    def createDateField (label):
        return models.DateField(label, default = None)
    
    @staticmethod
    def createPhoneField ():
        phone_regex = RegexValidator(regex=r'\(\d{2}\)\d{4,5}-\d{4}', message="Insert a valid phone number. Examples: (99)99999-9999; (99)9999-9999")
        return models.CharField("Phone Number", max_length = 18, default = None, validators = [phone_regex])

    @staticmethod
    def createFileField ():
        return models.FileField("Document", storage=STORAGE)

    @staticmethod
    def createCharField(label, max_length, choices=[], null=False):

        if choices.__len__() == 0:
            return models.CharField(label, max_length = max_length, default = None, null=True)
        else:
            return models.CharField(label, max_length = max_length, choices=choices, null=True)
    
    @staticmethod
    def createIntergerField(label):
        return models.IntegerField(label, default = 0)

    @staticmethod
    def createBooleanField(label):
        return models.BooleanField(label, default = False)

    @staticmethod
    def createForeignKey(model):
        return models.ForeignKey(model, on_delete=models.CASCADE, default=None)
    
    @staticmethod
    def createFloatField(label, default=0):
        return models.FloatField(label, default = default)

    @staticmethod
    def createTextField(label):
        return models.TextField(label, default = None, null = True, blank = True)

class ShortcutsFacade:
    @staticmethod
    def callRender(request, template, data={}):
        return render(request, template, data)

    @staticmethod
    def callRedirect(name, *args, **kwargs):
        return redirect(name, *args, **kwargs)

class ModelFacade:
    @staticmethod
    def getModel(model, *args, **kwargs):
        return get_object_or_404(model, *args, **kwargs)

class UserFacade:
    @staticmethod
    def addMethodToUser(methodName,method):
        User.add_to_class(methodName, method)

    @staticmethod
    def getUser(userModel, username):
        return get_object_or_404(userModel, username=username)

class FormFacade:
    @staticmethod
    def dateInput():
        return forms.DateInput(format = '%Y-%m-%d', attrs = {'type': 'date'})
    
    @staticmethod
    def phoneInput():
        return forms.TextInput(attrs = {'type': 'tel'})
    
    @staticmethod
    def createIntegerField():
        return forms.IntegerField() 

    @staticmethod
    def createIntegerRangeField(max, min):
        return forms.IntegerField(validators=[MaxValueValidator(max), MinValueValidator(min)])

    @staticmethod
    def createChoiceField(choices, required=True):
        return forms.ChoiceField(choices=choices, required=required)

    @staticmethod
    def createTextArea(placeholder, label, required=False):
        return forms.CharField(widget = forms.Textarea(attrs = {"placeholder": placeholder}), label = label, required=required)

class HttpFacade:
    @staticmethod
    def response():
        return HttpResponse()
    @staticmethod
    def error404():
        raise Http404
