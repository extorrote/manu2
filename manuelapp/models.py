from django.db import models
from django.utils import timezone

class Condo(models.Model):
    development_name = models.CharField(max_length=50, null=True, blank=True)
    neighborhood = models.CharField(max_length=50, null=True, blank=True)  
    holiday_season=models.CharField(max_length=50, null=True, blank=True)#DEJAR 1 SOLO PRECIO #PONER HORARIO DE CHECK IN Y CHECKOUT ,
    refundable_damage_deposit=models.CharField(max_length=50, null=True, blank=True)
    night_minimum=models.CharField(max_length=50, null=True, blank=True)   
    primary_view = models.CharField(max_length=50, null=True, blank=True)
    secondary_view = models.CharField(max_length=50, null=True, blank=True)
    bedrooms = models.CharField(max_length=50, null=True, blank=True)
    bathrooms = models.CharField(max_length=50, null=True, blank=True)
    property_type = models.CharField(max_length=200, null=True, blank=True)
    max_people = models.PositiveIntegerField()
    children_under_12=models.CharField(max_length=50, null=True, blank=True)
    pet_friendly = models.CharField(max_length=50, null=True, blank=True)
    imagen1 = models.ImageField(upload_to='manuelapp/images', null=True, blank=True)
    imagen2 = models.ImageField(upload_to='manuelapp/images', null=True, blank=True)
    imagen3 = models.ImageField(upload_to='manuelapp/images', null=True, blank=True)
    imagen4 = models.ImageField(upload_to='manuelapp/images', null=True, blank=True)
    imagen5 = models.ImageField(upload_to='manuelapp/images', null=True, blank=True)
    imagen6 = models.ImageField(upload_to='manuelapp/images', null=True, blank=True)
    imagen7 = models.ImageField(upload_to='manuelapp/images', null=True, blank=True)
    imagen8 = models.ImageField(upload_to='manuelapp/images', null=True, blank=True)
    
    hot_water = models.CharField(max_length=500, null=True, blank=True)
    air_conditioning = models.CharField(max_length=150, null=True, blank=True)
    smoking_allowed=models.CharField(max_length=50, null=True, blank=True)
    on_site_gym=models.CharField(max_length=250, null=True, blank=True)
    swimming_pool=models.CharField(max_length=250, null=True, blank=True)
    appliances = models.CharField(max_length=250, null=True, blank=True)
    security = models.BooleanField(default=False)  # True for 'yes', False for 'no'
    horario_checking=models.CharField(max_length=50,null=True,blank=True)#QUITE LOS PRECIOS AGREGUE HORARIO CHECKING Y CHECKOUT Y DESCRIPCION EXTRA
    horario_checkout=models.CharField(max_length=50,null=True,blank=True)
    extra_description=models.CharField(max_length=1000,null=True,blank=True)
    youtube_iframe = models.TextField(blank=True, default="", null=True)
    google_maps = models.TextField(blank=True, null=True)
 
    def __str__(self):
        return f'{self.development_name or "Condo"} - {self.neighborhood or "No neighborhood"}'
    
    
class Reservation(models.Model):
    condo = models.ForeignKey(Condo, on_delete=models.CASCADE, related_name='reservations')
    start_date = models.DateField()
    end_date = models.DateField()
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    num_guests = models.IntegerField()
    special_requests = models.TextField(blank=True)

    def clean(self):
        # Ensure num_guests does not exceed the condo's max_people
        if self.num_guests > self.condo.max_people:
            raise ValidationError(f"Number of guests ({self.num_guests}) exceeds the maximum allowed ({self.condo.max_people}) for this condo.")

    def save(self, *args, **kwargs):
        self.clean()  # Ensure validation happens before saving
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Reservation for {self.condo} from {self.start_date} to {self.end_date}'
