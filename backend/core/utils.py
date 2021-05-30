from abc import ABC, abstractmethod
from .forms import ClientUserForm
from .facade import ShortcutsFacade

class UserContext:
    def __init__(self, user):
        self._user = user

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, user):
        self._user = user
    
    def detailView(self, request):
        result = self._user.getTemplatesLocation() + "detail.html"
        data = {'user': self._user}
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