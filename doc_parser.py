# Import libraries.
import argparse
import os
import sys
import pandas as pd
import helpers


def parse_arguments():
    # Infrastructure to set up command line argument parser.
    parser = argparse.ArgumentParser(description='Enter the directory containing the .txt files you wish to analyze'
                                                 'as well as the number of interesting words you would like to observe'
                                                 'DIRECTORY MUST NOT CONTAIN ANY SPACES IN FOLDER NAMES')
    parser.add_argument("-d", "--directory", type=str, help='Path to the directory containing the .txt files'
                                                            'DIRECTORY MUST NOT CONTAIN ANY SPACES IN FOLDER NAMES')
    parser.add_argument("-n", "--number_words", type=int, help='Number of interesting words and their associated '
                                                               'sentences that  you would like parsed '
                                                               'must be less than 100)')

    args = parser.parse_args()
    directory = args.directory
    N = args.number_words

    # Input validation for N
    if N > 100:
        print('Please enter a number of words that is less than 100.')
        sys.exit()

    # Input validation for directory.
    if not os.path.isdir(directory):
        print('The path specified does not exist.')
        sys.exit()

    return directory, N


def main(directory, N):
    print(f"The path to the file directory specified is {directory} with an N value of {N}.")
    print('----------------------------------------------------------------------------------------------------------')

    # Read in multiple files from directory with glob utility.
    name_map, all_data = helpers.globber(directory=directory)

    # Create frequency table as a python dict to analyze all_data and determine the frequency of every word.
    freq_df = helpers.frequencyCounter(data=all_data)

    # Eliminate stop words from frequency table.
    freq_df = helpers.stopWordRemover(file='stop-word-list.csv', frequency_table=freq_df)

    # Convert all_data from a list to a pandas dataframe.
    all_data = pd.DataFrame(all_data, columns=['text'])

    # Merge the name_map that holds all of the truncated names of the documents and the strings of the parsed documents
    # in all_data to form a comprehensive all_data pandas dataframe.
    all_data = name_map.join(all_data)

    # Create split_sentences data structure to hold every document and every sentence the document contains.
    split_sentences = helpers.sentenceSplitter(data=all_data)

    # Output configuration.
    output = helpers.outputConstructor(freq_df=freq_df, split_sentences=split_sentences, data=all_data, n=N)

    # Extract output to .csv file in the specified directory.
    output.to_csv('output.csv')


if __name__ == "__main__":
    arguments = parse_arguments()
    main(*arguments)
