from django.contrib.auth import login
from django.contrib.auth.models import User
from .models import ClientUser, PartnerUser
from .utils import UserContext, ShortcutsFacade, ClientCreator
from .forms import ClientUserForm, PartnerUserForm
from .facade import UserFacade


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

def editPartner(request):
    user = UserFacade.getUser(PartnerUser, request.user.username)
    context = UserContext(user, PartnerUserForm)
    return context.editView(request)