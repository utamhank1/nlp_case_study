# nlp_case_study
Repository to hold files for preliminary nlp data processing of various .txt documents.

# Requirements:
The following python 3.7 modules are used in the execution of this file, non-standard library packages are bolded and version number is given:

python 3.7
argparse
os
sys
glob
pandas (1.0.2)
collections
re
csv
string
numpy (1.18.1)
The requirements.txt file contains the two non-standard library python modules that need to be installed into the virtual environment. 

2.	You must have a directory of plain text files that you wish to analyze, the path to this directory cannot contain any spaces or special characters.

3.	You must have the following .csv file present in your working directory (NOT the directory which contains the text files to analyze!)
stop-word-list.csv
Launching the program:

# Launching the Program:

Enter the following into the command line:
python doc_parser.py -d [YOUR DIRECTORY] -n [YOUR NUMBER]
Inputs: 
	There are two user-supplied inputs to the program doc_parser.py:
-d [directory]: This is the path to the directory which contains the list of .txt files that you want to analyze, it cannot contain any spaces or special characters.
-n [number]: This is an integer number that specifies the length of the output.csv file in regards to the number of interesting words that the user desires to see the occurrences and sentences for; for example: if you want to see the top 25 most frequently occurring interesting words, enter 25. This number must be less than 100.

#Output:
	There will be an output.csv file that will be parsed into the working directory with the following format: 
