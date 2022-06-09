from math import ceil, log2

def write_rom(image_name, mif_name, width, depth):
	print("Generating ROM module... ", end="", flush=True)
	buildString = ""

	# module header
	buildString += f"module {image_name}_rom (\n"
	buildString += f"\tinput logic clock,\n"
	buildString += f"\tinput logic [{ceil(log2(depth)) - 1}:0] address,\n"
	buildString += f"\toutput logic [{width-1}:0] q\n"
	buildString += f");\n"
	buildString += f"\n"

	# variable declarations, rom gets instantiated with the compiler directive in the comment.
	buildString += f'logic [{width-1}:0] memory [0:{depth-1}] /* synthesis ram_init_file = "{mif_name}" */;\n'
	buildString += f"\n"

	# always output the data at the given address
	buildString += f"always_ff @ (posedge clock) begin\n"
	buildString += f"\tq <= memory[address];\n"
	buildString += f"end\n"
	buildString += f"\n"
	buildString += f"endmodule\n"

	# write to file
	with open(f"./{image_name}/{image_name}_rom.sv", "w") as f:
		f.write(buildString)

	print("Done")
