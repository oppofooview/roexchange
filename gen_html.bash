#1/bin/bash
filename="index.html"
cd dist
echo "<html>" > $filename
echo "  <head>" >> $filename
echo "    <title>This is the title of the webpage!</title>" >> $filename
echo "  <body>" >> $filename
find images -type f -printf "      <img src=\"images/%f\"/^>\n" >> $filename
echo "  </body>" >> $filename
echo "</html>" >> $filename

