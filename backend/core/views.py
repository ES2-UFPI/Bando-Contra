from .models import ClientUser, PartnerUser
from .utils import UserContext
from .utils import ClientCreator
from .facade import UserFacade

def detailClient(request):
    user = UserFacade.getUser(ClientUser, request.user.username)
    context = UserContext(user)
    return context.detailView(request)

def detailPartner(request):
    user = UserFacade.getUser(PartnerUser, request.user.username)
    context = UserContext(user)
    return context.detailView(request)

def addClient(request):
    creator = ClientCreator()
    return creator.addUser(request, "sign in")