import requests
import urllib.request
import json
from django.shortcuts import redirect, render
from .models import City, Users
from .forms import CityForm, ContactForm, CreateUserForm, UsersForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


def contact(request):
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form':form}
    return render(request, 'contact.html', context)

def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        username=request.POST['username']
        print(username)
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            user_obj = User.objects.filter(username=username).first()
            print(user_obj)
            Users(user=user_obj).save()
            messages.success(request, 'Accounts was created for ' + username)
            return redirect('login')
    context = {'form': form}
    return render(request, 'register.html', context)

def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username OR password is incorrect')
            return render(request, 'login.html', {})
    context = {}
    return render(request, 'login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login')

def index(request):
    if request.method == 'POST':
        city = request.POST['city']
        source = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?q='+city+'&units=metric&appid=46d044e8d12d6236c57e74cc884337e2').read()
        list_of_data = json.loads(source)
        data = {
            "country_code": str(list_of_data['sys']['country']),
            "coordinate": str(list_of_data['coord']['lon']) + ',' + str(list_of_data['coord']['lon']),
            "temp": str(list_of_data['main']['temp'])+'° C',
            "pressure": str(list_of_data['main']['pressure']),
            "humidity": str(list_of_data['main']['humidity']),
            'main': str(list_of_data['weather'][0]['main']),
            "description": str(list_of_data['weather'][0]['description']),
            "icon": str(list_of_data['weather'][0]['icon']),
        }
        print(data)
    else:
        data = {}
    
    return render(request, 'index.html', data)


def city(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=46d044e8d12d6236c57e74cc884337e2'
    
    error = ''
    msg = ''
    message = ''

    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            new_city = form.cleaned_data['name']
            existing_city_count = City.objects.filter(name=new_city).count()
            if existing_city_count == 0:
                r = requests.get(url.format(new_city)).json()
                if r['cod'] == 200:
                    form.save()
                else:
                    error = 'City not exist'
            else:
                error = 'City already exists in database'
        
        if error:
            msg = error
            message = 'is-danger'
        else:
            msg = 'City added successfully'
            message = 'is-success'

    form = CityForm()

    cities = City.objects.all()

    weather_data = []

    for c in cities:
        r = requests.get(url.format(c)).json()

        city_weather= {
            'city': c.name,
            'temperature': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon'],
        }

        weather_data.append(city_weather)

    context = {'weather_data': weather_data, 'form':form, 'msg': msg, 'message':message}
    return render(request, 'addcity.html', context)

def delete_city(request, city_name):
    City.objects.get(name=city_name).delete()
    return redirect('city')





def profile(request):
    try:
        task = Users.objects.get(user=request.user)
        form = UsersForm(instance=task)
        if request.method == 'POST':
            form = UsersForm(request.POST, request.FILES, instance=task)
            if form.is_valid():
                form.save()
                return redirect('profile')
    except:
        form = UsersForm()
        

        
       

    return render(request, 'profile.html', {'form':form})

def prof(request):

    fn = Users.objects.get(user=request.user)

    return render(request,'myprofile.html',{'fm':fn})



