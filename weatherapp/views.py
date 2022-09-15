from django.shortcuts import render, get_object_or_404, redirect
from decouple import config
import requests
from pprint import pprint
from django.contrib import messages
from .models import City

def index(request):
    API_KEY = config("API_KEY")
    city = "Adana"
    u_city = request.POST.get("name") # we're capturing the name="name" from the index.html index element with the get method. Cuz remember, its a dictionary (QueryDict) and the method we need is get()
    
    if u_city:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={u_city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        print(response.ok)

        if response.ok: # response.ok checks if the input value exists in the api database
            content = response.json()
            r_city = content['name']


            if City.objects.filter(name=r_city): # checking if the user input city already exists in my database
                messages.warning(request, "City already exists!")
            else:                                # else, create the city in the db
                City.objects.create(name=r_city)


        else:
            messages.warning(request, "There is no such city")
        

    city_data = []
    cities = City.objects.all()

    for city in cities:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        content = response.json()
        data ={
            "city" : city, # this line is purely to access id. We didn't use content['id'] since we dont want the api data id but rather db item id
            "temp" : content["main"]["temp"],
            "icon" : content["weather"][0]["icon"],
            "desc" : content["weather"][0]["description"]
        }
        city_data.append(data)


    context = {
        'city_data': city_data
    }

    return render(request, 'weatherapp/index.html', context)


def delete_city(request, id):
    city = get_object_or_404(City, id=id) # get_object_or_404 calls a simple get() only difference is that it raises Http404 instead of DoesNotExist
    city.delete()
    messages.warning(request, "City deleted")
    return redirect("home")


# #! content
# {'base': 'stations',
#  'clouds': {'all': 20},
#  'cod': 200,
#  'coord': {'lat': 36.985, 'lon': 35.2881},
#  'dt': 1663167856,
#  'id': 325361,
#  'main': {'feels_like': 304.36,
#           'humidity': 61,
#           'pressure': 1009,
#           'temp': 302.16,
#           'temp_max': 303.44,
#           'temp_min': 302.16},
#  'name': 'Adana Province',
#  'sys': {'country': 'TR',
#          'id': 6946,
#          'sunrise': 1663125601,
#          'sunset': 1663170558,
#          'type': 1},
#  'timezone': 10800,
#  'visibility': 10000,
#  'weather': [{'description': 'few clouds',
#               'icon': '02d',
#               'id': 801,
#               'main': 'Clouds'}],
#  'wind': {'deg': 180, 'speed': 6.17}}