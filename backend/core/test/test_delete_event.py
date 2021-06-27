from django.test import TestCase
from ..models import Event, PartnerUser
import datetime

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