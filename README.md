# Homework - Copy Number Variation and CRISPR
## Objectives

Using CRISPR library data supplied and Copy Number Variation (CNV) data of your choice, identify relationships between CNV of target site and CRISPR guide activity. This CRISPR library was conducted in the A375 melanoma cell line, so CNV and genotype information should be obtained for this cell line using published literature or cell line databases. The data source should be justified.

## Outside data
In order to complete the task, you must first download the following data:

1. **CNV data**: The CNV data used in this pipeline came from [COSMIC](cancer.sanger.ac.uk). They have a vast repository of cell line data including CNV information on the A375 melanoma cell line. In order to download the data, you must first register [HERE](https://cancer.sanger.ac.uk/cosmic/register). Once your account is set up, type the following in terminal to get the CNV data on A375 melanoma cell line:

	```
	sftp username@sftp-cancer.sanger.ac.uk
	```
	(must enter password here)

	```
	sftp> get /files/grch38/cell_lines/v76/copy_number/906793.csv
	sftp> exit
	```

2. **Off-target data**: Off-target activity is an active interest of Desktop Genetics so this pipeline includes that information. The off-target scores of all probes can be found in Supplementary Table 1 of the original published paper [Shalem et al. 2014](http://www.ncbi.nlm.nih.gov/pubmed/24336571). The data is in excel format and needs to be converted to tab separated format. To do this, open the file in excel and save as a "Tab Delimited Text (*.txt)".

3. **Genome**: This pipeline assumes you are working with hg38 build of the human genome (latest build as of 3/5/2016). For the purposes of this pipeline, I used bowtie. However, you can substitue another aligner as long as the input accepts FASTA files and the output is in SAM format.

## Pipeline
In order to make a full CNV table from the provided CRISPR `crispr_guide_data_mac.tsv` file, use the following pipeline:

1. **PC to MAC conversion**: This pipeline also assumes all of the files are in mac/unix format. This means you must convert any non-mac formatted files before running. To do this, use the command:

	```
	tr '\r' '\n' < oldfilename > newfilename
	```

2. **Create FASTA file**: In order to create a FASTA file from the guide sequences, use `TSV_to_FASTA.py`. In the dataset provided, use the following command:

	```
	python TSV_to_FASTA.py -i data/crispr_guide_data_mac.tsv -o data/guide_sequences.fa
	```

3. **Align FASTA file**: Aligning the FASTA file allows you to determine location of all guide sequences. You may have your own aligner for this step. I used bowtie and hg38 build with the following parameters:

	```
	bowtie -f -S ~/genomes/hg38/hg38 guide_sequences.fa guide_sequences.sam
	```

4. **Create CNV table**: Creating the tab-separated CNV table required four input files:

	1. Aligned Guide Sequences SAM file
	2. A375 Copy Number Variation .csv file
	3. The original `crispr_guide_data.tsv` (MAC/Unix converted)
	4. Off-target scores in .tsv format, found in [Shalem et al. 2014](http://www.ncbi.nlm.nih.gov/pubmed/24336571) Supplementary Table 1.

Once created, the user can further analyze the CNV table using the provided R code as well as custom analyses in R, Python, or Excel. An example command code to run this script: 

	```
	python make_CNV_table.py -s data/guide_sequences.sam -c data/A375_CNV.csv -g data/crispr_guide_data_mac.tsv -t data/Shalem_2014Table_S1.tsv -o data/CNV_guide_table.tsv 
	```

