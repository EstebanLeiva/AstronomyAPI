import nasapy
import os
import pandas
from datetime import date, timedelta
import urllib.request
from database import Image, db

key = "3pdvIP08fK1EEb7QJ1HaJliJVaahITfuWeJ36hkF"
nasa = nasapy.Nasa(key = key)


start_date = date(2019, 1, 1)
end_date = date(2020, 1, 1)
delta = timedelta(days=1)

while start_date <= end_date:
    apod = nasa.picture_of_the_day(date=start_date.strftime('%Y-%m-%d'))
    title = apod["title"]
    explanation = apod["explanation"]
    url = apod["url"]
    hdurl = apod["hdurl"]
    image = Image(title=title,explanation=explanation,url=url,hdurl=hdurl)
    db.session.add(image)
    start_date += delta

db.session.commit()


    