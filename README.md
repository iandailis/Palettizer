# Palettizer

Generates SV modules that output a given image, compressed using a k-means quantizer.

Wanted to create this because I saw so many people store their sprite and background data with raw pixel values, causing either low resolution or very long compile times, and that just pained me.
Therefore, I created this so you can still have beautiful pictures with low compile times and efficient compression.

# How to use:

1) Get all the required libraries (scikit-image and sklearn) by running "pip install -r requirements.txt"
2) Run "main.py"
3) Follow the instructions in the terminal. There are two provided images to try out. EDIT: USE RELATIVE PATH, ABSOLUTE PATH MAY NOT WORK. PUT THE IMAGE IN THE SAME FOLDER AS main.py
4) Look at the generated output image in the generated folder and decide if the settings were good enough.
5) Put the generated folder into your main project directory and add the three sv files to your project.
6) Instantiate the <picture_name>_mapper module

# Things to note:

- Deciding how many colors to use depends on your image. You will need to make a compromise between resolution and number of colors. Some images are mostly of one range of colors, while others may go across the entire spectrum. For example, "butterfly.jpg" is mostly yellow, so you can get away with only using 4 bits and thus having the full 640x480 resolution. "cat.jpg" uses many more colors though, so it will look better if you use 8 bits and sacrifice some resolution.
- M9K usage is weird. Just because a device has a certain number of bits, doesn't mean that it will be able to use it all effectively if your data width is weird. The automatic resolution function does work till 8 bits reliably.
- If you want to put anything other than one image into your M9k blocks, dont use the automatic resolution. Set your own resolution.
- This program generates three files so that you can use bits and pieces if you want. If you are making a sprite, don't use the mapper sv file, and just take the rom and palette.

Enjoy!
-Ian
