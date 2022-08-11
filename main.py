from skimage.io import imread
from skimage.transform import resize

from src.palettizer import palettizer
from src.write_mif import write_mif
from src.write_png import write_png
from src.write_rom import write_rom
from src.write_palette import write_palette
from src.write_mapper import write_mapper
from src.best_resolution import best_resolution

from os import makedirs

def main():
	# open input image
	image_path = input("Path to input image (relative or absolute): ")
	image = imread(image_path).astype("uint8")

	# get number of colors to compress into
	k = int(input("Number of bits per pixel to store (only tested up to 8): "))

	# get resized image dimensions
	try:
		print("Press <Enter> without any input to auto-select the highest resolution for M9k blocks.")
		image_x = int(input("Desired output horizontal resolution: "))
		image_y = int(input("Desired output vertical resolution: "))
	except:
		print("Getting highest possible resolution... ", end="", flush=True)
		image_x, image_y = best_resolution(k)
		print(f"""Image will be {image_x} x {image_y}""")

	# check if parameters will fit into the M9k blocks
	mbits_available = 182*1024*8 # 182 M9k blocks * 1024 bytes per block * 8 bits per block
	mbits_used = image_x*image_y*k
	print(f"""Using {mbits_used} / {mbits_available} available M9k memory bits""")
	print("Design may still not fit. M9k block usage is weird.")

	# resize the image
	print("Resizing image... ", end="", flush=True)
	image_resized = resize(image, (image_y, image_x), anti_aliasing=True, preserve_range=True).astype("uint8")
	print("Done")

	# get the palettized image and the array of palettes
	image_palettized, palette = palettizer(image_resized, 2**k)

	# compress colors to 4 bit
	for i in range(len(palette)):
		for j in range(len(palette[i])):
			palette[i][j] &= 0xF0

	# set the image name and create the directory, if it does not exist
	image_shape = image_resized.shape
	image_name = image_path.rsplit('.')[0]
	try:
		makedirs(image_name)
	except:
		pass

	# create the mif (memory instantiation file)
	width, depth, mif_name = write_mif(image_palettized, k, image_name)

	# create the ROM that will read the mif
	write_rom(image_name, mif_name, width, depth)

	# create the palette module
	write_palette(image_name, palette)

	# create the mapper, which will use the palette and ROM modules
	write_mapper(image_name, image_shape, width, depth)

	# show the result
	write_png(image_palettized, palette, image_name, image_shape)

	print(f"""Output files are in ./{image_name}/""")


if (__name__ == "__main__"):
	try:
		main()
	except Exception as e:
		print(e)
