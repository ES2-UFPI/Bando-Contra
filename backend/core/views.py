from .models import ClientUser
from .utils import UserContext
from .utils import ShortcutsFacade
from .utils import UserFacade

def detailClient(request):
    user = UserFacade.getUser(ClientUser, request.user.username)
    context = UserContext(user)
    return context.detailView(request)