from django.test import TestCase
from .models import Event, PartnerUser, ClientUser
import datetime

#python manage.py test backend.core.tests

class TesteClientUserModel(TestCase):
    
    def setUp(self):
        user = ClientUser.objects.create(cpf="0123456", address="Quadra 61 - Teresina-PI", phone="(99)99999-9999", bornDate="2021-05-30", username="user1")
        user.save()

    def testCreateUser(self):
        searchUser = ClientUser.objects.get(cpf="0123456")
        self.assertEquals(searchUser.username, "user1")
    
    def testVerififyUser(self):
        searchUser = ClientUser.objects.filter(cpf="0123456")
        self.assertEquals(len(list(searchUser)), 1)

class TestEditEventView(TestCase):
    def setUp(self):
        self.partnerUser = PartnerUser(nationality = 'Belga', validation = True, phone = "(86)99959-6969", observation = 'ola mundo!')
        self.partnerUser.save()
        self.event = Event(address = 'rua 10 casa 20', arrival = datetime.date(2021, 3, 17), departure = datetime.date(2021, 2, 17),partner = self.partnerUser)
        self.event.save()

    def testUrl(self):
        pk = self.event.id
        response = self.client.get('/user/partner/edit_event/{}'.format(pk))
        self.assertEqual(response.status_code, 200)
    
    def testCorrectTemplates(self):
        pk = self.event.id
        response = self.client.get('/user/partner/edit_event/{}'.format(pk))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/user/partner/addEvent.html')
    
    def testEditEvent(self):
        pk = self.event.id
        response = self.client.post('/user/partner/edit_event/{}'.format(pk), {'address':'rua 11 casa 21', 'arrival':self.event.arrival, 'departure':self.event.departure})
        editedEvent = Event.objects.get(id = pk)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.event.arrival, editedEvent.arrival)
        self.assertEqual(self.event.departure, editedEvent.departure)
        self.assertNotEqual(self.event.address, editedEvent.address)
        self.assertEqual(editedEvent.address, 'rua 11 casa 21')

class TestDeleteEventView(TestCase):
    def setUp(self):
        self.partnerUser = PartnerUser(nationality = 'Belga', validation = True, phone = "(86)99959-6969", observation = 'ola mundo!')
        self.partnerUser.save()
        self.event = Event(address = 'rua 10 casa 20', arrival = datetime.date(2021, 3, 17), departure = datetime.date(2021, 2, 17),partner = self.partnerUser)
        self.event.save()

    def testUrl(self):
        pk = self.event.id
        response = self.client.get('/user/partner/edit_event/{}'.format(pk))
        self.assertEqual(response.status_code, 200)

    def testCorrectTemplates(self):
        pk = self.event.id
        response = self.client.get('/user/partner/edit_event/{}'.format(pk))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/user/partner/addEvent.html')

    def testDeleteEvent(self):
        pk = self.event.id
        response = self.client.get('/user/partner/delete_event/{}'.format(pk))
        self.assertEqual(response.status_code, 200)
        try:
            Event.objects.get(id=pk)
            self.fail("EVENT STILL EXISTS")
        except:
            pass

    def testNotFound(self):
        response = self.client.get('/user/partner/edit_event/{}'.format(2))
        self.assertEqual(response.status_code, 404)
