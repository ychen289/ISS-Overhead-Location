import requests
from datetime import datetime
import smtplib
import time
from config import YOUR_EMAIL, EMAIL_APP_PASSWORD, RECIPIENT_EMAIL, EMAIL_MESSAGE

MY_LAT = 51.507351  # Your latitude
MY_LONG = -0.127758  # Your longitude


def isNight():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now()
    time_now = time_now.hour

    if time_now >= sunset or time_now <= sunrise:
        return True
    else:
        return False


def isStationOverhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    if (MY_LAT - 5 <= iss_latitude <= MY_LAT + 5) and (
        MY_LONG - 5 <= iss_longitude <= MY_LONG + 5
    ):
        print("The ISS is overhead near you.")
        return True
    else:
        print("The ISS is not overhead.")
        return False


def sendEmail():
    with smtplib.SMTP("smtp.gmail.com") as connection:
        print("Setting up connection ..... ")
        connection.starttls()
        connection.login(user=YOUR_EMAIL, password=EMAIL_APP_PASSWORD)
        print("Sending email .....")
        connection.sendmail(
            from_addr=YOUR_EMAIL,
            to_addrs=RECIPIENT_EMAIL,
            msg=EMAIL_MESSAGE,
        )
        print("ISS Notification sent!")


def spaceStationTracker():
    if isNight() and isStationOverhead():
        sendEmail()

while True:
    time.sleep(60)
    spaceStationTracker()
