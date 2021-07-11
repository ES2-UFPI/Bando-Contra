from django.forms import ModelForm
from django.core.exceptions import ValidationError
from .models import ClientUser, PartnerUser, Event, Service
from .facade import FormFacade

def binarySearch(array, value):
    start = 0
    end = len(array)
    
    while start != end:
        middle = start + (end-start)//2
        
        if value == array[middle]:
            return middle
        elif value > array[middle]:
            start = middle + 1
        else:
            end = middle
    
    return end

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
    def __init__(self, *args, **kwargs):
        self.partnerUsername = kwargs.pop('partnerUsername')
        super(EventForm, self).__init__(*args, **kwargs)
        
    class Meta:
        model = Event
        fields = ['address', 'arrival', 'departure']
        widgets = {
            'departure': FormFacade.dateInput(),
            'arrival': FormFacade.dateInput()
        }

        input_formats = {
            'departure': ('%Y-%m-%d',),
            'arrival': ('%Y-%m-%d',)
        }
        
    def clean(self):
        cleanedData = super().clean()
        arrival = cleanedData.get("arrival")
        departure = cleanedData.get("departure")
        if arrival and departure:
            if departure < arrival:
                raise ValidationError("Arrival cannot be later than departure!")

            events = Event.objects.filter(partner__username=self.partnerUsername)
            arrivals = events.values_list('arrival', flat=True)
            departures = events.values_list('departure', flat=True)

            floor = binarySearch(departures, arrival)
            ceeling = binarySearch(arrivals, departure)

            if floor != ceeling:
                raise ValidationError("Already exists a Event in this date")



class ServiceForm(ModelForm):
    class Meta:
        model = Service
        fields = "__all__"
        exclude = ('clientUser', 'event')
        widgets = {
            'requestDate': FormFacade.dateInput(),
            'orderPlacementDate': FormFacade.dateInput(),
            'deliveryDate': FormFacade.dateInput()
        }
        
        input_formats = {
            'requestDate': ('%Y-%m-%d',),
            'orderPlacementDate': ('%Y-%m-%d',),
            'deliveryDate': ('%Y-%m-%d',)
        }
        
