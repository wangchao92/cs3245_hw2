import argparse
import nltk
import os
import sys
import string
import extsort

PUNCTUATION = set(string.punctuation)

def main():
  # parser = argparse.ArgumentParser(prog='CS3245 HW2', description='CS3245 HW2')
  # parser.add_argument('-i', required=True, help='directory-of-documents')
  # parser.add_argument('-d', required=True, help='dictionary-file')
  # parser.add_argument('-p', required=True, help='postings-file')

  # args = parser.parse_args()
  # directory_path = args.i
  # dictionary_file_name = args.d
  # postings_file_name = args.p

  directory_path = 'test'
  dictionary_file_name = 'dictionary.txt'
  postings_file_name = 'postings.txt'

  stemmer = nltk.stem.porter.PorterStemmer()

  token_id = 0
  dictionary = {}

  out_file = open('tuples.txt', 'w')

  for doc_id in os.listdir(directory_path):
    doc_path = os.path.join(directory_path, doc_id)
    seen_tokens = set()

    with open(doc_path, 'r') as f:
      for line in f:
        tokens = nltk.word_tokenize(line)
        tokens = [token for token in tokens if token not in PUNCTUATION]
        tokens = [stemmer.stem(token.lower()) for token in tokens]

        for token in tokens:
          if token not in seen_tokens:
            seen_tokens.add(token)

            if token not in dictionary:
              dictionary[token] = token_id
              token_id += 1

            out_file.write(str(dictionary[token]))
            out_file.write(' ')
            out_file.write(doc_id)
            out_file.write(' ')
            out_file.write(token)
            out_file.write('\n')

  out_file.close()

  sorter = extsort.ExternalSort(extsort.parse_memory('100M'))
  sorter.sort('tuples.txt')

if __name__ == '__main__':
  main()
