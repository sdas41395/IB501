#!/usr/bin/env python2

#importing Cairo drawing module
#importing re for regex
import cairocffi as cairo
import math

#
#
#                                       Preliminary cairo stuff
#
#
#img dictionary holding image-specific dimensions
#
img = {}
img['height'] = 800
img['width'] = 800
img['center_x'] = img['width'] / 2.0
img['center_y'] = img['height'] / 2.0
img['font_size'] = 16

#
# Define the path our file
#
outpath = './output.pdf'
ps = cairo.PDFSurface(outpath, img['height'], img['width'])
cr = cairo.Context(ps)

#
#------------------------------------------------------------------------------------
#
# All of your computation goes here...
#

#
#                               Data stored in dictionaries
#


# Add each chromosome to the dictionary and store the
# basepair and statistical value
#creating the keyvalue pairs within fst_stats and rna_stats
fst_stats_bp = {}
fst_stats_val = {}

rna_stats_bp = {}
rna_stats_val = {}

#opening files batch_1.phistats_fw2-oc.tsv and Gacu_FoldChange_GenomCoords.tsv
file_batch = open('./batch_1.phistats_fw2-oc.tsv' , 'r')
file_coords = open('./Gacu_FoldChange_GenomCoords.tsv', 'r')

#looking to store the basepair and chromosome value
#chromsome group located at column 5 and bp value located at column 6 in batch file
#Smoothed FST value located at 11

#parsing through the files to store data in dictionaries. We have two dictionaries
#for fst and rna. The dictionaries contain bp value and smoothed fst value
#First loop is inserting for the fst values and second for rna values. The next functions used to skip the header on batch
next(file_batch)
next(file_batch)
next(file_batch)
for line in file_batch:
        line = line.split('\t')
        if line[4] in fst_stats_bp:
                        fst_stats_bp[line[4]].append(line[5])

        else:
                        fst_stats_bp[line[4]] = [line[5]]
        if line[5] in fst_stats_val:
                        fst_stats_val[line[4]].append(line[10])
        else:
                        fst_stats_val[line[4]] = [line[10]]

for line in file_coords:
        line = line.split('\t')
        if line[1] in rna_stats_bp:
                        rna_stats_bp[line[1]].append(line[2])
        else:
                        rna_stats_bp[line[1]] = [line[2]]
        if line[1] in rna_stats_val:
                        rna_stats_val[line[1]].append(line[6])
        else:
                        rna_stats_val[line[1]] = [line[6]]






chrom_values = {'groupI'    : 28185914, 'groupII'   : 23295652, 'groupIII'   : 16798506, 'groupIV'  : 32632948, 'groupIX'   : 20249479, 'groupV'    : 12251397, 'groupVI'    : 17083675, 'groupVII' : 27937443, 'groupVIII' : 19368704, 'groupX'    : 15657440, 'groupXI'    : 16706052, 'groupXII' : 18401067, 'groupXIII' : 20083130, 'groupXIV'  : 15246461, 'groupXIX'   : 20240660, 'groupXV'  : 16198764, 'groupXVI'  : 18115788, 'groupXVII' : 14603141, 'groupXVIII' : 16282716, 'groupXX'  : 19732071, 'groupXXI'  : 11717487}
Group_Val = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII', 'XIII', 'XIV', 'XV', 'XVI', 'XVII', 'XVIII', 'XIX', 'XX', 'XXI']


#-------------------------------------------------------------------------------------
#
#                       pre-defined functions
#

#
# Convert a radius and a span of degrees into X, Y coordinates
#
def get_x_y_coordinates(center_x, center_y, degree, radius):
 if degree <= 90:
        theta = float(degree)
        opp_side = radius * math.sin(math.radians(theta))
        adj_side = radius * math.cos(math.radians(theta))
        x = center_x + adj_side
        y = center_y + opp_side
 elif degree <= 180:
        theta = float(degree - 90.0)
        opp_side = radius * math.sin(math.radians(theta))
        adj_side = radius * math.cos(math.radians(theta))
        x = center_x - opp_side
        y = center_y + adj_side
 elif degree <= 270:
        theta = float(degree - 180.0)
        opp_side = radius * math.sin(math.radians(theta))
        adj_side = radius * math.cos(math.radians(theta))
        x = center_x - adj_side
        y = center_y - opp_side
 else:
        theta = float(degree - 270.0)
        opp_side = radius * math.sin(math.radians(theta))
        adj_side = radius * math.cos(math.radians(theta))
        x = center_x + opp_side
        y = center_y - adj_side
 return (x, y)


def degree_calculate(group_size):
	values = chrom_values.values()
	total_size = sum(values)
	return float(group_size)/total_size * 360

def fst_calculate(fst_index, value, degree, degree_change):
 	array_fst = fst_stats_bp.get(fst_index)
	sum = 0
	for x in range(len(array_fst)):
		sum = sum + int(array_fst[x])
	return float(value)/sum * (degree_change - degree)


#------------------------------------------------------------------------------------
#
#                                         Drawing
#
#
# Choose a font
#
cr.select_font_face("Sans", cairo.FONT_SLANT_NORMAL,cairo.FONT_WEIGHT_NORMAL)
# Set the font size
cr.set_font_size(12)
# Choose a font color
cr.set_source_rgb(0, 0, 0)


#for loop will go thorugh all groups of chromosomes and create rectangles of appropriate size.
#uses variables defined earlier - chrom_values which is the array of chromosomes and function degree calculator
#delcaring variables to be used in for loop. r_in and r_out specify the inner and outer radius. 
#degree holds the previous end point degree value. 
r_in = 250
r_out = 300
degree = 0
degree_change = 0
chrom_count = 0

for value in chrom_values.values():
	
	x,y = get_x_y_coordinates(400,400,degree,r_in)
	cr.move_to(x,y)
	degree_change = degree_calculate(value) + degree
	degree_change_gap = degree_change - 2.5
	cr.arc(400,400,r_in,math.radians(degree),math.radians(degree_change_gap))
	x,y = get_x_y_coordinates(400,400,degree_change_gap,r_out)
	cr.line_to(x,y)
	cr.arc_negative(400,400,r_out,math.radians(degree_change_gap),math.radians(degree))
	cr.close_path()
	
	#doing the middle of the block
	x_l,y_l = get_x_y_coordinates(400,400,(degree_change_gap - degree)/2 + degree, r_out + 40)
	x_l2,y_l2 = get_x_y_coordinates(400,400,(degree_change_gap - degree)/2 + degree, r_in - 20)
	cr.move_to(x_l,y_l)
	cr.set_line_width(0.3)
	cr.line_to(x_l2,y_l2)
	cr.set_line_width(1.5)

	#text
	cr.select_font_face("Sans", cairo.FONT_SLANT_NORMAL,cairo.FONT_WEIGHT_NORMAL)
	cr.set_font_size(14)
	cr.set_source_rgb(0.1,0.2,0.3)
	textents = cr.text_extents(Group_Val[chrom_count])
	text_width = textents[2]
	text_height = textents[3]
	x_l,y_l = get_x_y_coordinates(400,400,(degree_change_gap - degree)/2 + degree, r_out + 60)
	cr.move_to(x_l,y_l)
	cr.show_text(Group_Val[chrom_count])
		

	#fst building
	chrom_list = fst_stats_bp.keys()
        current_chrom = chrom_list[chrom_count]
	#degree_prev = degree

	count = 0
	while count < (degree_change_gap - degree):
		x,y = get_x_y_coordinates(400,400,degree + (count), r_in)
                cr.move_to(x,y)
                x_f,y_f = get_x_y_coordinates(400,400,degree + (count),r_out)
                cr.line_to(x_f,y_f)
                cr.set_source_rgb(0.5,.5,.5)
                cr.stroke()
		cr.stroke_preserve()
                count = count + .05

	for iterator in range(len(fst_stats_bp[current_chrom])):
		array_fst = fst_stats_bp.get(current_chrom)
		degree_fst = fst_calculate(current_chrom, array_fst[iterator], degree, degree_change_gap)	
		degree_new = degree + degree_fst
		x,y = get_x_y_coordinates(400,400, degree + degree_fst, r_in)
		cr.move_to(x,y)
		x_f,y_f = get_x_y_coordinates(400,400,degree + degree_fst, r_out)
		cr.line_to(x_f,y_f)
		cr.set_source_rgb(0.1,.1,.1)
                cr.stroke()
                cr.stroke_preserve()

		#print (degree_new - degree_prev)
		
		#count = 0			
		#while count < degree_new - degree_prev:
		#	x,y = get_x_y_coordinates(400,400,degree + (count), r_in)
		#	cr.move_to(x,y)
		#	x_f,y_f = get_x_y_coordinates(400,400,degree + (count),r_out)
		#	cr.line_to(x_f,y_f)
		#	cr.set_source_rgb(.3,.2,.5)
		#	cr.stroke()
		#	cr.stroke_preserve()
		#	count = count + .05
		#	
		#degree_prev = degree_new

		
	
	degree = degree_change
	chrom_count = chrom_count + 1
	cr.set_source_rgb(0,0,0)
	cr.stroke()
        cr.stroke_preserve()
	cr.fill()			
	


#Calculating the FST proportions within each rectangular block







# Close the file
#
cr.show_page()
