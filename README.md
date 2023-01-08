# Palettizer

Generates SV modules that output a given image, compressed using k-means clustering.

Wanted to create this because I saw so many people store their sprite and background data with raw pixel values, causing either low resolution or very long compile times, and that just pained me.
Therefore, I created this so you can still have beautiful pictures with low compile times, efficient compression, and easy integration.

# How to use:

1) Download Python (developed on 3.11.1 for Windows 10, but other configurations should also work).
2) Open a terminal. For Windows, use powershell.
3) Get all the required libraries by running ```pip install -r requirements.txt```.
4) Run ```python main.py```
5) Follow the instructions in the terminal. There are two provided images to try out.
6) Look at the generated output image in the generated folder and decide if the settings were good enough.
7) Put the generated folder into your main project directory (that's the same place as your .qpf file).
8) Add the three .sv files in the folder to your Quartus project (rom, palette, and example).
9) Instantiate the example module in your project, connect all the signals, and compile.
10) Program the FPGA and verify that you see your generated image on the screen. If so, the tool has worked!

# Notes/Recommendations:

* The picture in the ROM is stored in row-major order. At every address is stored one pixel's palette index.

* If you are making sprites, don't just use the example. Instead, instantiate and use the rom and the palette in your existing color mapper module similarly to the example, then change the rom address calculation and other stuff.

* To do transparency for your sprites:
	1) In the original image, make the background color drastically different from the rest of the image. Hot pink is usually a good color.
	2) When setting the VGA R/G/B outputs based on DrawX/Y, don't just look at sprite_on. Also make sure the palette module's r/g/b output isn't that same hot pink.  

* Here's an example for how to instantiate the example in your top level (to verify everything was generated/added correctly):  

```
logic vga_clk, blank;
logic [9:0] DrawX, DrawY;

vga_controller vga ( // the provided VGA controller from Lab 6 and 7
	.Clk       (MAX10_CLK1_50),
	.Reset     (1'b0),
	.hs        (VGA_HS),
	.vs        (VGA_VS),
	.pixel_clk (vga_clk),
	.blank     (blank),
	.sync      (),
	.DrawX     (DrawX),
	.DrawY     (DrawY)
);

pic_example pic ( // the generated example. in this case, the image was called "pic"
	.vga_clk (vga_clk),
	.DrawX   (DrawX), 
	.DrawY   (DrawY),
	.blank   (blank),
	.red     (VGA_R),
	.green   (VGA_G),
	.blue    (VGA_B)
);
```

* Use a virtual environment when installing python packages. Makes your future life easier. Instructions are here: https://docs.python.org/3/library/venv.html  

Essentially, do:
```python -m venv .venv``` This creates a virtual environment, the files being inside a directory ```.venv/```

```./.venv/Scripts/Activate.ps1``` This activates the virtual environment. Use a different activation script depending on your operating system.

Now, run the pip commands to install packages and it will not be cluttering the global directory where you may never use it again.

* Deciding how many colors to use depends on your image. You will need to make a compromise between resolution and number of colors. Some images are mostly of one range of colors, while others may go across the entire spectrum. For example, "butterfly.jpg" is mostly yellow, so you can get away with only using 4 bits and thus having the full 640x480 resolution. "cat.jpg" uses many more colors though, so it will look better if you use more bits for more colors and sacrifice some resolution.

* M9K usage is weird. Just because a M9K has a certain number of bits, doesn't mean that it will be able to use it all effectively, depending on the data width.

# FAQ:

* *Warning (10858): Verilog HDL warning at pic_rom.sv(7): object memory used but never assigned* - Don't worry about it, if the in the


Enjoy!
-Ian
