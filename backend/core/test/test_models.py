from django.test import TestCase
from ..models import ClientUser

#python manage.py test backend.core.test.tests_models

class TesteSimpleCaseModels(TestCase):
    
    def setUp(self):
        user = ClientUser.objects.create(cpf="0123456", address="Quadra 61 - Teresina-PI", phone="(99)99999-9999", bornDate="2021-05-30", username="user1")
        user.save()

    def testCreateUserOk(self):
        searchUser = ClientUser.objects.get(cpf="0123456")
        self.assertEquals(searchUser.username, "user1")
    
    def testVerificarUser(self):
        searchUser = ClientUser.objects.filter(cpf="0123456")
        self.assertEquals(len(list(searchUser)), 1)