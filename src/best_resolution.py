from math import ceil, log2, sqrt

def best_resolution(k):
	totalBits = 182*1024*8

	# manual testing, m9k block usage is wack
	if (k == 5):
		totalBits = 181*1024*8
	elif (k == 6):
		totalBits = 181*1024*8
	elif (k == 8):
		totalBits = 180*1024*8
	
	# retains 4:3 aspect ratio to keep square pixels.
	x = int(sqrt(4/3*(totalBits//k)))
	y = int(sqrt(3/4*(totalBits//k)))

	return min(x, 640), min(y, 480)
