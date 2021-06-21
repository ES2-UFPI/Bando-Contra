from django.forms import ModelForm
from .models import ClientUser, PartnerUser, Event
from .facade import FormFacade

class ClientUserForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ClientUserForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
    
    class Meta:
        model = ClientUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'cpf', 'address', 'phone', 'bornDate']
        widgets = {
            'phone': FormFacade.phoneInput(),
            'bornDate': FormFacade.dateInput(),
        }

        input_formats = {
            'bornDate': ('%Y-%m-%d',)
        }


class PartnerUserForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(PartnerUserForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
    
    class Meta:
        model = PartnerUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'nationality', 'phone']
        widgets = {
            'phone': FormFacade.phoneInput(),
        }

class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = '__all__'