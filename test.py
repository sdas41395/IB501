#!/usr/bin/python
import math
array_ = [0.0] * 101
file = open('lane1_NoIndex_L001_R1_003.fastq','r')
count = 0
count_file = 0
count_tot = 1

#This function converts every passing quality character into an appropriate phred score according to 1.8 standards
def convert_phred(position_):
	position_ = ord(position_) - 33
	return position_

#This is creating the main arrays to be used throughout the program. One array is a double that contains the values of that position. The rest are the variance, standard deviation, and the mean 
array_med = []
for i in range(101):
	array_med.append([])

array_var = [0.0] * 101
array_std = [0.0] * 101




#This loop is collecting the sum total of all points into the array that will be holding the mean. After collection the mean is calculated for every point. The double array is storing all points into each position.
#Count_tot is the total amount of files present in the file itself. Modding it by 4 gives the phred score line. 
#count_file gives the total length of all the files which is just the total divided by 4. It will be used to divide the sum at each posiiton to get the mean. 
for line in file:
	if count_tot % 4 == 0:
		random_array = [] 
		count = 0
		count_file = count_file + 1
		while count < 101:
			array_[count] = convert_phred(line[count]) + array_[count]
			if count >= 0 & count <101:
				array_med[count].append(convert_phred(line[count]))
			count = count + 1
	count_tot = count_tot + 1

#This loop is calculating the mean for every position in the mean array. Dividing by the total amount of files. 
x=0
while x < len(array_):
	array_[x] = array_[x]/count_file
	x = x + 1

#The phred values are being calcuated here which gives the variance and the std. deviation
phred_sum = 0
for i in range(101):
	phred_value = 0
	phred_mean = 0
	phred_sum = 0

        for x in range(count_file):
		phred_value = array_med[i][x]
                phred_mean = (phred_value - array_[i])**2
		phred_sum = phred_mean + phred_sum
	phred_sum = phred_sum/count_file 
	array_var[i] = phred_sum	

for i in range(101):
	array_std[i] = math.sqrt(array_var[i])


#This is a check to see how far the program has gone
print("Finished variance, std, and mean")

#This array is holding all the values form the 2d array so the median can be calculated. Makes it easier to understand
array_med_val = [0.0] * 101
x = 0

#These two dictionaries will be holding the distribution of the 6th and the 95th position. 
count_6 = {}
count_94 = {}



#This while loop is going through every position and finding the median value. Note that the position values are being sorted to easier caluclate the median rather than iteratively looping through every point
#The center is our median and is dependent on whether the total length is odd or even
#If the position is 5 or 94 we want to keep all values and get a distribution curve
while x < 101:
	array_med[x] = sorted(array_med[x])
	center = len(array_med[x]) / 2
	if center % 2 != 0:
		array_med_val[x] = array_med[center]
	if center % 2 == 0:
		array_med_val[x] = (array_med[x][center + 1] + array_med[x][center])/2	
	if x == 5:
		for iterator in range(len(array_med[x])):
			if array_med[x][iterator] in count_6:
				count_6[array_med[x][iterator]] = count_6[array_med[x][iterator]] + 1
			if array_med[x][iterator] not in count_6:
				count_6[array_med[x][iterator]] =  1
	if x == 94:
		 for iterator in range(len(array_med[x])):
                        if array_med[x][iterator] in count_94:
                                count_94[array_med[x][iterator]] = count_94[array_med[x][iterator]] + 1
                        if array_med[x][iterator] not in count_94:
                                count_94[array_med[x][iterator]] =  1
	x = x+1

#The file being open will hold the count_6 and count_94 dictionaries to get the distributions. 
file_o = open("distributions.txt","w")
list6key = count_6.keys()
list6value =count_6.values()
list95key = count_94.keys()
list95value = count_94.values()
file_o.write(str(list6key))
file_o.write(str(list6value))
file_o.write(str(list95key))
file_o.write(str(list95value))


#This is just to print the values in a specific format
print("#Base Pair       Mean Quality Score	Standard Deviation	Variance	Median")
y=0
while y < 101:       
	 print("%d               %f		%f		%f		%f" % (y, array_[y], array_std[y], array_var[y],array_med_val[y]))
         y = y+1



