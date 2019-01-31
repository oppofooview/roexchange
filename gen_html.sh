#1/bin/bash

cd dist
declare -a pages=("mats.html" "weapon_cards.html" "armor_cards.html" \
  "offhand_cards.html" "headgear_cards.html" "accessory_cards.html" \
  "footgear_cards.html")
declare -a folders=("images/Materials" "images/Cards/Weapon" \
  "images/Cards/Armor" "images/Cards/Offhand" "images/Cards/Headgear" \
  "images/Cards/Accessory" "images/Cards/Footgear")

for (( i=0; i<${#pages[*]}; ++i )); 
#i in "${arr[@]}"
do
  filename=${pages[$i]}
  folder=${folders[$i]}
  title=`echo $filename | cut -d'.' -f 1`
  echo "$filename, $folder, $title" 

  echo "<html>" > $filename
  echo "  <head>" >> $filename
  echo "    <title>$title</title>" >> $filename
  echo "  <body>" >> $filename
  find $folder -type f -printf "      <img src=\"$folder/%f\"/^>\n" >> $filename
  echo "  </body>" >> $filename
  echo "</html>" >> $filename
done

#filename="index.html"
#cd dist
#echo "<html>" > $filename
#echo "  <head>" >> $filename
#echo "    <title>This is the title of the webpage!</title>" >> $filename
#echo "  <body>" >> $filename
#find images -type f -printf "      <img src=\"images/%f\"/^>\n" >> $filename
#echo "  </body>" >> $filename
#echo "</html>" >> $filename

