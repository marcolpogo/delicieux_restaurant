#! /bin/bash

url="http://127.0.0.1:5000/api/modification"
prevName="DUMMY PREV NAME"
updName="$1"

curl $url -H "Content-Type: application/json" -d "{\"previousName\":\"$prevName\",\"updatedName\":\"$updName\"}"
