# admin.py
from django.contrib import admin
from .models import Condo,Reservation

@admin.action(description='Mark selected condos as featured')
def mark_as_featured(modeladmin, request, queryset):
    queryset.update(is_featured=True)

class CondoAdmin(admin.ModelAdmin):
    list_display = ('development_name', 'neighborhood')
    actions = [mark_as_featured]

admin.site.register(Condo, CondoAdmin)




admin.site.register(Reservation)
