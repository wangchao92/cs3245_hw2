import argparse
import nltk
import pickle
import string

PUNCTUATION = set(string.punctuation)


def main():
    parser = argparse.ArgumentParser(
        prog='CS3245 HW2', description='CS3245 HW2')
    parser.add_argument('-d', required=True, help='dictionary-file')
    parser.add_argument('-p', required=True, help='postings-file')
    parser.add_argument('-q', required=True, help='file-of-queries')
    parser.add_argument('-o', required=True, help='output-file-of-results')

    args = parser.parse_args()
    dictionary_file_name = args.d
    postings_file_name = args.p
    query_file_name = args.q
    output_file_name = args.o

    execute_queries(dictionary_file_name, postings_file_name, query_file_name, output_file_name)


def execute_queries(dictionary_file_name='dictionary.txt', postings_file_name='postings.txt', query_file_name='query.txt', output_file_name='output.txt'):
    ptr_dictionary = None
    with open(dictionary_file_name, 'r') as dictionary_file:
        ptr_dictionary = pickle.load(dictionary_file)

    query_file = open(query_file_name, 'r')

    for query in query_file:
        pass

    query_file.close()

if __name__ == '__main__':
    execute_queries()
