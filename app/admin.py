from django.contrib import admin
from .models import City, Users, Contact

admin.site.register(Users)
admin.site.register(City)

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display=('name','email','subject')

