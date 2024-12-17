from customtkinter import*
import requests
import time
from datetime import datetime, timedelta
from PIL import Image

# Initialise the CustomTkinter app
weatherapp = CTk()
weatherapp.title("Weather App")
weatherapp.geometry("700x700")

# getDateNow function
def getDateNow():
    month=int(datetime.now().month)
    day=int(datetime.now().day)
    year=int(datetime.now().year)
    monthName = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    return f"{monthName[month-1]} {day}, {year}"

# openWeather function
def openWeatherData():
    # Define your API key and city name
    api_key = 'your_api_key'
    cityname = dataEntry.get()
    
    # Correct API URL for current weather data
    apilink = f"https://api.openweathermap.org/data/2.5/weather?q={cityname}&appid={api_key}"
    
    # Convert Kelvin to Celsius
    ktoc = 273.15

    try:
        # Make the API call and parse the response JSON
        json = requests.get(apilink).json()

        # Handle errors in the API response
        if json.get("cod") != 200:
            error_message = json.get("message", "Unknown error occurred")
            data1.configure(text="Error")
            data2.configure(text=error_message)
            weatherImageLabel.configure(image=None, text="")
            weatherDescriptionLabel.configure(text="")
            sunriseLabel.configure(text="")
            return
        
        # Extract weather description
        description = json["weather"][0]["description"]

        # Dynamically load the weather image and update the description text
        try:
            weather_img_path = f"weatherimages/{description.replace(' ', '_')}.png"
            weather_image = CTkImage(Image.open(weather_img_path), size=(120, 120))
            weatherImageLabel.configure(image=weather_image)
            weatherImageLabel.image = weather_image  # Keep a reference to avoid garbage collection
            weatherDescriptionLabel.configure(text=f"Weather: {description.capitalize()}")
        except FileNotFoundError:
            weatherImageLabel.configure(image=None, text="Image not found")
            weatherDescriptionLabel.configure(text=f"Weather: {description.capitalize()}")

        # Extract the required data
        apidata = json["weather"][0]["main"]
        temperature = int(json["main"]["temp"] - ktoc)
        feelslike = int(json["main"]["feels_like"] - ktoc)
        lowest = int(json["main"]["temp_min"] - ktoc)
        highest = int(json["main"]["temp_max"] - ktoc)
        pressure = json["main"]["pressure"]
        humidity = json["main"]["humidity"]
        windspeed = json["wind"]["speed"]
        
        # Get the timezone offset from the API
        timezone_offset = json.get("timezone", 0)  # Offset in seconds

        # Convert sunrise timestamp to AM/PM format
        sunrise_timestamp = json["sys"]["sunrise"]
        sunrise_utc_time = datetime.utcfromtimestamp(sunrise_timestamp)

        # Adjust to the city's local timezone
        local_offset = timedelta(seconds=timezone_offset)  # Adjust the offset for your timezone
        sunrise_local_time = sunrise_utc_time + local_offset
        
        # Format sunrise time in AM/PM format
        sunrise_time = sunrise_local_time.strftime("%I:%M %p")

        # Display the sunrise time under the weather image
        sunriseLabel.configure(text=f"Sunrise: {sunrise_time}")

        # Format the weather data
        maindata = f"{apidata}\nTemperature: {temperature}°C"
        additionalinfo = (
            f"Feels Like: {feelslike}°C\n"
            f"Lowest Temperature: {lowest}°C\n"
            f"Highest Temperature: {highest}°C\n"
            f"Pressure: {pressure} hPa\n"
            f"Humidity: {humidity}%\n"
            f"Wind Speed: {windspeed} m/s"
        )

        # Update the labels with the weather data
        data1.configure(text=maindata)
        data2.configure(text=additionalinfo)
       

    except Exception as e:
        # Handle exceptions like network errors
        data1.configure(text="Error")
        data2.configure(text=str(e))
        weatherImageLabel.configure(image=None, text="")
        weatherDescriptionLabel.configure(text="")
        sunriseLabel.configure(text="")


# Create the left (weather) and right (date and images) frames
leftFrame = CTkFrame(master=weatherapp, width=400, height=400)
leftFrame.pack(side="left", expand=True, fill="both", padx=20, pady=20)

rightFrame = CTkFrame(master=weatherapp, width=300, height=300, corner_radius=10)
rightFrame.pack(side="right", fill="both", expand=True, padx=20, pady=20)

# Add widgets to the right frame
dateLabel = CTkLabel(master=rightFrame, text=getDateNow(), font=("times", 20, "bold"))
dateLabel.pack(padx=10, pady=(50, 10)) 

# Separate labels for the weather image and description
weatherImageLabel = CTkLabel(master=rightFrame, text="", font=("times", 16))
weatherImageLabel.pack(pady=10)

weatherDescriptionLabel = CTkLabel(master=rightFrame, text="", font=("times", 20))
weatherDescriptionLabel.pack(pady=5)

sunriseLabel = CTkLabel(master=rightFrame, text="", font=("times", 16))
sunriseLabel.pack(pady=(0, 20))  # Add padding below the sunrise label

# Font type and size
font1 = ("times", 25, "bold")
font2 = ("times", 35, "bold")

# City Entry
dataEntry = CTkEntry(master=leftFrame, justify="center", width=250, height=50, font=font2, placeholder_text="Enter city")
dataEntry.focus()
dataEntry.bind("<Return>", lambda event: openWeatherData())  # Bind Enter key to the function
dataEntry.pack(expand=True, pady=35)

# Add widgets to the left frame
data1 = CTkLabel(master=leftFrame, text="", font=font2)
data1.pack(expand=True, pady=10, padx=20)

data2 = CTkLabel(master=leftFrame, text ="", font=font1)
data2.pack(expand=True, pady=10, padx=20)

# Check button
checkButton = CTkButton(master=leftFrame, text="Weather", font=font1, command=openWeatherData)
checkButton.place(relx=0.5, rely=0.5, anchor="center")
checkButton.pack(expand=True, pady=45, padx=20)

weatherapp.mainloop()
