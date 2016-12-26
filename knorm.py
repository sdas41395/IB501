#!/usr/bin/python
import sys
coverage = 0
filename = ""

#This takes the command options and assigns them to global variables to be later used in the program
for x in range(len(sys.argv)):
        if sys.argv[x] == "-f":
                filename = sys.argv[x+1]
        if sys.argv[x] == "-c":
                coverage = int(sys.argv[x+1])


kmer = 15
file_out = open("output_knorm.txt","w")
dict_ = {}

#This function creates the dictionary holding the kmers
def k_mer(kmer,line):
        end_count = kmer
        count_char = 0
        list_ = []
        while end_count < (len(line)):
                current_kmer = line[count_char:end_count]
                if current_kmer in dict_:
                        dict_[current_kmer] = dict_[current_kmer] + 1
                if current_kmer not in dict_:
                        dict_[current_kmer] = 1
                list_.append(dict_[current_kmer])
                end_count = end_count + 1
                count_char = count_char + 1
#The list created is for the dictionary values. It is looking to find the median of the sorted values. Sorting the list improves upon the time 
        median = 0
        list_ = sorted(list_)
        center = len(list_)/2
        if center % 2 == 0:
                median = (list_[center + 1] + list_[center])/2
        if center % 2 != 0:
                median = list_[center]
#The median is returned
        return median

#The file is opened here and the program runs the function
file_ = open(filename,"r")
count_ = 0
#The loop travels through every fastq file and finds and comapres the median value to the coverage in the parameters.
for line in file_:
	if count_ % 4 == 1:
                coverage_obt = k_mer(kmer,line)
                if coverage_obt <= coverage:
                        file_out.write("\n")
                        file_out.write(line)
                        file_out.write("\n")
                        file_out.write("\n")
	count_ = count_ + 1
#The program does not print

