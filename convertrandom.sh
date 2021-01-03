#!/usr/bin/env sh


while true
do
	RPHOTOS=$(python3 randomphoto.py)
	RPHOTOSA=($RPHOTOS)
	RPHOTO=${RPHOTOSA[0]}
	RPHOTOURL=${RPHOTOSA[1]}

	echo $RPHOTO
	echo $RPHOTOURL
	qrencode -o /tmp/testqr.png $RPHOTOURL
	convert $RPHOTO -auto-orient -rotate 90 -resize 758x1024 \
		-background black -gravity center -extent 758x1024 \
                /tmp/testqr.png -gravity SouthWest -geometry +5+5  -composite \
		-colorspace Gray -dither FloydSteinberg -remap kindle_colors.gif \
		-quality 75 -define png:color-type=0 -define png:bit-depth=8 \
		/tmp/output.png

	{ printf 'HTTP/1.0 200 OK\r\nContent-Length: %d\r\n\r\n' "$(wc -c < /tmp/output.png)"; cat /tmp/output.png; } | nc -l 8080
	date
done
