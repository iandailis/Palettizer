# Palettizer

Generates SV modules that output a given image, compressed using k-means clustering.

Wanted to create this because I saw so many people store their sprite and background data with raw pixel values, causing either low resolution or very long compile times, and that just pained me.
Therefore, I created this so you can still have beautiful pictures with low compile times, efficient compression, and easy integration.

# How to use:

1) Download Python (developed on 3.11.1 for Windows 10, but other configurations should also work)
2) Open a terminal. For Windows, use powershell.
3) Get all the required libraries by running ```pip install -r requirements.txt```
2) Run ```python main.py```
3) Follow the instructions in the terminal. There are two provided images to try out.
4) Look at the generated output image in the generated folder and decide if the settings were good enough.
5) Put the generated folder into your main project directory and add the three sv files to your project.
6) Instantiate the <picture_name>_mapper module

# Things to note:

- Use a virtual environment when installing python packages. Makes your future life easier. Instructions are here: https://docs.python.org/3/library/venv.html

Essentially, do:
```python -m venv .venv``` This creates a virtual environment, the files being inside a directory ```.venv/```

```./.venv/Scripts/Activate.ps1``` This activates the virtual environment. Use a different activation script depending on your operating system.

Now, run the pip commands to install packages and it will not be cluttering the global directory where you may never use it again.

- Deciding how many colors to use depends on your image. You will need to make a compromise between resolution and number of colors. Some images are mostly of one range of colors, while others may go across the entire spectrum. For example, "butterfly.jpg" is mostly yellow, so you can get away with only using 4 bits and thus having the full 640x480 resolution. "cat.jpg" uses many more colors though, so it will look better if you use 8 bits and sacrifice some resolution.

- M9K usage is weird. Just because a M9K has a certain number of bits, doesn't mean that it will be able to use it all effectively, depending on the data width.

- This program generates three files so that you can use bits and pieces if you want. If you are making a sprite, don't use the mapper sv file, and just take the rom and palette.

Enjoy!
-Ian
