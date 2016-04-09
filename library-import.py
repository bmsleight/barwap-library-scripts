landing_location = '/tmp/landing/'
final_location = '/tmp/final/'

photo_types = ('.jpg', '.JPG', '.png', '.PNG', '.jpeg', '.JPEG')
video_types = ('.mp4', '.avi', '.3gp')



########################
import os, datetime, sys
import exifread

photos_in_landing_location = []
videos_in_landing_location = []
flag_new_files = False

def move(date_taken, filename):
    moved = False
    year = date_taken.strftime("%Y")
    month = date_taken.strftime("%b").lower()
    day = date_taken.strftime("%d") + "-" 

    final_location_full = final_location + year + "/" + month
    final_filename = final_location_full + "/" + day + os.path.basename(filename)

    try: 
        skip = os.path.isfile(final_filename) 
        if skip:
            print "Removing duplicate: ", filename
            os.remove(filename)
        if not skip:
            try:
                os.makedirs(final_location_full)
            except:
                pass
            print "Moving ", filename, " to ", final_filename
            os.rename(filename, final_filename)
            moved = True
            try:
                os.removedirs(os.path.dirname(filename))
            except:
                pass
    except OSError:
        print "[MOVE] Error for: ", filename
    return moved


for dirpath, dirnames, filenames in os.walk(landing_location):
    for filename in filenames:
        if filename.endswith(photo_types):
            photos_in_landing_location.append(os.path.join(dirpath, filename))
        if filename.endswith(video_types):
            videos_in_landing_location.append(os.path.join(dirpath, filename))

for filename in photos_in_landing_location:
    with open(filename, 'rb') as fh:
        tags = exifread.process_file(fh, stop_tag="EXIF DateTimeOriginal")
        try:
            exif = str(tags["EXIF DateTimeOriginal"]) # 2015:02:25 18:08:07
            date_taken = datetime.datetime.strptime(exif, "%Y:%m:%d %H:%M:%S")
            if(move(date_taken, filename)):
                flag_new_files = True
        except:
            print "[EXIF] Error for: ", filename

for filename in videos_in_landing_location:
    base_filename = os.path.basename(filename)
    # Find first number location
    index = 0
    for i, c in enumerate(base_filename):
        if c.isdigit():
            index = i
            break
    try:
        date_from_filename = base_filename[index:index+8]
        # This will check we have a real date in the format YYYYMMDD
        date_taken = datetime.datetime.strptime(date_from_filename, "%Y%m%d")
        if(move(date_taken, filename)):
            flag_new_files = True
    except:
        print "[VIDEO DATE] Error for: ", filename


# Set exit codes
if(flag_new_files):
    sys.exit(0)
else:
    sys.exit(1)


