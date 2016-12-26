#!/usr/bin/python
import sys
kmer = 0
file_ = sys.argv[0]
#The program parameters are being sent in
for count in range(len(sys.argv)):
	if sys.argv[count] == "-f":
		file_ = sys.argv[count+1]
	if sys.argv[count] == "-k":
		kmer = int(sys.argv[count+1])

#Two dictionaries created. One is holding the kmers and there occurrences and the other the frequency of such occurrences
dict_ = {}
dict_2 = {}
file = open(file_, "r")

#Function to create a dictionary of kmers and their occurrences
def k_mer(kmer,line):
	end_count = kmer 
	count_char = 0
	while end_count < (len(line)):
		current_kmer = line[count_char:end_count]
		if current_kmer in dict_:
			dict_[current_kmer] = dict_[current_kmer] + 1
		if current_kmer not in dict_:
                        dict_[current_kmer] = 1
		end_count = end_count + 1
		count_char = count_char + 1

#Function to take the previous dictionary and get a frequency of occurrences.
def kmer_I(dict_):
	count_dict = 0
#The list array is only of the values. The actual occurrences are irrelevany
	list = dict_.values()
	list = sorted(list)
	for iterator in range(len(list)):	
		count_dict = list[iterator]	
#Dictionary 2 is filled with the occurrences
		if list[iterator] in dict_2:
			dict_2[count_dict] = dict_2[count_dict] + 1
		if list[iterator] not in dict_2:
			dict_2[count_dict] = 1
	

#The functions run for every read
count_file = 0
for line in file:
	if count_file % 4 == 1:
		k_mer(kmer,line)
	count_file = count_file + 1

#Once the dictionary is created dict_2 can be created off of that final result. Excluded from line loop
kmer_I(dict_)


#Printing format
print("#k-mer frequency	Number of k-mers in this Category")


#Opening and writing keys and values to respective values
list_key = dict_2.keys()
list_values = dict_2.values()
file_key = open("output_kspec_key.txt" , "w")
file_value = open("output_kspec_value.txt" , "w")

#Printing to standard line
y = 0
while y < len(dict_2):
	print("%d	%d" % (list_key[y],list_values[y]))	
	y = y+1

#Writing specific files with keys and values
file_key.write(str(list_key))
file_value.write(str(list_values))
