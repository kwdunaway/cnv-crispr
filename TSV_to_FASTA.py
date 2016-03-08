#!/usr/bin/python
import sys, getopt


################################################################################
# Author: Keith Dunaway
# Email: kwdunaway@ucdavis.edu
# Date: 2-26-2016
#
# This script creates a FASTA file from a .tsv file. The format of each
# sequence within the FASTA file created is as follows:
# >genename_sequence
# sequence
#
# Esample output in fasta file:
# >A1BG_ACCTGTAGTTGCCGGCGTGC
# ACCTGTAGTTGCCGGCGTGCNGG
# >A1BG_GTCGCTGAGCTCCGATTCGA
# GTCGCTGAGCTCCGATTCGANGG
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
	seqcol = 2			#Set global variable to define column that contains sequence
	genecol = 0			#Set global variable to define column that contains gene name		

	try:
		opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
	except getopt.GetoptError:	
		print 'Error:' , sys.argv[0]
		print '\t-i,--ifile\t <inputfile.tsv>'
		print '\t-o,--ofile\t <outputfile.fa>'
		sys.exit()
	for opt, arg in opts:
		if opt == '-h':
			print 'Error:' , sys.argv[0]
			print '\t-i,--ifile\t <inputfile.tsv>'
			print '\t-o,--ofile\t <outputfile.fa>'
			sys.exit()
		elif opt in ("-i", "--ifile"):
			try:
				INPUT = open(arg, 'r')
			except IOError:
				print 'I/O error: Cannot open',arg 
				return			
		elif opt in ("-o", "--ofile"):
			try:
				OUTPUT = open(arg, 'w')
			except IOError:
				print 'I/O error: Cannot open',arg 
				return			
	
	

####################################################################
#                 Main Loop going through INPUT                    #
####################################################################

	#Loop that goes through input, line by line, to find the sequences for output
	for inline in INPUT:

		#Tab separate line
		data = inline.split("\t")
		
		#If header line, skip line
		if (data[0] == "gene_name"):
			continue
		
		#Print description line which contains Gene name followed by counter, then sequence
		OUTPUT.write('>' + data[genecol] + '_' + data[seqcol] + '\n')
		#Prints FASTA sequence to be aligned
		OUTPUT.write(data[seqcol] + 'NGG\n')

	#Close I/O files	
	INPUT.close()
	OUTPUT.close()



if __name__ == '__main__':
   main(sys.argv[1:])
