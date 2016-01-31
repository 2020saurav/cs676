import cv2
import math
import copy
from helper import *

# read image
rgb_img = cv2.imread('test.png')
#convert to LUV space
img = cv2.cvtColor(rgb_img, cv2.cv.CV_BGR2Luv)

height = img.shape[0]
width  = img.shape[1]

MAX_EPOCH = 3
SPACE_SCALE = 0.5

sr = 3
rr = 2
L = {} # Set of basin of attraction of modes
C = {} # Set of colors of modes
basin_list = []

# returns vector with space and range coordinates
def get_vector(i, j):
	return [i, j, img[i][j][0], img[i][j][1], img[i][j][2]]

# Estimate of probability density function (not normalized)
def scaled_pdf_est(x):
	est = 0
	for i in range(0, height):
		for j in range(0, width):
			x_i                = get_vector(i, j)
			del_x              = difference(x, x_i)
			scaled_del_space_x = multiply(del_x[:2], 1.0/sr)
			scaled_del_range_x = multiply(del_x[2:], 1.0/rr)
			est               += epan_kernel(sq_norm(scaled_del_space_x)) * epan_kernel(sq_norm(scaled_del_range_x)) / sr**2 / rr**3
	return est

# compute coordinate of next mean
def next_mean(x):
	num = (0, 0, 0, 0, 0)
	den = 0
	#x   = get_vector(ci, cj)
	# find next mean within bandwidth? or the whole matrix?
	#for i in range(max(0, ci - BANDWIDTH), min(height, ci + BANDWIDTH)):
	#	for j in range(max(0, cj - BANDWIDTH), min(width, cj + BANDWIDTH)):
	for i in range(0, height):
		for j in range(0, width):
			x_i          = get_vector(i, j)
			del_x        = difference(x, x_i)
			scaled_del_space_x = multiply(del_x[:2], 1.0/sr)
			scaled_del_range_x = multiply(del_x[2:], 1.0/rr)
			scaled_del_x = scaled_del_space_x +  scaled_del_range_x
			g_val        = g_flat(sq_norm(scaled_del_x))
			num          = add(num, multiply(x_i, g_val))
			den         += g_val
	return multiply(num, 1.0/den)

# whether 2 basins can be merged
def can_merge(i, j):
	basin1 = basin_list[i]
	basin2 = basin_list[j]
	x1 = basin1[0][0]
	y1 = basin1[0][1]
	x2 = basin2[0][0]
	y2 = basin2[0][1]
	space_dist_sq = ((x1-x2)**2 + (y1-y2)**2)
	if space_dist_sq <= sr**2:
		return True
	c1 = C[(x1, y1)]
	c2 = C[(x2, y2)]
	color_dist_sq = (c1[0]-c2[0])**2 + (c1[1]-c2[1])**2 + (c1[2]-c2[2])**2
	if color_dist_sq <= rr**2:
		return True
	return False

# merge 2 basins of attraction
def merge(i, j):
	global basin_list
	basin1 = basin_list[i]
	basin2 = basin_list[j]
	x1 = basin1[0][0]
	y1 = basin1[0][1]
	x2 = basin2[0][0]
	y2 = basin2[0][1]
	c1 = C[(x1, y1)]
	c2 = C[(x2, y2)]
	pdf1 = scaled_pdf_est((x1, y1, c1[0], c1[1], c1[2]))
	pdf2 = scaled_pdf_est((x2, y2, c2[0], c2[1], c2[2]))
	if pdf1 >= pdf2:
		mode_x = x1
		mode_y = y1
	else:
		mode_x = x2
		mode_y = y2
	merged_basin = ((mode_x, mode_y), basin1[1] + basin2[1])
	basin_list = basin_list[:i] + [merged_basin] + basin_list[i+1:j] + basin_list[j+1:]

# Find basins of attraction
for i in range(0, height):
	for j in range(0, width):
		x = get_vector(i,j)
		for epoch in range(0, MAX_EPOCH):
			y = next_mean(x)
			x = y
		mode_x = y[0]
		mode_y = y[1]

		if (mode_x, mode_y) in L:
			L[(mode_x, mode_y)].append((i, j))
		else:
			L[(mode_x, mode_y)] = [(i, j)]
			C[(mode_x, mode_y)] = (y[2], y[3], y[4])

# merge
basin_list = sorted(L.iteritems())
for i in range (0, len(basin_list)):
	for j in range(i+1, len(basin_list)):
		if j >= len(basin_list):
			break # since basin_list is being changed
		if can_merge(i, j):
			merge(i, j)

new_img = copy.deepcopy(img)
# form segmented image
for i in range(0, len(basin_list)):
	b = int (C[basin_list[i][0]][0])
	g = int (C[basin_list[i][0]][1])
	r = int (C[basin_list[i][0]][2])
	for (x, y) in basin_list[i][1]:
		new_img[x][y] = [b, g, r]
new_rgb_img = cv2.cvtColor(new_img, cv2.cv.CV_Luv2BGR)
cv2.imwrite("test_flat_seg.png", new_rgb_img)
