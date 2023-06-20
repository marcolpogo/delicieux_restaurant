#! /bin/bash

url="https://ctf.ageei.org/delicieuxrestaurant//api/modification"
prevName="DUMMY PREV NAME"
updName="$1"

curl $url -H "Content-Type: application/json" -d "{\"previousName\":\"$prevName\",\"updatedName\":\"$updName\"}"
