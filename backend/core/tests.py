import datetime
from django.contrib.auth.models import User
from django.test import TestCase
from django.test import Client
from .models import Event, PartnerUser, ClientUser, Service
from .forms import ClientUserForm, PartnerUserForm, EventForm, binarySearch, ServiceForm

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
        self.partnerUser = PartnerUser(nationality = 'Belga', validation = True, phone = "(86)99959-6969", observation = 'ola mundo!', username='partner')
        self.partnerUser.save()
        self.event = Event(address = 'rua 10 casa 20', arrival = datetime.date(2021, 3, 17), departure = datetime.date(2021, 3, 17),partner = self.partnerUser)
        self.event.save()

    def testUrl(self):
        self.client.get('/testLogin/partner')
        pk = self.event.id
        response = self.client.get('/user/partner/edit_event/{}'.format(pk))
        self.assertEqual(response.status_code, 200)
    
    def testCorrectTemplates(self):
        self.client.get('/testLogin/partner')
        pk = self.event.id
        response = self.client.get('/user/partner/edit_event/{}'.format(pk))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/user/partner/addEvent.html')
    
    def testEditEvent(self):
        self.client.get('/testLogin/partner')
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
        self.partnerUser = PartnerUser(nationality = 'Belga', validation = True, phone = "(86)99959-6969", observation = 'ola mundo!', username='partner')
        self.partnerUser.save()
        self.event = Event(address = 'rua 10 casa 20', arrival = datetime.date(2021, 3, 17), departure = datetime.date(2021, 2, 17),partner = self.partnerUser)
        self.event.save()

    def testUrl(self):
        self.client.get('/testLogin/partner')
        pk = self.event.id
        response = self.client.get('/user/partner/edit_event/{}'.format(pk))
        self.assertEqual(response.status_code, 200)

    def testCorrectTemplates(self):
        self.client.get('/testLogin/partner')
        pk = self.event.id
        response = self.client.get('/user/partner/edit_event/{}'.format(pk))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/user/partner/addEvent.html')

    def testDeleteEvent(self):
        self.client.get('/testLogin/partner')
        pk = self.event.id
        response = self.client.get('/user/partner/delete_event/{}'.format(pk))
        self.assertEqual(response.status_code, 200)
        try:
            Event.objects.get(id=pk)
            self.fail("EVENT STILL EXISTS")
        except:
            pass

    def testNotFound(self):
        self.client.get('/testLogin/partner')
        response = self.client.get('/user/partner/edit_event/{}'.format(2))
        self.assertEqual(response.status_code, 404)

class TestListClientServices(TestCase):
    def setUp(self):
        self._partnerUser = PartnerUser(nationality = 'Belga', validation = True, phone = "(86)99959-6969", observation = 'ola mundo!')
        self._partnerUser.save()
        self._event1 = Event(address = 'test1', arrival = datetime.date(2021, 3, 17), departure = datetime.date(2021, 2, 17),partner = self._partnerUser)
        self._event1.save()
        self._event2 = Event(address = 'test2', arrival = datetime.date(2021, 3, 17), departure = datetime.date(2021, 2, 17),partner = self._partnerUser)
        self._event2.save()
        self._user = ClientUser(cpf="0123456", address="Quadra 61 - Teresina-PI", phone="(99)99999-9999", bornDate="2021-05-30", username="user1", password="user1")
        self._user.save()
        self._service1 = Service(itemDescription="test", quantity=1, productStatus="status", problemDescription="test", itemValue=2.5, fixedTax=1, dynamicTax=1, totalValue=1, address="test", requestDate=datetime.date.today(), orderPlacementDate=datetime.date.today(), deliveryDate=datetime.date.today(), taxation=True, clientUser=self._user, event=self._event1)
        self._service2 = Service(itemDescription="test", quantity=1, productStatus="status", problemDescription="test", itemValue=2.5, fixedTax=1, dynamicTax=1, totalValue=1, address="test", requestDate=datetime.date.today(), orderPlacementDate=datetime.date.today(), deliveryDate=datetime.date.today(), taxation=True, clientUser=self._user, event=self._event2)

    def testUrl(self):
        self.client.get('/testLogin/user1')
        response = self.client.get('/user/client/list_services/')
        self.assertEqual(response.status_code, 200)

    def testCorrectTemplates(self):
        self.client.get('/testLogin/user1')
        response = self.client.get('/user/client/list_services/')
        self.assertTemplateUsed(response, 'core/user/client/listServices.html')

    def testNotFound(self):
        response = self.client.get('/user/client/list_services/')
        self.assertEqual(response.status_code, 302)

class TestListPartnerServices(TestCase):
    def setUp(self):
        self._partnerUser = PartnerUser(nationality = 'Belga', validation = True, phone = "(86)99959-6969", observation = 'ola mundo!', username="user2", password="user2")
        self._partnerUser.save()
        self._event1 = Event(address = 'test1', arrival = datetime.date(2021, 3, 17), departure = datetime.date(2021, 2, 17),partner = self._partnerUser)
        self._event1.save()
        self._event2 = Event(address = 'test2', arrival = datetime.date(2021, 3, 17), departure = datetime.date(2021, 2, 17),partner = self._partnerUser)
        self._event2.save()
        self._user = ClientUser(cpf="0123456", address="Quadra 61 - Teresina-PI", phone="(99)99999-9999", bornDate="2021-05-30", username="user1", password="user1")
        self._user.save()
        self._service1 = Service(itemDescription="test", quantity=1, productStatus="status", problemDescription="test", itemValue=2.5, fixedTax=1, dynamicTax=1, totalValue=1, address="test", requestDate=datetime.date.today(), orderPlacementDate=datetime.date.today(), deliveryDate=datetime.date.today(), taxation=True, clientUser=self._user, event=self._event1)
        self._service2 = Service(itemDescription="test", quantity=1, productStatus="status", problemDescription="test", itemValue=2.5, fixedTax=1, dynamicTax=1, totalValue=1, address="test", requestDate=datetime.date.today(), orderPlacementDate=datetime.date.today(), deliveryDate=datetime.date.today(), taxation=True, clientUser=self._user, event=self._event2)

    def testUrl(self):
        self.client.get('/testLogin/user2')
        response = self.client.get('/user/partner/list_services/')
        self.assertEqual(response.status_code, 200)

    def testCorrectTemplates(self):
        self.client.get('/testLogin/user2')
        response = self.client.get('/user/partner/list_services/')
        self.assertTemplateUsed(response, 'core/user/partner/listServices.html')

    def testNotFound(self):
        response = self.client.get('/user/partner/list_services/')
        self.assertEqual(response.status_code, 302)

class TestSearchModule(TestCase):
    def testAverageCase(self):
        array = [1,2,3,4,5]
        value = 3
        self.assertEqual(binarySearch(array, value), 2)

    def testNotFoundCase1(self):
        array = [1,2,4,5,6]
        value = 3
        self.assertEqual(binarySearch(array, value), 2)

    def testNotFoundCase2(self):
        array = [1,2,3,4,5]
        value = 0
        self.assertEqual(binarySearch(array, value), 0)

    def testNotFoundCase3(self):
        array = [1,2,3,4,5]
        value = 6
        self.assertEqual(binarySearch(array, value), 5)

    def testFirstItemCase(self):
        array = [1,2,3,4,5]
        value = 1
        self.assertEqual(binarySearch(array, value), 0)

    def testLastItemCase(self):
        array = [1,2,3,4,5]
        value = 5
        self.assertEqual(binarySearch(array, value), 4)

    def testOneCase(self):
        array = [1]
        value = 1
        self.assertEqual(binarySearch(array, value), 0)

    def testTwoCases(self):
        array = [1,2]
        value = 1
        self.assertEqual(binarySearch(array, value), 0)

class TestEventForm(TestCase):
    def setUp(self):
        self.partnerUser = PartnerUser(nationality = 'Belga', validation = True, phone = "(86)99959-6969", observation = 'ola mundo!')
        self.partnerUser.save()
        self.event = Event(address = 'test', arrival = datetime.date(2021, 7, 11), departure = datetime.date(2021, 7, 18),partner = self.partnerUser)
        self.event.save()
        self.event = Event(address = 'test', arrival = datetime.date(2021, 7, 28), departure = datetime.date(2021, 7, 31),partner = self.partnerUser)
        self.event.save()
    
    def testAddEvent(self):
        form = EventForm({'address': 'test', 'arrival': datetime.date(2021, 8, 1), 'departure': datetime.date(2021, 8, 12)}, partnerUsername = self.partnerUser.username)
        self.assertTrue(form.is_valid())
    
    def testAddEventBetweenEvents(self):
        form = EventForm({'address': 'test', 'arrival': datetime.date(2021, 7, 19), 'departure': datetime.date(2021, 7, 27)}, partnerUsername = self.partnerUser.username)
        self.assertTrue(form.is_valid())

    def testAddFirstEvent(self):
        form = EventForm({'address': 'test', 'arrival': datetime.date(2021, 7, 1), 'departure': datetime.date(2021, 7, 10)}, partnerUsername = self.partnerUser.username)
        self.assertTrue(form.is_valid())

    def testArrivalLaterThanDeparture(self):
        form = EventForm({'address': 'test', 'arrival': datetime.date(2021, 8, 12), 'departure': datetime.date(2021, 8, 1)}, partnerUsername = self.partnerUser.username)
        self.assertFalse(form.is_valid())

    def testInvalidArrival(self):
        form = EventForm({'address': 'test', 'arrival': datetime.date(2021, 7, 17), 'departure': datetime.date(2021, 7, 27)}, partnerUsername = self.partnerUser.username)
        self.assertFalse(form.is_valid())

    def testInvalidDeparture(self):
        form = EventForm({'address': 'test', 'arrival': datetime.date(2021, 7, 19), 'departure': datetime.date(2021, 7, 29)}, partnerUsername = self.partnerUser.username)
        self.assertFalse(form.is_valid())

    def testInvalidArrivalAndDeparture(self):
        form = EventForm({'address': 'test', 'arrival': datetime.date(2021, 7, 17), 'departure': datetime.date(2021, 7, 29)}, partnerUsername = self.partnerUser.username)
        self.assertFalse(form.is_valid())

class TestUserForms(TestCase):

    def testAddClient(self):
        form = ClientUserForm({'username': 'teste', 'cpf': '00000000000', 'address': 'teste', 'phone':'(86)99999-9999', 'bornDate': datetime.date(2021, 8, 1), 'password1': 'senha159951', 'password2': 'senha159951', 'email': 'teste@teste.com', 'first_name': 'teste', 'last_name': 'teste'})
        self.assertTrue(form.is_valid())
        form.save()

    def testAddParter(self):
        form = PartnerUserForm({'username': 'teste', 'nationality': 'teste', 'phone':'(86)99999-9999', 'password1': 'senha159951', 'password2': 'senha159951', 'email': 'teste@teste.com', 'first_name': 'teste', 'last_name': 'teste'})
        self.assertTrue(form.is_valid())
        form.save()

    def testCryptography(self):
        form = ClientUserForm({'username': 'teste1', 'cpf': '00000000000', 'address': 'teste', 'phone':'(86)99999-9999', 'bornDate': datetime.date(2021, 8, 1), 'password1': 'senha159951', 'password2': 'senha159951', 'email': 'teste@teste.com', 'first_name': 'teste', 'last_name': 'teste'})
        form.save()
        user = User.objects.get(username='teste1')
        self.assertNotEqual(user.password, 'senha159951')

        form = PartnerUserForm({'username': 'teste2', 'nationality': 'teste', 'phone':'(86)99999-9999', 'password1': 'senha159951', 'password2': 'senha159951', 'email': 'teste@teste.com', 'first_name': 'teste', 'last_name': 'teste'})
        form.save()
        user = User.objects.get(username='teste2')
        self.assertNotEqual(user.password, 'senha159951')

class TestAuthentication(TestCase):
    def setUp(self):
        form = ClientUserForm({'username': 'user1', 'cpf': '00000000000', 'address': 'teste', 'phone':'(86)99999-9999', 'bornDate': datetime.date(2021, 8, 1), 'password1': 'senha159951', 'password2': 'senha159951', 'email': 'teste@teste.com', 'first_name': 'teste', 'last_name': 'teste'})
        form.save()

    def testLoginUrl(self):
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)

    def testLoginCorrectTemplates(self):
        response = self.client.get('/accounts/login/')
        self.assertTemplateUsed(response, 'registration/login.html')

    def testLogin(self):
        response = self.client.post('/accounts/login/', {'username': 'user1', 'password': 'senha159951'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.wsgi_request.user.username, 'user1')

    def testLoginFail(self):
        response = self.client.post('/accounts/login/', {'username': 'user1', 'password': 'senha159952'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')
        self.assertNotEqual(response.wsgi_request.user.username, 'user1')

    def testLogoutUrl(self):
        self.client.get('/testLogin/user1')
        response = self.client.get('/accounts/logout/')
        self.assertEqual(response.status_code, 302)

    def testLogoutCorrectTemplates(self):
        self.client.get('/testLogin/user1')
        response = self.client.get('/accounts/logout/', follow=True)
        self.assertTemplateUsed(response, 'registration/login.html')

    def testLogout(self):
        self.client.get('/testLogin/user1')
        response = self.client.get('/accounts/logout/')
        if response.wsgi_request.user.id != None:
            self.fail("User is logged in")      

class TestServicesForm():
    
    def setUp(self):
        self.client = ClientUser.objects.create(cpf="0123456", address="Quadra 61 - Teresina-PI", phone="(99)99999-9999", bornDate="2021-05-30", username="user1")
        self.client.save()
        self.partnerUser = PartnerUser(nationality = 'Belga', validation = True, phone = "(86)99959-6969", observation = 'ola mundo!')
        self.partnerUser.save()
        self.event = Event(address = 'rua 10 casa 20', arrival = datetime.date(2021, 3, 17), departure = datetime.date(2021, 3, 17),partner = self.partnerUser)
        self.event.save()
        self.event = Event(address = 'rua 10 casa 20', arrival = datetime.date(2021, 3, 27), departure = datetime.date(2021, 3, 30),partner = self.partnerUser)
        self.event.save()

    def testAddEventServiceForm(self):
        objService = {"itemDescription": "Iphone 12", "quantity": 1, "productStatus": "Tudo certo", "problemDescription": "Sem problemas", "itemValue": 10000, "fixedTax": 1, "dynamicTax": 1, "totalValue": 1, "address":"Quadra 61", "requestDate": datetime.date(2021, 3, 17), "orderPlacementDate": datetime.date(2021, 3, 29), "deliveryDate": datetime.date(2021, 3, 30), "taxation": False, "clientUser": self.client, "event":self.event}
        form = ServiceForm(objService)
        self.assertFalse(form.is_valid())

class TestFeedback(TestCase):
    def setUp(self):
        self._partnerUser = PartnerUser(nationality = 'Belga', validation = True, phone = "(86)99959-6969", observation = 'ola mundo!')
        self._partnerUser.save()
        self._event = Event(address = 'rua 10 casa 20', arrival = datetime.date(2021, 3, 17), departure = datetime.date(2021, 3, 17),partner = self._partnerUser)
        self._event.save()
        self._user = ClientUser(cpf="0123456", address="Quadra 61 - Teresina-PI", phone="(99)99999-9999", bornDate="2021-05-30", username="user1", password="user1")
        self._user.save()
        self._service = Service(itemDescription="test", quantity=1, productStatus="Order Delivered", problemDescription="test", itemValue=2.5, fixedTax=1, dynamicTax=1, totalValue=1, address="test", requestDate=datetime.date.today(), orderPlacementDate=datetime.date.today(), deliveryDate=datetime.date.today(), taxation=True, clientUser=self._user, event=self._event)
        self._service.save()

    def testUrl(self):
        self.client.get('/testLogin/user1')
        pk = self._service.id
        response = self.client.get('/user/client/feedback/{}'.format(pk))
        self.assertEqual(response.status_code, 200)
    
    def testCorrectTemplates(self):
        self.client.get('/testLogin/user1')
        pk = self._service.id
        response = self.client.get('/user/client/feedback/{}'.format(pk))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/user/client/feedback.html')
    
    def testAddFeedback(self):
        self.client.get('/testLogin/user1')
        pk = self._service.id
        response = self.client.post('/user/client/feedback/{}'.format(pk), {'feedback': 'very good!', 'evaluation': '5'})
        editedService = Service.objects.get(id = pk)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(editedService.clientFeedback, 'very good!')

class TestParterInfoPermissions(TestCase):
    def setUp(self):
        partnerUser = PartnerUser(username = 'partner', nationality = 'Belga', validation = True, phone = "(86)99959-6969", observation = 'ola mundo!')
        partnerUser.save()
        user = ClientUser.objects.create(cpf="0123456", address="Quadra 61 - Teresina-PI", phone="(99)99999-9999", bornDate="2021-05-30", username="client")
        user.save()
    
    def testPartnerUserAtDetailPage(self):
        self.client.get('/testLogin/partner')
        response = self.client.get('/user/partner/detail')
        self.assertEqual(response.status_code, 200)

    def testAnonymousUserAtDetailPage(self):
        response = self.client.get('/user/partner/detail', follow = True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/login.html")
    
    def testClientUserAtDetailPage(self):
        self.client.get('/testLogin/client')
        response = self.client.get('/user/partner/detail')
        self.assertEqual(response.status_code, 404)
    
    def testPartnerUserAtEditPage(self):
        self.client.get('/testLogin/partner')
        response = self.client.get('/user/partner/edit_profile')
        self.assertEqual(response.status_code, 200)

    def testAnonymousUserAtEditPage(self):
        response = self.client.get('/user/partner/edit_profile', follow = True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/login.html")
    
    def testClientUserAtEditPage(self):
        self.client.get('/testLogin/client')
        response = self.client.get('/user/partner/edit_profile')
        self.assertEqual(response.status_code, 404)

class TestServicePermissions(TestCase):
    def setUp(self):
        self._partnerUser = PartnerUser(username = 'partner', nationality = 'Belga', validation = True, phone = "(86)99959-6969", observation = 'ola mundo!')
        self._partnerUser.save()

        self._event = Event(address = 'test1', arrival = datetime.date(2021, 3, 17), departure = datetime.date(2021, 2, 17),partner = self._partnerUser)
        self._event.save()

        self._client = ClientUser.objects.create(cpf="0123456", address="Quadra 61 - Teresina-PI", phone="(99)99999-9999", bornDate="2021-05-30", username="client")
        self._client.save()

        self._service = Service(itemDescription="test", quantity=1, productStatus="status", problemDescription="test", itemValue=2.5, fixedTax=1, dynamicTax=1, totalValue=1, address="test", requestDate=datetime.date.today(), orderPlacementDate=datetime.date.today(), deliveryDate=datetime.date.today(), taxation=True, clientUser=self._client, event=self._event)
        self._service.save()
    
    def testPartnerUserAtEditServicePage(self):
        self.client.get('/testLogin/partner')
        response = self.client.get('/user/partner/edit_service/{}'.format(self._service.id))
        self.assertEqual(response.status_code, 200)
    
    def testAnonymousUserAtEditServicePage(self):
        response = self.client.get('/user/partner/edit_service/{}'.format(self._service.id))
        self.assertEqual(response.status_code, 302)
        
    def testClientUserAtEditServicePage(self):
        self.client.get('/testLogin/client')
        response = self.client.get('/user/partner/edit_service/{}'.format(self._service.id))
        self.assertEqual(response.status_code, 404)
    
    def testPartnerUserAtDetailServicePage(self):
        self.client.get('/testLogin/partner')
        response = self.client.get('/user/detail_service/{}'.format(self._service.id))
        self.assertEqual(response.status_code, 200)
    
    def testAnonymousUserAtDetailServicePage(self):
        response = self.client.get('/user/detail_service/{}'.format(self._service.id))
        self.assertEqual(response.status_code, 302)
        
    def testClientUserAtDetailServicePage(self):
        self.client.get('/testLogin/client')
        response = self.client.get('/user/detail_service/{}'.format(self._service.id))
        self.assertEqual(response.status_code, 200)
    
    def testPartnerUserAtListPartnerServicesPage(self):
        self.client.get('/testLogin/partner')
        response = self.client.get('/user/partner/list_services/')
        self.assertEqual(response.status_code, 200)
    
    def testAnonymousUserAtListPartnerServicesePage(self):
        response = self.client.get('/user/partner/list_services/')
        self.assertEqual(response.status_code, 302)
        
    def testClientUserAtListPartnerServicesPage(self):
        self.client.get('/testLogin/client')
        response = self.client.get('/user/partner/list_services/')
        self.assertEqual(response.status_code, 404)
    
    def testPartnerUserAtLisClienttServicesPage(self):
        self.client.get('/testLogin/partner')
        response = self.client.get('/user/client/list_services/')
        self.assertEqual(response.status_code, 404)

class TestEventPermissions(TestCase):
    def setUp(self):
        self._partnerUser = PartnerUser(username = 'partner', nationality = 'Belga', validation = True, phone = "(86)99959-6969", observation = 'ola mundo!')
        self._partnerUser.save()

        self._event = Event(address = 'test1', arrival = datetime.date(2021, 3, 17), departure = datetime.date(2021, 2, 17),partner = self._partnerUser)
        self._event.save()

        self._client = ClientUser.objects.create(cpf="0123456", address="Quadra 61 - Teresina-PI", phone="(99)99999-9999", bornDate="2021-05-30", username="client")
        self._client.save()
    
    def testPartnerUserAtDetailSchedulePage(self):
        self.client.get('/testLogin/partner')
        response = self.client.get('/user/partner/schedule')
        self.assertEqual(response.status_code, 200)
    
    def testAnonymousUserAtDetailSchedulePage(self):
        response = self.client.get('/user/partner/schedule', follow = True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/login.html")

    def testPartnerUserAtAddEventPage(self):
        self.client.get('/testLogin/partner')
        response = self.client.get('/user/partner/add_event')
        self.assertEqual(response.status_code, 200)
    
    def testAnonymousUserAtAddEventPage(self):
        response = self.client.get('/user/partner/add_event', follow = True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/login.html")

    def testPartnerUserAtEditEventPage(self):
        self.client.get('/testLogin/partner')
        response = self.client.get('/user/partner/edit_event/{}'.format(self._event.id))
        self.assertEqual(response.status_code, 200)
    
    def testAnonymousUserAtEditEventPage(self):
        response = self.client.get('/user/partner/edit_event/{}'.format(self._event.id), follow = True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/login.html")

    def testPartnerUserAtDeleteEventPage(self):
        self.client.get('/testLogin/partner')
        response = self.client.get('/user/partner/delete_event/{}'.format(self._event.id))
        self.assertEqual(response.status_code, 200)
    
    def testAnonymousUserAtEDeleteEventPage(self):
        response = self.client.get('/user/partner/delete_event/{}'.format(self._event.id), follow = True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/login.html")

        def testClientUserAtAddEventPage(self):
        self.client.get('/testLogin/client')
        response = self.client.get('/user/partner/add_event')
        self.assertEqual(response.status_code, 404)

    def testClientUserAtEditEventPage(self):
        self.client.get('/testLogin/client')
        response = self.client.get('/user/partner/edit_event/{}'.format(self._event.id))
        self.assertEqual(response.status_code, 404)

    def testClientUserAtDeleteEventPage(self):
        self.client.get('/testLogin/client')
        response = self.client.get('/user/partner/delete_event/{}'.format(self._event.id))
        self.assertEqual(response.status_code, 404)
    

