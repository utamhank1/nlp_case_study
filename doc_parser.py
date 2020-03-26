# Import libaries.
import argparse
import os
import sys
import glob
import pandas as pd
import collections
from collections import Counter
import re
import csv
import string
import numpy as np

# Infrastructure to set up command line argument parser.
parser = argparse.ArgumentParser(description='Enter the directory containing the .txt files you wish to analyze'
                                             'as well as the number of interesting words you would like to observe'
                                             'DIRECTORY MUST NOT CONTAIN ANY SPACES IN FOLDER NAMES')
parser.add_argument("-d", "--directory", type=str, help='Path to the directory containing the .txt files'
                                                        'DIRECTORY MUST NOT CONTAIN ANY SPACES IN FOLDER NAMES')
parser.add_argument("-n", "--number_words", type=int, help='Number of interesting words you would like parsed'
                                                           'ranked by popularity, must be less than 100)')

args = parser.parse_args()
directory = args.directory
N = args.number_words

# Input validation for directory.
if not os.path.isdir(directory):
    print('The path specified does not exist')
    sys.exit()


def main():
    print(f"The directory specified is {directory} with an N value of {N}.")
    # Load English tokenizer, tagger, parser, NER and word vectors
    # nlp = English()

    # Read in multiple files from directory with glob utility.
    file_names = glob.glob(directory + '/*txt')

    # Empty list to eventually hold strings of all data parsed from .txt files.
    all_data = []
    name_map = pd.DataFrame(file_names, columns=['file_names'])

    # Open every .txt file and save it as a string in an element of the list called all_data.
    index = 0

    # Iterate over every file name and read in the corresponding file. Save it as a string and create a list called
    # all_data that holds the strings from each file.
    for name in file_names:
        with open(name, 'r', encoding='utf8') as file:
            all_data.append(file.read().replace('\n', ''))
            # Get only the document name portion from the file path.
            name_split = name.split('\\')
            # Load the document name into name_map.
            name_map['file_names'][index] = name_split[-1]
            index = index + 1

    # Create frequency table as a python dict to analyze all_data and determine the frequency of every word.
    freq_table = Counter(re.sub(r'[1234567890,.;@#?!&$\-"]+\ *', ' ', ' '.join(all_data)).split())

    # Convert frequency table to pandas dataframe to enable easier sorting.
    freq_df = pd.DataFrame.from_dict(freq_table, columns=['frequency'], orient='index')
    # Sort word frequency values by descending order.
    freq_df = freq_df.sort_values(by='frequency', ascending=False)
    # Add index column.
    freq_df = freq_df.reset_index()
    # Rename old index column to 'word'.
    freq_df = freq_df.rename(columns={'index': 'word'})

    # Eliminate stop words from frequency table.
    # Import list of stopwords.
    with open('stop-word-list.csv', newline='') as csv_file:
        stop_data = csv.reader(csv_file, delimiter=',')
        stop_words = list(stop_data)
    stop_words = stop_words[0]

    # Strip spaces out of stop words list.
    stop_words = [word.strip(' ') for word in stop_words]
    # Preallocate list of stop words with first letter capitalized.
    stop_words_caps = [0] * len(stop_words)

    # Capitalize every first letter in stop words and merge the two lists of stop_words.
    for i in range(0, len(stop_words)):
        stop_words_caps[i] = string.capwords(stop_words[i])
    stop_words_all = stop_words + stop_words_caps

    # Iterate over stop_words_all and find any matches in the frequency table, if a match is found, replace that
    # word with a nan value (to be deleted later).
    for word in stop_words_all:
        for i in range(0, len(freq_df)):
            if word == freq_df['word'][i]:
                freq_df['word'][i] = np.nan

    # Drop rows containing nan from the freq_df dataframe, reset the index.
    freq_df = freq_df.dropna()
    freq_df = freq_df.reset_index(drop=True)

    # Convert all_data from a list to a pandas dataframe.
    all_data = pd.DataFrame(all_data, columns=['text'])

    # Merge the name_map that holds all of the truncated names of the documents and the strings of the parsed documents
    # in all_data to form a comprehensive all_data pandas dataframe.
    all_data = name_map.join(all_data)


if __name__ == "__main__":
    main()
