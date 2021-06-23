from django.contrib.auth import login
from django.contrib.auth.models import User
from .models import ClientUser, PartnerUser, Event
from .utils import UserContext, ShortcutsFacade, ClientCreator, PartnerCreator
from .forms import ClientUserForm, PartnerUserForm, EventForm
from .facade import UserFacade, ShortcutsFacade

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
    user = User.objects.get(username='partner1')
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
    return ShortcutsFacade.callRender(request, "core/user/partner/schedule.html", {"schedule": schedule}) 

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
