from django.contrib.auth import login
from django.contrib.auth.models import User
from .models import ClientUser, PartnerUser, Event, Service
from .utils import UserContext, ShortcutsFacade, ClientCreator, PartnerCreator
from .forms import ClientUserForm, PartnerUserForm, EventForm, ServiceForm
from .facade import UserFacade, ShortcutsFacade, ModelFacade, HttpFacade
from datetime import date

def detailClient(request):
    user = UserFacade.getUser(ClientUser, request.user.username)
    context = UserContext(user)
    return context.detailView(request)

def detailPartner(request):
    user = UserFacade.getUser(PartnerUser, request.user.username)
    context = UserContext(user)
    assessment = user.assessmentSum/user.assessmentCount if user.assessmentCount > 0  else 0
    return context.detailView(request, assessment)

def temporaryLogin(request):
    user = User.objects.get(username='user1')
    login(request, user)
    return ShortcutsFacade.callRender(request, "core/user/client/detail.html")

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

def editPartner(request):
    user = UserFacade.getUser(PartnerUser, request.user.username)
    context = UserContext(user, PartnerUserForm)
    return context.editView(request)

def detailSchedule(request):
    user = UserFacade.getUser(PartnerUser, request.user.username)
    schedule = Event.objects.filter(partner = user)
    data = {
        "schedule": schedule,
        "today": date.today()
    }
    return ShortcutsFacade.callRender(request, "core/user/partner/schedule.html", data) 

def addEvent(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit = False)
            user = UserFacade.getUser(PartnerUser, request.user.username)
            event.partner = user
            event.save()
            return ShortcutsFacade.callRedirect("detailSchedule")
    else:
        form = EventForm()
    data = {'title': 'Add Schedule Event', 'form': form}
    return ShortcutsFacade.callRender(request, "core/user/partner/addEvent.html", data)

def addService(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            service = form.save(commit=False)
            user = UserFacade.getUser(ClientUser, request.user.username)
            service.clientUser = user
            service.save()
            return ShortcutsFacade.callRedirect("detailService")
    else:
        form = ServiceForm()
    data = {'title':'Add Service', 'form': form}
    return ShortcutsFacade.callRender(request, "core/user/client/addService.html", data)
    
def editEvent(request, pk):
    event = ModelFacade.getModel(Event, id = pk)
    if request.method == 'POST':
        form = EventForm(request.POST, instance = event)
        if form.is_valid():
            form.save()
            return ShortcutsFacade.callRedirect("detailSchedule")
    else:
        form = EventForm(instance = event)
    data = {'title': 'Edit Schedule Event', 'form': form}
    return ShortcutsFacade.callRender(request, "core/user/partner/addEvent.html", data)


def deleteEvent(request, pk):
    event = ModelFacade.getModel(Event, id=pk)

    currentUser = UserFacade.getUser(PartnerUser, request.user.username)
    if event.partner != currentUser:
        HttpFacade.error404()

    event.delete()

    return HttpFacade.response()
