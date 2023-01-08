# Palettizer

Generates SV modules that output a given image, compressed using k-means clustering.

I created this tool because I saw so many people store their sprite and background data with raw pixel values, causing either low resolution or very long compile times, and that just pained me. This tool generates SystemVerilog modules that output beautiful pictures with low compile times, efficient compression, and easy integration.

# How to use:

1) Download Python (developed on 3.11.1 for Windows 10, but other configurations should also work).
2) Open a terminal. For Windows, use powershell.
3) Get all the required libraries by running ```pip install -r requirements.txt```.
4) Run ```python main.py```
5) Follow the instructions in the terminal. There are two provided images to try out.
6) Look at the generated output image in the generated folder and decide if the settings were good enough.
7) Put the entire generated folder into your main project directory (that's the same place as your .qpf file).
8) Add the three .sv files in the folder to your Quartus project (rom, palette, and example).
9) Instantiate the example module in your project, connect all the signals, and compile.
10) Program the FPGA and verify that you see your generated image on the screen. If so, the tool has worked!

# FAQ:

* *Warning (10858): Verilog HDL warning at <image_name>_rom.sv(7): object memory used but never assigned*  
Don't worry about it.

* *Warning (10230): Verilog HDL assignment warning at <image_name>_example.sv(12): truncated value with size 32 to match size of target (11)*  
Also don't worry about it.

* *Error (127001): Can't find Memory Initialization File or Hexadecimal (Intel-Format) File ./<image_name>/<image_name>.mif for ROM instance ALTSYNCRAM*  
This one you worry about. The comment on <image_name>_rom.sv (7) is a compiler directive to initialize the inferred M9K memory with the contents in a given .mif file. This error message means it couldn't find the generated .mif file. There are a few things you can do here:
	* Option 1 (recommended): Make sure the generated folder is in the same place as the .qpf (quartus project) file. The specified path in the generated rom assumes this.
	* Option 2 (could be easier): Change the path in the compiler directive to the actual path of the generated .mif file. It could also be an absolute path.
	
* *How does this tool work?*  
Essentially, I took from ECE 311 Lab 4 Exercise 6 the provided LM Quantizer, somewhat simplified it, then created a bunch of wrapper code that generates the modules and assets. Here is some further reading into k-means clustering:  
https://en.wikipedia.org/wiki/K-means_clustering  
https://scikit-learn.org/stable/modules/clustering.html#k-means  

# Notes/Recommendations:

* The picture in the ROM is stored in row-major order. At every address is stored one pixel's palette index.

* If you are making sprites, don't just use the example. Instead, instantiate and use the rom and the palette in your existing color mapper module similarly to the example, then change the rom address calculation and other stuff (yes this isn't that specific, but sprites are a very broad thing with many implementations).

* To do transparency for your sprites:
	1) In the original image, make the background color drastically different from the rest of the image. Hot pink is usually a good color.
	2) Use the tool and regenerate the modules/assets.
	3) When setting the VGA R/G/B outputs based on DrawX/Y, don't just look at sprite_on. Also make sure the palette module's r/g/b output isn't that same hot pink.  

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
	1) ```python -m venv .venv``` This creates a virtual environment, the files being inside a directory ```.venv/```

	2) ```./.venv/Scripts/Activate.ps1``` This activates the virtual environment. Use a different activation script depending on your operating system.

	3) Run ```pip install -r requirements.txt``` The packages will no longer clutter the global directory where you may never use them again.

* Deciding how many colors to use depends on your image. You will need to make a compromise between resolution and number of colors. Some images are mostly of one range of colors, while others may go across the entire spectrum. For example, "butterfly.jpg" is mostly yellow, so you can get away with only using 4 bits and thus having the full 640x480 resolution. "cat.jpg" uses many more colors though, so it will look better if you use more bits for more colors and sacrifice some resolution.

* M9K usage is weird. Just because a M9K has a certain number of bits, doesn't mean that it will be able to use it all effectively, depending on the data width.

Enjoy!
-Ian D
