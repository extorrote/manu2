from django import forms
from django.core.validators import RegexValidator
class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()    
    phone = forms.CharField(
        max_length=15, 
        validators=[RegexValidator(
            regex=r'^\+?1?\d{9,15}$', 
            message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
        )]
    )
    message = forms.CharField(widget=forms.Textarea)





from django import forms
from .models import Condo, Reservation
from django.core.validators import RegexValidator #ESTO LO IMPORTE PARA TERMINOS Y CONDICIONES OPTION

class CondoForm(forms.ModelForm):
    # Define a list of image fields dynamically
    image_fields = [forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'multiple': False})) for _ in range(1, 9)]
    video = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={'multiple': False}))
    google_maps = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 3}))

   

    class Meta:
        model = Condo
        fields ='__all__'
        
        labels={
            'development_name':' Development Name',
            'neighborhood':'NeigborHood',
            'primary_view':'Primary View', 
            'secondary_view':'Seconday View',
            'bedrooms':'Bedrooms', 
            'bathrooms':'Bathrooms',
            'property_type':'Property Type',
            'hot_water':'Hot Water',
            'air_conditioning':'Air Conditioning',
            'swimming_pool':'Swimming Pool',
            'on_site_gym':'On Site Gym',
            'appliances':'Apliances', 
            'holiday_season':'Holiday Season Price',
            'refundable_damage_deposit':'Refundable Damage Deposit',           
            'imagen1':'image #1',
            'imagen2':'image #2',
            'imagen3':'image #3',
            'imagen4':'image #4',
            'imagen5':'image #5',
            'imagen6':'image #6',
            'imagen7':'image #7',
            'imagen8':'image #8',
            'youtube_iframe': 'Link de YouTube',     
            'security':'Security',
            'max_people':'Max People', 
            'pet_friendly':'Pet Friendly',
            'children_under_12':'Children Under 12',
            'smoking_allowed':'Smoking Allowed',           
            'night_minimum':'Night Minimum',
            'horario_checking':'Checking Time',
            'horario_checkout':'Checkout Time',
            'extra_description':'Extra Description',
        }
        widgets = {
            'price_per_night': forms.NumberInput(attrs={'step': '0.01'}),
            'security': forms.CheckboxInput(),  # For boolean fields
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for i in range(1, 9):
            self.fields['imagen{}'.format(i)].label = f'Image {i}'
        self.fields['google_maps'].label = 'Google Maps  Code'

class ReservationForm(forms.ModelForm):
    accept_terms = forms.BooleanField(
        required=True, 
        label="I readed and  accept the Terms and Conditions",
        error_messages={'required': 'You must accept the terms and conditions to proceed.'}
    )
    
    class Meta:
        model = Reservation
        fields = ['condo', 'start_date', 'end_date', 'name', 'email', 'phone_number', 'num_guests', 'special_requests']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'special_requests': forms.Textarea(attrs={'rows': 3}),
        }