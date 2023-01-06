
#!/bin/bash

#Create a font character sheet of a font, OCR it
#First argument is the path to the font
echo "base_alpha:"
CSET="$(echo {a..z} {A..Z} | tr -d ' ')"
echo $CSET

convert -monochrome -font "$1" -pointsize 32 -density 300 -kerning 64 label:"$CSET" out.png

echo "cipher_alpha:"
tesseract out.png - --dpi 300 -c tessedit_char_whitelist="$CSET" -l lat --psm 13

# open the generated image, and validate that it matches the OCR string output
# these can now be used for dejumbling by configuring the `chipher_alpha` and `base_alpha` variables for the book in `books.yml`
