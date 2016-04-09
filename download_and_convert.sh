# scp to location
scp -r 192.168.1.207:/var/www/videos/ ./
scp -r 192.168.1.207:/var/www/photos/ ./

# Clear out old photos thumbnails
find ./photos/ -type f -name "*248x372*" -delete
find ./photos/ -type f -name "*760x760*" -delete

# Check correct Startign dir
cd photos/
#for DIR in */*; do [ -d "$DIR" ] && cd $DIR && find . -mindepth 2 -type f -name '*' |   perl -l000ne 'print $_;  s/\//-/g; s/^\.-/.\// and print' | xargs -0n2 mv   && cd ../..; done
find ./*/ -depth -type d  -exec rmdir -p --ignore-fail-on-non-empty {} \;
cd ..

# Clear out old videos thumbnails
find ./videos/ -type f -name "*.jpg" -delete
find ./videos/ -type f -name "*.flv" -delete
# Alot of files of 3gp - Old format! Pretend they are all avi
find ./videos/ -type f -name "*.3gp" -exec mv '{}' '{}'.avi \;
