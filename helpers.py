# Import libraries.
from collections import Counter
import re
import csv
import string
import numpy as np
import glob
import pandas as pd


# Helper function to match word occurrences in a string.
def findWholeWord(w):
    """
    This function takes in a string w and outputs a match object if there is a word w in a block of text, outputs
    None if there is not.
    :param w: string
    :return: match object or None
    """
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search


# Read in multiple files from directory with glob utility.
def globber(directory):
    """
    This function takes in a directory name and outputs a pandas dataframe of filenames and a pandas dataframe of
     each file and all associated text from that file.
    :param directory: string
    :return: pandas dataframe (columns = 'file_names'), pandas dataframe (columns = 'file_names', 'text')
    """
    file_names = glob.glob(directory + '/*txt')

    # Empty list to eventually hold strings of all data parsed from .txt files.
    all_data = []
    name_map = pd.DataFrame(file_names, columns=['file_names'])

    # Iterate over every file name and read in the corresponding file. Save it as a string and create a list called
    # all_data that holds the strings from each file.
    index = 0
    for name in file_names:
        with open(name, 'r', encoding='utf8') as file:
            all_data.append(file.read().replace('\n', ''))
            # Get only the document name portion from the file path.
            name_split = name.split('\\')
            # Load the document name into name_map.
            name_map['file_names'][index] = name_split[-1]
            index = index + 1

    return name_map, all_data


def frequencyCounter(data):
    """
    This function takes in a pandas dataframe that contains columns 'file_names' and 'text' and outputs a dataframe
    freq_df that includes a list of every word in the text and the associated frequency count of that word.
    :param data: pandas dataframe (columns = 'file_names', 'text')
    :return: pandas dataframe (columns = 'word', 'frequency')
    """
    freq_table = Counter(re.sub(r'[1234567890,.;@#?!&$\-"]+\ *', ' ', ' '.join(data)).split())

    # Convert frequency table to pandas dataframe to enable easier sorting.
    freq_df = pd.DataFrame.from_dict(freq_table, columns=['frequency'], orient='index')
    # Sort word frequency values by descending order, add index column, rename index column to 'word'.
    freq_df = freq_df.sort_values(by='frequency', ascending=False).reset_index().rename(columns={'index': 'word'})

    return freq_df


def stopWordRemover(file, frequency_table):
    """
    This function takes in a filename for a .csv file of all stop words and a pandas dataframe of the unfiltered
    frequency table of words and removes all of the stop words from the frequency table. Output is a frequency table
    without stop words.
    :param file: string
    :param frequency_table: pandas dataframe (columns = 'word', 'frequency')
    :return: pandas dataframe (columns = 'word', 'frequency')
    """
    # Import list of stopwords.
    with open(file, newline='') as csv_file:
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
        for i in range(0, len(frequency_table)):
            if word == frequency_table['word'][i]:
                frequency_table['word'][i] = np.nan

    # Drop rows containing nan from the freq_df dataframe, reset the index.
    freq_df = frequency_table.dropna().reset_index(drop=True)

    return freq_df


def sentenceSplitter(data):
    """
    This function takes in a pandas dataframe 'data' and outputs a pandas dataframe of every sentence in ever document
    with the associated document number
    :param data: pandas dataframe (columns = 'file_names', 'text')
    :return: pandas dataframe (columns = 'document_number', 'sentence')
    """

    split_sentences = pd.DataFrame(columns=['document_number', 'sentence'])
    # create docDict intermediate python dictionary data structure to hold every document number and a list of
    # sentences from that document.
    docDict = {}
    for i in range(0, len(data)):
        docDict["{0}".format(i)] = re.split('(?<=[\.\?\!])\s*', data['text'][i])

    # Create pandas dataframe from the docDict dictionary to hold the document number and every sentence.
    k = 0
    for i in range(0, len(docDict)):
        for j in range(0, len(docDict[f"{i}"])):
            split_sentences.loc[k] = i, docDict[f"{i}"][j]
            k = k + 1

    return split_sentences


def outputConstructor(freq_df, split_sentences, data, n):
    """
    Constructs the output table and takes in the pandas dataframes for frequency table, text, N user set value,
    and returns the output table.
    :param freq_df: pandas dataframe (columns = 'word', 'frequency')
    :param split_sentences: pandas dataframe (columns = 'document_number', 'sentence')
    :param data: pandas dataframe (columns = 'file_names', 'text')
    :param n: integer
    :return: pandas dataframe (columns = 'word', 'frequency', 'document_names', 'sentences')
    """
    # Output configuration.
    output = pd.DataFrame(freq_df[['word', 'frequency']][0:n], columns=['word', 'frequency', 'document_names',
                                                                        'sentences'])
    # For loop that iterates from 0 to the user specified N value (representing the number of desired interesting words
    # to scan detect, and parse sentences for and constructs the output data structure by pulling relevant columns and
    # entries from the freq_df, split_sentences, and all_data data structures.
    for i in range(0, n):
        sentences = []
        document_names = []
        for j in range(0, len(split_sentences)):
            # Use helper function to look for matches between the words in freq_df and split_sentences.
            if findWholeWord(freq_df['word'][i].lower())(split_sentences['sentence'][j].lower()) is not None:
                # If match is found, add that document name and that sentence to the list of document numbers and
                # sentences for that word.
                document_names.append(data['file_names'][split_sentences['document_number'][j]])
                sentences.append(split_sentences['sentence'][j])

        # Find all unique entries in the set of all document names containing that word and all unique sentences
        # containing that word, parse them to a list, and load them into that row of the output data structure.
        output['document_names'][i] = list(set(document_names))
        output['sentences'][i] = list(set(sentences))

    return output
