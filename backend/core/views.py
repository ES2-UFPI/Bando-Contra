from .models import ClientUser, PartnerUser

# Create your views here.
def detailPartner(request):
    user = UserFacade.getUser(PartnerUser, request.user.username)
    content = UserContext(user)
    return context.detailView(request)