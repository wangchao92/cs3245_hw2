import argparse
import nltk
import os
import pickle
import string

PUNCTUATION = set(string.punctuation)
UNIVERSAL_SET_KEY = '.'


def main():
    parser = argparse.ArgumentParser(
        prog='CS3245 HW2', description='CS3245 HW2')
    parser.add_argument('-i', required=True, help='directory-of-documents')
    parser.add_argument('-d', required=True, help='dictionary-file')
    parser.add_argument('-p', required=True, help='postings-file')

    args = parser.parse_args()
    directory_path = args.i
    dictionary_file_name = args.d
    postings_file_name = args.p

    build_index(directory_path, dictionary_file_name, postings_file_name)


def build_index(directory_path='test', dictionary_file_name='dictionary.txt', postings_file_name='postings.txt'):
    # Sort file names numerically, not lexicographically
    doc_file_names = os.listdir(directory_path)
    doc_file_names.sort(key=int)

    stemmer = nltk.stem.porter.PorterStemmer()

    postings_lists = {}
    postings_lists[UNIVERSAL_SET_KEY] = []

    # Build postings lists; treat doc file names as doc ids
    for doc_file_name in doc_file_names:
        doc_file_path = os.path.join(directory_path, doc_file_name)
        doc = open(doc_file_path, 'r')

        # Add doc id to universal set
        postings_lists[UNIVERSAL_SET_KEY].append(int(doc_file_name))

        seen_terms = set()

        for line in doc:
            tokens = nltk.word_tokenize(line)

            # terms is an array of stemmed lowercase tokens that are not
            # punctuation
            terms = [stemmer.stem(token.lower())
                     for token in tokens if token not in PUNCTUATION]

            for term in terms:
                # Avoid duplicate doc ids for the same term
                if term not in seen_terms:
                    seen_terms.add(term)

                    # Initialise postings list for new term
                    if term not in postings_lists:
                        postings_lists[term] = []

                    # Add doc id to postings list
                    postings_lists[term].append(int(doc_file_name))

        doc.close()

    # Stores start/end pointers to postings list within postings file
    # To be written to the dictionary file
    ptr_dictionary = {}

    # Stores postings lists
    postings_file = open(postings_file_name, 'w')

    # Write postings lists to file, storing start/end pointers
    for term, postings_list in postings_lists.iteritems():
        start_ptr = postings_file.tell()

        postings_list = pickle.dumps(postings_list)
        postings_file.write(postings_list)

        end_ptr = postings_file.tell()

        ptr_dictionary[term] = (start_ptr, end_ptr)

    postings_file.close()

    # Write dictionary to file
    with open(dictionary_file_name, 'w') as dictionary_file:
        pickle.dump(ptr_dictionary, dictionary_file)

if __name__ == '__main__':
    build_index()
    # main()
