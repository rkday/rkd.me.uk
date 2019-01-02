POST=$1
NEW=posts/$(basename $POST)

./port.py $POST $NEW
git rm $POST
git add $NEW
cobalt build
