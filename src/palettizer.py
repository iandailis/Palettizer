from numpy import array as np_array
from sklearn.cluster import KMeans

def palettizer(image, k):
	"""
	I took this code from the LM Quantizer in ECE 311 Lab 4, 
	and slightly refactored it. 
	"""
	print("Palettizing image... ", end="", flush=True)
	# easier variable names
	n_rows, n_cols = image.shape[0], image.shape[1]

	# create k-means object
	kmeans = KMeans(n_clusters = k)

	# reshape pixel value to be like data points
	pixel_vals = np_array([(image[row,col] & 0xF0) for row in range(n_rows) for col in range(n_cols)])

	# fit the k-means model to pixel data and get color labels
	image_palettized = kmeans.fit_predict(pixel_vals)

	# get the palette
	palette = kmeans.cluster_centers_.astype("uint8")

	print("Done")
	return image_palettized, palette
