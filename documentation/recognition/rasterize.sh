x=$1
convert -density 150 "$x" "${x%.*}.jpg"
