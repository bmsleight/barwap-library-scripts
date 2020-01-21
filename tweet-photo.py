import os, random
import configparser
import tweepy


photo_types = ('.jpg', '.JPG', '.jpeg', '.JPEG')
src = "/home/bms/library.barwap.com/html/"
photo_file = "/home/bms/library.barwap.com/html/photos.txt"
secrets = 'secrets.ini'

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
    url = "https://library.barwap.com/" +  randomPhoto
    filename = src + randomPhoto
    year = randomPhoto.split("/")[0]
    return (url, filename, year)

def tweetPhoto():
    config = configparser.ConfigParser()
    config.read('secrets.ini')
    auth = tweepy.OAuthHandler(config['keys']['consumer_key'], 
                               config['keys']['consumer_secret'])
    auth.set_access_token(config['keys']['access_token'], 
                          config['keys']['access_token_secret'])
    api = tweepy.API(auth)
    url, filename, year = randomlink()
    status = "Todays photo from " + str(year) + " " + url 
    print(status, filename)
    api.update_with_media(filename, status)

tweetPhoto()

#writePhotoList()
#print(randomlink())

