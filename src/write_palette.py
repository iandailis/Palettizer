from math import ceil, log2

def write_palette(image_name, palette):
	print("Generating palette module... ", end="", flush=True)
	
	buildString = (
		# module header
		f"""module {image_name}_palette (\n"""
		f"""\tinput logic [{ceil(log2(len(palette))) - 1}:0] index,\n"""
		f"""\toutput logic [3:0] red, green, blue\n"""
		f""");\n"""
		f"""\n"""

		# variable declarations
		f"""logic [11:0] palette [{len(palette)}];\n"""
		f"""assign {{red, green, blue}} = palette[index];\n"""
		f"""\n"""

		# defining each palette position
		f"""always_comb begin\n"""
	)
	for i, color in enumerate(palette):
		buildString += f"""\tpalette[{i:02}] = {{4'h{color[0]>>4:1X}, 4'h{color[1]>>4:1X}, 4'h{color[2]>>4:1X}}};\n"""
	buildString += f"""end\n"""
	buildString += f"""\n"""

	buildString += f"""endmodule\n"""

	# write to file
	with open(f"""./{image_name}/{image_name}_palette.sv""", "w") as f:
		f.write(buildString)
	print("Done")
