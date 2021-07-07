from abc import ABC, abstractmethod
from .forms import ClientUserForm, PartnerUserForm
from .facade import ShortcutsFacade
from .models import Event, Service

def pairEvent(date):
    events = Event.objects.all()

    for event in events:
        if(event.arrival <= date and date <= event.departure):
            return event

class UserContext:
    def __init__(self, user, userForm=None):
        self._user = user
        self._userForm = userForm

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, user):
        self._user = user

    @property
    def userForm(self):
        return self._userForm

    @user.setter
    def userForm(self, userForm):
        self._userForm = userForm
    
    def detailView(self, request, assessment=0):
        result = self._user.getTemplatesLocation() + "detail.html"
        data = {
            'user': self._user,
            'assessment' : assessment,
        }
        return ShortcutsFacade.callRender(request, result, data)

    def editView(self, request):
        if request.method == 'POST':
            form = self._userForm(request.POST, instance=self._user)
            if form.is_valid():
                form.save()
                return ShortcutsFacade.callRedirect("detail_client")
        else:
            form = self._userForm(instance=self._user)

        result = self._user.getTemplatesLocation() + "register.html"
        data = {'form': form, 'title': 'edit profile'}

        return ShortcutsFacade.callRender(request, result, data)

    def listServicesView(self, request):
        result = self._user.getTemplatesLocation() + "listServices.html"
        data = {'services': self._user.getServices()}
        return ShortcutsFacade.callRender(request, result, data)

class UserCreator(ABC):
    @abstractmethod
    def factoryMethod(self, request):
        pass 

    def addUser(self, request, title):
        
        if request.method == "POST":
            user = self.factoryMethod(request)
            if user != None:
                user.save()
                return ShortcutsFacade.callRedirect("detail_client")
            form = ClientUserForm(request.POST)
        else:
            form = self.getForm()
        data = {'title':title, "form":form}
        result = self.getTemplatesLocation() + "register.html"
        return ShortcutsFacade.callRender(request, result, data) 
    
    @abstractmethod
    def getTemplatesLocation(self):
        pass
    
    @abstractmethod
    def getForm(self):
        pass

class ClientCreator(UserCreator):
    
    def factoryMethod(self, request ):
        form = ClientUserForm(request.POST)
        if form.is_valid():
            return form.save(commit = False)

    def getForm(self):
        return ClientUserForm()
    
    def getTemplatesLocation(self):
        return "core/user/client/"

class PartnerCreator(UserCreator):
    
    def factoryMethod(self, request ):
        form = PartnerUserForm(request.POST)
        if form.is_valid():
            return form.save(commit = False)

    def getForm(self):
        return PartnerUserForm()
    
    def getTemplatesLocation(self):
        return "core/user/partner/"