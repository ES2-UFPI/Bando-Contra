from django.forms import ModelForm
from .models import ClientUser

class ClientUserForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ClientUserForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
    
    class Meta:
        model = ClientUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'cpf', 'address', 'phone', 'bornDate']
