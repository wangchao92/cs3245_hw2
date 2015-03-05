import argparse
import math
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

    execute_queries(
        dictionary_file_name, postings_file_name, query_file_name, output_file_name)


def execute_queries(dictionary_file_name='dictionary.txt', postings_file_name='postings.txt', query_file_name='query.txt', output_file_name='output.txt'):
    ptr_dictionary = None
    with open(dictionary_file_name, 'r') as dictionary_file:
        ptr_dictionary = pickle.load(dictionary_file)

    postings_file = open(postings_file_name, 'r')

    global universal_set
    start_ptr, end_ptr = ptr_dictionary['.']
    universal_set = postings_file.read(end_ptr - start_ptr)
    universal_set = pickle.loads(universal_set)

    global total_count
    total_count = len(universal_set)

    query_file = open(query_file_name, 'r')

    for line in query_file:
        pass

    query_file.close()

    postings_file.close()


def negate(postings_list):
    result = [
        doc_id for doc_id in universal_set if doc_id not in set(postings_list)]

    return result


def intersect(list_a, list_b, negate_a=False, negate_b=False):
    # Optimise
    if negate_a:
        list_a = negate(list_a)

    if negate_b:
        list_b = negate(list_b)

    sqrt_a = int(math.sqrt(len(list_a)))
    sqrt_b = int(math.sqrt(len(list_b)))

    result = []
    i = j = 0
    while i < len(list_a) and j < len(list_b):
        if list_a[i] == list_b[j]:
            result.append(list_a[i])
            i += 1
            j += 1
        elif list_a[i] > list_b[j]:
            if j % sqrt_b == 0 and j + sqrt_b < len(list_b) and list_a[i] >= list_b[j + sqrt_b]:
                j += sqrt_b
            else:
                j += 1
        else:
            if i % sqrt_a == 0 and i + sqrt_a < len(list_a) and list_a[i + sqrt_a] <= list_b[j]:
                i += sqrt_a
            else:
                i += 1

    return result


def union(list_a, list_b, negate_a=False, negate_b=False):
    # Optimise
    if negate_a:
        list_a = negate(list_a)

    if negate_b:
        list_b = negate(list_b)

    result = []
    i = j = 0
    while i < len(list_a) and j < len(list_b):
        if list_a[i] == list_b[j]:
            result.append(list_a[i])
            i += 1
            j += 1
        elif list_a[i] > list_b[j]:
            result.append(list_b[j])
            j += 1
        else:
            result.append(list_a[i])
            i += 1

    if i < len(list_a):
        result.extend(list_a[i:])

    if j < len(list_b):
        result.extend(list_b[j:])

    return result

if __name__ == '__main__':
    print intersect(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10'], ['1', '4', '9', '10'])

    print union(['0', '2', '4', '6', '7', '8', '9', '10'], ['0', '1', '2', '3', '4', '5', '6'])
