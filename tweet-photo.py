import os, random
import configparser
import tweepy
from datetime import datetime

photo_types = ('.jpg', '.JPG', '.jpeg', '.JPEG')
src = "/home/bms/library.barwap.com/html/"
photo_file = "/home/bms/library.barwap.com/html/photos.txt"
secrets = '/home/bms/barwap-library-scripts/secrets.ini'
followers = " [ @bmsleight @sploshy ] "


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

def tweetPhoto():
    url, purl, filename, year = randomlink()
    now = datetime.now()
    if (now.strftime("%p") == 'AM'):
        greeting = "Morning followers"
    else:
        greeting = "Evening followers"
    status =  greeting + followers + "\n"
    status += "Todays photo is from " + str(year) + "\n"
    status += url + "\n" + purl
    config = configparser.ConfigParser()
    config.read(secrets)
    auth = tweepy.OAuthHandler(config['keys']['consumer_key'],
                               config['keys']['consumer_secret'])
    auth.set_access_token(config['keys']['access_token'], 
                          config['keys']['access_token_secret'])
    api = tweepy.API(auth)
    print(status, filename)
    api.update_with_media(filename, status)

tweetPhoto()

#writePhotoList()
#print(randomlink())

