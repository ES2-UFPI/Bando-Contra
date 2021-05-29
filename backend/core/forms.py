from django.forms import ModelForm
from .models import ClientUser

class ClientUserForm(ModelForm):
    def __init__(self):
        super(ClientUserForm, self).__init__()
        self.fields['email'].required = True
    
    class Meta:
        model = ClientUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'cpf', 'address', 'phone', 'bornDate']
