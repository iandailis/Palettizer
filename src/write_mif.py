
def write_mif(image_palettized, k, image_name):
	"""
	https://www.intel.com/content/www/us/en/programmable/quartushelp/13.0/mergedProjects/reference/glossary/def_mif.htm
	"""
	print("Generating MIF (Memory Instantiation File)... ", end="", flush=True)

	width = k
	depth = len(image_palettized)

	buildString = f""

	# construct header
	buildString += f"WIDTH={width};\n"
	buildString += f"DEPTH={depth};\n"
	buildString += f"\n"
	buildString += f"ADDRESS_RADIX=UNS;\n" # UNS = unsigned int
	buildString += f"DATA_RADIX=UNS;\n"
	buildString += f"\n"
	buildString += f"CONTENT BEGIN\n"

	# write data in address : data format
	for i, palette_index in enumerate(image_palettized):
		buildString += f"\t{i} : {palette_index};\n"
	
	buildString += f"END;\n"

	# write the data to the file
	mif_name = f"./{image_name}/{image_name}.mif"
	with open(mif_name, "w") as f:
		f.write(buildString)

	print("Done")
	return width, depth, mif_name
