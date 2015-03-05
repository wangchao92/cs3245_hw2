import argparse
import nltk
import os
import pickle
import string

PUNCTUATION = set(string.punctuation)


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
    doc_file_names = os.listdir(directory_path)
    doc_file_names.sort(key=int)

    stemmer = nltk.stem.porter.PorterStemmer()

    postings_lists = {}

    for doc_file_name in doc_file_names:
        doc_file_path = os.path.join(directory_path, doc_file_name)
        doc = open(doc_file_path, 'r')

        seen_terms = set()

        for line in doc:
            tokens = nltk.word_tokenize(line)
            terms = [stemmer.stem(token.lower())
                      for token in tokens if token not in PUNCTUATION]

            for term in terms:
                if term not in seen_terms:
                    seen_terms.add(term)

                    if term not in postings_lists:
                        postings_lists[term] = []

                    postings_lists[term].append(doc_file_name)

        doc.close()

    ptr_dictionary = {}

    postings_file = open(postings_file_name, 'w')

    for term, postings_list in postings_lists.iteritems():
        start_ptr = postings_file.tell()

        postings_list = pickle.dumps(postings_list)
        postings_file.write(postings_list)

        end_ptr = postings_file.tell()

        ptr_dictionary[term] = (start_ptr, end_ptr)

    postings_file.close()

    copy_postings_lists = {}
    with open(postings_file_name, 'r') as postings_file:
        for term, (start_ptr, end_ptr) in ptr_dictionary.iteritems():
            postings_file.seek(start_ptr)

            postings_list = postings_file.read(end_ptr - start_ptr)
            postings_list = pickle.loads(postings_list)

            copy_postings_lists[term] = postings_list

    for term, postings_list in postings_lists.iteritems():
        print term, postings_lists[term]
        print term, copy_postings_lists[term]

    with open(dictionary_file_name, 'w') as dictionary_file:
        pickle.dump(ptr_dictionary, dictionary_file)

if __name__ == '__main__':
    build_index()
