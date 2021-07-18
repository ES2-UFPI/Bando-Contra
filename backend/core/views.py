from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import ClientUser, PartnerUser, Event, Service
from .utils import UserContext, ShortcutsFacade, ClientCreator, PartnerCreator, pairEvent
from .forms import ClientUserForm, PartnerUserForm, EventForm, ServiceForm, ClientFeedbackForm, LimitedServiceForm
from .facade import UserFacade, ShortcutsFacade, ModelFacade, HttpFacade
from datetime import date, timedelta
from django.forms.widgets import HiddenInput
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator

@login_required
def home(request):

    try:
        user = UserFacade.getUser(ClientUser, request.user.username)
        return ShortcutsFacade.callRedirect('detail_client')
    except:
        user = UserFacade.getUser(PartnerUser, request.user.username)
    
    return ShortcutsFacade.callRedirect('detail_partner')
    

def detailClient(request):
    user = UserFacade.getUser(ClientUser, request.user.username)
    context = UserContext(user)
    return context.detailView(request)

@login_required
def detailPartner(request):
    user = UserFacade.getUser(PartnerUser, request.user.username)
    context = UserContext(user)
    assessment = user.assessmentSum/user.assessmentCount if user.assessmentCount > 0  else 0
    return context.detailView(request, assessment)

def temporaryLogin(request):
    #5
    user = User.objects.get(username='partner1')
    login(request, user)
    return ShortcutsFacade.callRender(request, "core/user/client/detail.html")

def testLogin(request, username):
    user = User.objects.get(username=username)
    login(request, user)
    return HttpFacade.response()

def addClient(request):
    creator = ClientCreator()
    return creator.addUser(request, "sign up")

def editClient(request):
    user = UserFacade.getUser(ClientUser, request.user.username)
    context = UserContext(user, ClientUserForm)
    return context.editView(request)

def addPartner(request):
    creator = PartnerCreator()
    return creator.addUser(request, "sign up")

@login_required
def editPartner(request):
    user = UserFacade.getUser(PartnerUser, request.user.username)
    context = UserContext(user, PartnerUserForm)
    return context.editView(request)

@login_required
def detailSchedule(request):
    user = UserFacade.getUser(PartnerUser, request.user.username)
    schedule = Event.objects.filter(partner = user)
    data = {
        "schedule": schedule,
        "today": date.today()
    }
    return ShortcutsFacade.callRender(request, "core/user/partner/schedule.html", data) 

@login_required
def addEvent(request):
    partner = UserFacade.getUser(PartnerUser, username = request.user.username)
    
    if request.method == 'POST':
        form = EventForm(request.POST, partnerUsername = partner.username)
        if form.is_valid():
            event = form.save(commit = False)
            user = UserFacade.getUser(PartnerUser, partner.username)
            event.partner = user
            event.save()
            return ShortcutsFacade.callRedirect("detailSchedule")
    else:
        form = EventForm( partnerUsername = None)
    data = {'title': 'Add Schedule Event', 'form': form}
    return ShortcutsFacade.callRender(request, "core/user/partner/addEvent.html", data)

@login_required
def addService(request):
    client = UserFacade.getUser(ClientUser, username = request.user.username)
    

    listEvents = Event.objects.filter(arrival__gte=date.today())

    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            service = form.save(commit=False)
            user = UserFacade.getUser(ClientUser, request.user.username)
            service.clientUser = user
            service.requestDate = date.today()
            service.deliveryDate = date.today() + timedelta(days=30)
            service.dynamicTax = 0.1 * service.itemValue
            service.totalValue = service.dynamicTax + service.itemValue + service.fixedTax
            service.event = Event.objects.get(id=form.cleaned_data["eventAdd"])
            service.save()
            return ShortcutsFacade.callRedirect("detailService", pk = service.id)
    else:
        form = ServiceForm()
    
    form.fields["eventAdd"].widget = HiddenInput()
    
    data = {'title':'Add Service', 'form': form, 'listEvents': listEvents}
    
    return ShortcutsFacade.callRender(request, "core/user/client/addService.html", data)

@login_required
def editService(request, pk):
    partner = UserFacade.getUser(PartnerUser, username = request.user.username)
    service = ModelFacade.getModel(Service, id = pk)

    if service.event.partner != partner:
        HttpFacade.error404()

    if request.method == 'POST':
        form = LimitedServiceForm(request.POST, instance = service)
        if form.is_valid():
            form.save(commit=True)
            return ShortcutsFacade.callRedirect("detailService", pk = service.id)
    else:
        form = LimitedServiceForm(instance = service)
    data = {'title':'Edit Service', 'form': form}
    return ShortcutsFacade.callRender(request, "core/user/partner/editService.html", data)

@login_required 
def detailService(request, pk):
    service = Service.objects.get(id = pk)

    if service.clientUser.username != request.user.username and service.event.partner.username != request.user.username:
        HttpFacade.error404()

    data = {
        "service": service,
    }
    
    return ShortcutsFacade.callRender(request, "core/user/service.html", data) 

@login_required
def editEvent(request, pk):
    partner = UserFacade.getUser(PartnerUser, username = request.user.username)
    event = ModelFacade.getModel(Event, id = pk)

    if event.partner != partner:
        HttpFacade.error404()

    if request.method == 'POST':
        form = EventForm(request.POST, instance = event, partnerUsername = partner.username)
        if form.is_valid():
            form.save()
            return ShortcutsFacade.callRedirect("detailSchedule")
    else:
        form = EventForm(instance = event,  partnerUsername = None)
    data = {'title': 'Edit Schedule Event', 'form': form}
    return ShortcutsFacade.callRender(request, "core/user/partner/addEvent.html", data)

@login_required
def deleteEvent(request, pk):
    event = ModelFacade.getModel(Event, id=pk)

    currentUser = UserFacade.getUser(PartnerUser, request.user.username)
    if event.partner != currentUser:
        HttpFacade.error404()

    event.delete()

    return HttpFacade.response()

@login_required
def listClientServices(request):
    user = UserFacade.getUser(ClientUser, request.user.username)
    context = UserContext(user)
    return context.listServicesView(request)

@login_required
def listPartnerServices(request):
    user = UserFacade.getUser(PartnerUser, request.user.username)
    context = UserContext(user)
    return context.listServicesView(request)

@login_required
def feedback(request, pk):
    service = ModelFacade.getModel(Service, id = pk)
    user = UserFacade.getUser(ClientUser, request.user.username)

    if service.productStatus != "Order Delivered":
        return ShortcutsFacade.callRedirect('listClientServices')

    if request.method == 'POST':
        form = ClientFeedbackForm(request.POST)
        if form.is_valid():
            service.event.partner.assessmentSum += form.cleaned_data['evaluation']
            service.event.partner.assessmentCount += 1
            service.clientFeedback = form.cleaned_data['feedback']
            service.save()
            return ShortcutsFacade.callRedirect('listClientServices')
    else:
        form = ClientFeedbackForm()
    data = {'title': 'Feedback', 'form': form}
    return ShortcutsFacade.callRender(request, 'core/user/client/feedback.html', data)