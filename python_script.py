#!/usr/bin/python

file = open("output.sam","r")
mapped = 0
unmapped = 0
for line in file:
		#splitting the column. The flag is located in column 2 of the line. 
		column = line.split('\t')
		#disregarding the header files
		if '@' not in column[0]:
			#type cast the column to int
			flag = int(column[1])
			#if mapped and not repeated. 
			if (((flag & 4) != 4) and ((flag & 256) != 256)):
				mapped = mapped+ 1
			#if unmapped and not repeated
			if ((flag & 256) != 256 and (flag & 4) == 4):
				unmapped = unmapped + 1

#printing results
print ("Unmapped:" + str(unmapped))
print ("Mapped:" + str(mapped))

