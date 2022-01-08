from django import forms
from django.forms import ModelForm, fields, widgets
from .models import City, Users, Contact
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ContactForm(ModelForm):
    # name = forms.CharField(widget=forms.Textarea(attrs={'cols': 52, 'rows': 2}))
    # email = forms.EmailField(widget=forms.Textarea(attrs={'cols': 52, 'rows': 2}))
    # subject = forms.CharField(widget=forms.Textarea(attrs={'cols': 111, 'rows': 2}))
    # message = forms.CharField(widget=forms.Textarea(attrs={'cols': 111, 'rows': 5}))
    class Meta:
        model = Contact
        fields = '__all__'
        widgets = {'name': widgets.Textarea(attrs={'cols': 52, 'rows': 2}),
                    'email':widgets.Textarea(attrs={'cols': 52, 'rows': 2}),
                    'subject':widgets.Textarea(attrs={'cols': 111, 'rows': 2}),
                    'message':widgets.Textarea(attrs={'cols': 111, 'rows': 5})
        

        
            }


class UsersForm(ModelForm):
	class Meta:
		model = Users
		fields = '__all__'
		exclude = ['user']

class CityForm(ModelForm):
    class Meta:
        model = City
        fields = 'name',
        widgets = {'name': widgets.TextInput(attrs={'class':'input','placeholder':'City Name'})}

class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']

