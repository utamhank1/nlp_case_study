# Import libaries.
import argparse
import os
import sys

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


if __name__ == "__main__":
    main()
