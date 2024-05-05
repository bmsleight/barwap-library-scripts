import os, random
import configparser
from datetime import datetime
import http.client
import requests


photo_types = ('.jpg', '.JPG', '.jpeg', '.JPEG')
src = "/home/bms/library.barwap.com/html/"
photo_file = "/home/bms/library.barwap.com/html/photos.txt"
secrets = '/home/bms/barwap-library-scripts/secrets.ini'


def getPhotosList(src=src):
    photos = []
    ignore_list = "thumbnails"
    for root, dirs, files in os.walk(src):
        if "thumbnails" in dirs:
            dirs.remove("thumbnails")
        for file in files:
            if not file.endswith('html') and not file.endswith('webm'):
                fulllocation = os.path.join(root, file)
                photos.append(os.path.relpath(fulllocation, src))
    return photos

def writePhotoList():
    f = open(photo_file,"w") 
    for photo in getPhotosList():
        f.write("https://library.barwap.com/" + photo)
    f.close()

def randomlink():
    photos = getPhotosList()
    randomPhoto = random.choice(photos)
    filename = src + randomPhoto
    year = randomPhoto.split("/")[0]
    month = randomPhoto.split("/")[1]
    url = "https://library.barwap.com/" + year  + "/" + month
    purl = "https://library.barwap.com/" + randomPhoto 
    return (url, purl, filename, year)

def waPhoto():
    url, purl, filename, year = randomlink()
    now = datetime.now()
    if (now.strftime("%p") == 'AM'):
        greeting = "Morning"
    else:
        greeting = "Evening"
    status =  greeting  + ". "
    status += "Todays photo is from " + str(year) + " "
    status += url
    payload =  "{ \"image\": { \"url\": \"" + purl + "\" }, \"caption\": \"" + status + "\"}"
    print(payload)


    config = configparser.ConfigParser()
    config.read(secrets)


    chat_id = config['keys']['chat_id']
    token = config['keys']['token']


    telegram_msg = requests.get(f'https://api.telegram.org/bot{token}/sendPhoto?chat_id={chat_id}&caption={status}&photo={purl}')
    print(telegram_msg)
    print(telegram_msg.content)


waPhoto()



