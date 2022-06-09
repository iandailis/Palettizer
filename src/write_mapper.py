from math import ceil, log2

def write_mapper(image_name, image_shape, width, depth):
	print("Generating mapper module... ", end="", flush=True)

	# build the file
	buildString = f""

	# module header
	buildString += f"module {image_name}_mapper (\n"
	buildString += f"\tinput logic [9:0] DrawX, DrawY,\n"
	buildString += f"\tinput logic vga_clk, blank,\n"
	buildString += f"\toutput logic [3:0] red, green, blue\n"
	buildString += f");\n"
	buildString += f"\n"

	# variable instantiations
	buildString += f"logic [{ceil(log2(depth))}:0] rom_address;\n"
	buildString += f"logic [{width}:0] rom_q;\n"
	buildString += f"\n"
	buildString += f"logic [3:0] palette_red, palette_green, palette_blue;\n"
	buildString += f"\n"

	# address into the rom = x*xDim/640 + y*yDim/480 * xDim
	buildString += f"assign rom_address = (DrawX*{image_shape[1]}/640) + (DrawY*{image_shape[0]}/480 * {image_shape[1]});\n"
	buildString += f"\n"

	# set rgb values synchronously, taking into account the blank signal 
	buildString += f"always_ff @ (posedge vga_clk) begin\n"
	buildString += f"\tred <= 4'h0;\n"
	buildString += f"\tgreen <= 4'h0;\n"
	buildString += f"\tblue <= 4'h0;\n"
	buildString += f"\n"
	buildString += f"\tif (blank) begin\n"
	buildString += f"\t\tred <= palette_red;\n"
	buildString += f"\t\tgreen <= palette_green;\n"
	buildString += f"\t\tblue <= palette_blue;\n"
	buildString += f"\tend\n"
	buildString += f"end\n"
	buildString += f"\n"

	# instantiate the ROM
	buildString += f"{image_name}_rom {image_name}_rom (\n"
	buildString += f"\t.clock   (vga_clk),\n"
	buildString += f"\t.address (rom_address),\n"
	buildString += f"\t.q       (rom_q)\n"
	buildString += f");\n"
	buildString += f"\n"

	# instantiate the palette
	buildString += f"{image_name}_palette {image_name}_palette (\n"
	buildString += f"\t.index (rom_q),\n"
	buildString += f"\t.red   (palette_red),\n"
	buildString += f"\t.green (palette_green),\n"
	buildString += f"\t.blue  (palette_blue)\n"
	buildString += f");\n"
	buildString += f"\n"

	buildString += f"endmodule\n"

	# write to file
	with open(f"./{image_name}/{image_name}_mapper.sv", "w") as f:
		f.write(buildString)

	print("Done")