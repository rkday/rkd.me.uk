POST=$1
NEW=posts/$(basename $POST)

./port.py $POST $NEW
