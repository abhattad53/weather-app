import tkinter as tk
from tkinter import *
from geopy.geocoders import Nominatim
from tkinter import ttk
from tkinter import messagebox
from timezonefinder import TimezoneFinder
from datetime import datetime
from configparser import ConfigParser
import requests
import pytz


def get_weather():
    city = textfield.get()

    geolocator = Nominatim(user_agent="Weather App")
    location = geolocator.geocode(city)
    obj = TimezoneFinder()
    result = obj.timezone_at(lng=location.longitude, lat=location.latitude)

    home = pytz.timezone(result)
    local_time = datetime.now(home)
    current_time = local_time.strftime("%I:%M %p")
    clock.config(text=current_time)
    name.config(text="CURRENT WEATHER")
    api_key = "e0b015a7551a9d659b9a9ad19a7ba566"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response = requests.get(url)

    if response.status_code == 404:
        messagebox.showerror("Error", "City not Found")
        return None

    data = response.json()
    city = data['name']
    # icon_id = data['weather'][0]['icon']
    country = data['sys']['country']
    pressure = data['main']['pressure']
    humidity = data['main']['humidity']
    wind = data['wind']['speed']
    temp = int(data['main']['temp'] - 273.15)
    condition = data['weather'][0]['main']
    description = data['weather'][0]['description']

    # Shift the text in the temperature and condition labels to a bit right
    t.config(text=temp, padx=20)
    c.config(text=(condition, '|', 'FEELS', 'LIKE', temp), padx=20)

    cond = get_suggestions(description)

    suggestions_label.config(text="Some suggestions:\n" + "\n".join(cond))

    w.config(text=temp)
    h.config(text=humidity)
    d.config(text=wind)
    p.config(text=pressure)


def get_suggestions(condition):
    suggestions = {
        'clear sky': ["Enjoy the sunny weather.", "Take a walk or engage in outdoor activities.",
                      "Wear sunglasses and sunscreen."],
        'few clouds': ["Carry an umbrella, just in case.", "\nGo for a hike or a picnic.",
                       "\nWear layers of clothing."],
        'broken clouds': ["Carry an umbrella, just in case.", "Go for a hike or a picnic.", "Wear layers of clothing."],
        'clouds': ["Don't forget sunscreen", "Go for a hike or a picnic.", "Wear layers of clothing."],
        'scattered clouds': ["Carry a light jacket.", "Enjoy outdoor activities.", "Keep an eye on the weather."],
        'overcast clouds': ["Carry a light jacket.", "Plan indoor activities.", "Stay productive indoors."],
        'mist': ["Drive cautiously.", "Carry a light jacket.", "Be mindful of slippery surfaces."],
        'fog': ["Drive with caution and use low beam headlights.", "Allow extra time for commuting.",
                "Be aware of reduced visibility."],
        'light rain': ["Use an umbrella.", "Wear waterproof clothing.", "Stay indoors or find shelter."],
        'moderate rain': ["Use an umbrella.", "Wear waterproof clothing.", "Use waterproof bags."],
        'heavy intensity rain': ["Use an umbrella.", "Wear waterproof clothing.", "Stay indoors or find shelter."],
        'very heavy rain': ["Use an umbrella.", "Wear waterproof clothing.", "Stay indoors or find shelter."],
        'extreme rain': ["Indoor board games for cozy entertainment.", "Enjoy a movie marathon at home.", "Try out new recipes for indoor cooking."],
        'shower rain': ["Use an umbrella.", "Wear waterproof clothing.", "Stay indoors or find shelter."],
        'freezing rain': ["Use an umbrella.", "Wear waterproof clothing.", "Stay indoors or find shelter."],
        'drizzle': ["Carry a compact umbrella.", "Wear a light rain jacket.", "Be cautious of slippery surfaces."],
        'snow': ["Bundle up and wear warm clothing.", "Clear walkways and driveways.",
                 "Be cautious of icy conditions."],
        'thunderstorm': ["Seek shelter indoors.", "Stay away from open areas and tall objects.",
                         "Avoid using electronic devices."],
    }
    return suggestions.get(condition, ["No specific suggestions for this condition."])

    # if condition in suggestions:


## else:
#  return ["No specific suggestions for this condition."]


# suggestions = get_suggestions(weather[3])
# print("\nSuggestions:")
# for i, suggestion in enumerate(suggestions, start=1):
#   print(f"{i}. {suggestion}")

app = Tk()
app.title("Weather App")
app.geometry("900x500+300+200")
app.resizable(False, False)

Search_image = PhotoImage(file="search.png")
myimage = Label(image=Search_image)
myimage.place(x=20, y=20)

textfield = tk.Entry(app, justify="center", width=17, font=("poppins", 25, "bold"), bg="#404040", border=0, fg="white")
textfield.place(x=50, y=40)
textfield.focus()

Search_icon = PhotoImage(file="search_icon.png")
myimage_icon = Button(image=Search_icon, borderwidth=0, cursor="hand2", bg="#404040", command=get_weather)
myimage_icon.place(x=400, y=34)

Logo_image = PhotoImage(file="logo.png")
logo = Label(image=Logo_image)
logo.place(x=280, y=100)

Frame_image = PhotoImage(file="box.png")
frame_myimage = Label(image=Frame_image)
frame_myimage.pack(padx=5, pady=5)
frame_myimage.place(x=50, y=377)

name = Label(app, font=("arial", 10, 'bold'))
name.place(x=30, y=100)
clock = Label(app, font=("Helvetica", 20))
clock.place(x=30, y=130)

suggestions_label = Label(app, font=("arial", 14, 'bold'), wraplength=350, justify=LEFT)
suggestions_label.place(x=550, y=100)


label1 = Label(app, text="TEMPERATURE", font=("Helvetica", 15, 'bold'), fg="white", bg='#1ab5ef')
label1.place(x=120, y=400)

label1 = Label(app, text="HUMIDITY", font=("Helvetica", 15, 'bold'), fg="white", bg='#1ab5ef')
label1.place(x=350, y=400)

label1 = Label(app, text="WIND", font=("Helvetica", 15, 'bold'), fg="white", bg='#1ab5ef')
label1.place(x=520, y=400)

label1 = Label(app, text="PRESSURE", font=("Helvetica", 15, 'bold'), fg="white", bg='#1ab5ef')
label1.place(x=650, y=400)

t = Label(font=("arial", 70, 'bold'), fg="#ee666d")
t.place(x=30, y=250)
c = Label(font=("arial", 15, 'bold'))
c.place(x=30, y=350)

w = Label(text="...", font=("arial", 20, 'bold'), bg="#1ab5ef")
w.place(x=180, y=430)
h = Label(text="...", font=("arial", 20, 'bold'), bg="#1ab5ef")
h.place(x=380, y=430)
d = Label(text="...", font=("arial", 20, 'bold'), bg="#1ab5ef")
d.place(x=525, y=430)
p = Label(text="...", font=("arial", 20, 'bold'), bg="#1ab5ef")
p.place(x=670, y=430)

app.mainloop()
