from .models import ClientUser, PartnerUser
from .utils import UserContext, UserFacade, ShortcutsFacade
from django.contrib.auth import login
from django.contrib.auth.models import User

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