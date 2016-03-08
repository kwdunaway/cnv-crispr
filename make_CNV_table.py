#!/usr/bin/python
import sys, getopt
from collections import defaultdict

################################################################################
# Author: Keith Dunaway
# Email: kwdunaway@ucdavis.edu
# Date: 3-5-2016
#
# This script take multiple files in, slurps relevant information, and
# outputs a CNV table that is tab-separated. This can further be analyzed
# using R, Python, or Excel.
#
################################################################################




####################################################################
# Some of this section of code copied from
# http://www.tutorialspoint.com/python/python_command_line_arguments.htm
####################################################################
# Main subroutine, will only run if this is the main python script called
def main(argv):


####################################################################
# Command Line Error Checking. Global Variables and I/O Initiation #
####################################################################
	CNV_list = []				#Global list that contains CNV information for the cell
	CNVtable_dic = {}			#Global dictionary that contains all carried over printed information

	try:
		opts, args = getopt.getopt(argv,"hc:s:t:g:o:",["cfile=","sfile=","tfile=","gfile=","ofile="])
	except getopt.GetoptError:	
		print 'Error:' , sys.argv[0]
		print '\n-c,--cfile\t <906793.csv>'
		print '\n-s,--sfile\t <guide_sequences.sam>'
		print '\n-t,--tfile\t <Shalem_2014Table_S1.txt>'
		print '\n-g,--gfile\t <crispr_guide_data_mac.tsv>'
		print '\n-o,--ofile\t <outputfile.tsv>'
		sys.exit()
	for opt, arg in opts:
		if opt == '-h':
			print 'Error:' , sys.argv[0]
			print '\n-c,--cfile\t <906793.csv>'
			print '\n-s,--sfile\t <guide_sequences.sam>'
			print '\n-t,--tfile\t <Shalem_2014Table_S1.txt>'
			print '\n-g,--gfile\t <crispr_guide_data_mac.tsv>'
			print '\n-o,--ofile\t <outputfile.tsv>'
			sys.exit()
		elif opt in ("-c", "--cfile"):
			try:
				CNV = open(arg, 'r')
			except IOError:
				print 'I/O error: Cannot open',arg 
				return			
		elif opt in ("-s", "--sfile"):
			try:
				SAM = open(arg, 'r')
			except IOError:
				print 'I/O error: Cannot open',arg 
				return
		elif opt in ("-t", "--tfile"):
			try:
				TARGETOS = open(arg, 'r')
			except IOError:
				print 'I/O error: Cannot open',arg 
				return			
		elif opt in ("-g", "--gfile"):
			try:
				GUIDE = open(arg, 'r')
			except IOError:
				print 'I/O error: Cannot open',arg 
				return			
		elif opt in ("-o", "--ofile"):
			try:
				OUTPUT = open(arg, 'w')
			except IOError:
				print 'I/O error: Cannot open',arg 
				return			
		


########################################################################
#                           Process CNV file                           #
########################################################################
	n = 0		# Counter for CNV_list
	for inline in CNV:
		#remove end of line character
		inline = inline.rstrip('\n')

		#Splits the comma separated file into components	
		data = inline.split(",")
		
		#If there is a header line, skip it
		if (data[0] == '#sample_name'):
			continue

		CNVcount = int(data[11])		# Copy number for specified region
		#If the CNVcount is 2, skip the line
		if (CNVcount == 2):
			continue
		#If chromosome name is chr-, skip line
		chr = 'chr' + data[4]			# Chromosome for specified region
		if (chr == 'chr-'):
			continue

		start = int(data[5])			# Start of specified region
		end = int(data[6])				# End of specified region
		
		#Adds information to CNV_list so it can be used in downstream processes
		CNV_list.append([])
		CNV_list[n].append(chr)
		CNV_list[n].append(start)
		CNV_list[n].append(end)
		CNV_list[n].append(CNVcount)
		n = n + 1						# Iterates counter
	CNV.close()
	del n								# deletes counter
	


########################################################################
#                           Process SAM file                           #
########################################################################
	n = 0		# Counter for CNV_list (again)
	for inline in SAM:
		#Skips header lines of sam file
		if (inline.startswith('@')):
			continue
	
		#Remove end of line character
		inline = inline.rstrip('\n')

		#Splits tab separated file and header cell
		data = inline.split('\t')
		head = data[0].split('_')

		#Pull out important information from sam line
		gene = head[0]
		sequence = head[1]
		location = int(data[3])
		chr = data[2]
		samcnv = 2
		
		#Goes through CNV_list looking to determine if the read is located in
		#     a CNV area other than 2
		for sublist in CNV_list:
			#If you find a CNV, change samcnv to the new cnv and exit loop
			if(chr == sublist[0] and location > sublist[1] and location < sublist[2]):
				samcnv = sublist[3]
				continue

		#Adds chromosome, position, and CNV of a given sequence to the CNVtable_dic
		CNVtable_dic.update({sequence:[chr, location, samcnv]})

	SAM.close()
	del n



########################################################################
#                         Process TARGETOS file                        #
########################################################################
	for inline in TARGETOS:
		#skips header lines of sam file
		if ('mismatches' in inline):
			continue

		#remove end of line character
		inline = inline.rstrip('\n')
		
		#Splits tab separated file and header cell
		data = inline.split('\t')

		#Pull out important information Off-target score file
		sequence = data[7]
		OffScore = float(data[6])
		
		#If the sequence in the TARGETOS file had a corresponding read...
		if CNVtable_dic.has_key(sequence):
			#...Add score to CNVtable_dic
			CNVtable_dic[sequence].append(OffScore)
		#Else, throw out Off-target score information

	TARGETOS.close()



########################################################################
#                     Process guide RNA TSV file                       #
########################################################################
	for inline in GUIDE:
		#remove end of line character
		inline = inline.rstrip('\n')
		
		#Takes header and prints it to outfile, along with new column headers
		if ('gene_name' in inline):
			OUTPUT.write(inline + '\tchromosome\tstart\tCNVcount\tOS\n')
			continue

		#Splits tab separated file and header cell
		data = inline.split('\t')

		#Find 
		sequence = data[2]

		#If target sequence is in 
		if CNVtable_dic.has_key(sequence):
			if len(CNVtable_dic[sequence]) > 3:
				#Prints all information to outfile
				OUTPUT.write(inline + '\t' + CNVtable_dic[sequence][0] + '\t' + str(CNVtable_dic[sequence][1]) + '\t' + str(CNVtable_dic[sequence][2]) + '\t' + str(CNVtable_dic[sequence][3]) + '\n')
			else:
				#Print error messages if the target sequence did not have Off-target score
				print 'Error, CNV sequence information is incomplete:\t' + CNVtable_dic[sequence]
				print 'Line of guide table:\t' + inline
		else:
			#Print error messages if the target sequence was not found in the sam file
			#Possibly, it did not get aligned
			print 'Error, could not fine target sequence:\t' + sequence
			print 'Line of guide table:\t' + inline
			
	GUIDE.close()
	OUTPUT.close()


		
if __name__ == '__main__':
   main(sys.argv[1:])
