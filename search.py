import argparse
import math
import nltk
import pickle
import string

PUNCTUATION = set(string.punctuation)
UNIVERSAL_SET_KEY = '.'
NULL_SET_KEY = ','
NOT_PREFIX = 'N_'
OR_PREFIX = 'O_'
AND_PREFIX = 'A_'


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
    global ptr_dictionary
    ptr_dictionary = None
    with open(dictionary_file_name, 'r') as dictionary_file:
        ptr_dictionary = pickle.load(dictionary_file)

    global postings_file
    postings_file = open(postings_file_name, 'r')

    global universal_set
    universal_set = read_postings_list(UNIVERSAL_SET_KEY)

    global total_count
    total_count = len(universal_set)

    global results
    results = {}

    query_file = open(query_file_name, 'r')

    for line in query_file:
        results = {} # Clears the intermediate results, in case of conflicts.
        print(line)
        print(apply_RPN(toRPN(line)))

    query_file.close()

    postings_file.close()


def negate(postings_list):
    result = [
        doc_id for doc_id in universal_set if doc_id not in set(postings_list)]

    return result


def intersect(list_a, list_b, negate_a=False, negate_b=False):
    result = []

    if negate_a and negate_b:
        return negate(union(list_a, list_b))
    elif negate_a is not negate_b:
        if negate_a:
            list_a, list_b = list_b, list_a

        j = 0
        for doc_id in list_a:
            # Iterate over list_b until we find an equal or greater element
            while j < len(list_b) and doc_id > list_b[j]:
                j += 1

            # Add doc_id if it is less than current list_b element, or we have reached the end of list_b
            if j == len(list_b) or doc_id < list_b[j]:
                result.append(doc_id)
    else:
        sqrt_a = int(math.sqrt(len(list_a)))
        sqrt_b = int(math.sqrt(len(list_b)))

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
    if negate_a and negate_b:
        return negate(intersect(list_a, list_b))

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

    while i < len(list_a):
        result.append(list_a[i])
        i += 1

    while j < len(list_b):
        result.append(list_b[j])
        j += 1

    return result

def toRPN(query):
    words = query.replace('(', ' ( ').replace(')', ' ) ').split() # "Spread" the parentheses.
    operator_stack = [] # Temporary operator stack.
    rpn = [] # Final reverse polish notation list.

    for word in words:
        if word == '(':
            operator_stack.append('(')

        elif word == ')': # Pop everything until a ) is found, then pop ).
            while len(operator_stack) != 0 and operator_stack[len(operator_stack) - 1] != '(':
                rpn.append(operator_stack.pop())

            if operator_stack[len(operator_stack) - 1] == '(':
                operator_stack.pop()

        elif word == 'NOT':
            operator_stack.append('NOT')

        elif word == 'AND': # Pop all NOTs before appending to operator stack.
            while len(operator_stack) != 0 and operator_stack[len(operator_stack) - 1] == 'NOT':
                rpn.append(operator_stack.pop())

            operator_stack.append('AND')

        elif word == 'OR': # Pop all NOTs and ANDs before appending to operator stack.
            while len(operator_stack) != 0 and (operator_stack[len(operator_stack) - 1] == 'NOT' or operator_stack[len(operator_stack) - 1] == 'AND'):
                rpn.append(operator_stack.pop())

            operator_stack.append('OR')

        else: # If it's a token, append to rpn.
            rpn.append(word.lower())

    while len(operator_stack) != 0: # Append remainder of operator stack to rpn.
        rpn.append(operator_stack.pop())

    return rpn

def apply_RPN(rpn):
    stack = [] # Stack of operands.
    result = [] # We will return this at the end of the method. 

    result = get_postings_list(rpn[0]) # Gets the posting list of the first operand.

    # For each element in the rpn...
    for i, element in enumerate(rpn):

        if element == 'NOT':
            a = stack.pop()

            if i == len(rpn) - 1: # Only negate operation if NOT is the last element.
                a_list = get_postings_list(a if a[0:2] != NOT_PREFIX else a[2:])
                result = negate(a_list)

            # Push the new key into the stack of operands.
            result_key = NOT_PREFIX + a
            stack.append(result_key)

        elif element == 'AND':
            a = stack.pop()
            b = stack.pop()

            # Get the postings list of the elements, stripping the NOT_PREFIX.
            a_list = get_postings_list(a if a[0:2] != NOT_PREFIX else a[2:])
            b_list = get_postings_list(b if b[0:2] != NOT_PREFIX else b[2:])

            # Intersection of a and b, and whether a or b are to be negated.
            result = intersect(a_list, b_list, a[0:2] == NOT_PREFIX, b[0:2] == NOT_PREFIX)

            # Push the new key into results and the stack of operands.
            result_key = AND_PREFIX + a + '_' + b
            results[result_key] = result
            stack.append(result_key)

        elif element == 'OR':
            a = stack.pop()
            b = stack.pop()

            # Get the postings list of the elements, stripping the NOT_PREFIX.
            a_list = get_postings_list(a if a[0:2] != NOT_PREFIX else a[2:])
            b_list = get_postings_list(b if b[0:2] != NOT_PREFIX else b[2:])

            # Union of a and b, and whether a or b are to be negated.
            result = union(a_list, b_list, a[0:2] == NOT_PREFIX, b[0:2] == NOT_PREFIX)

            # Push the new key into results and the stack of operands.
            result_key = OR_PREFIX + a + '_' + b
            results[result_key] = result
            stack.append(result_key)

        else:
            # Just append to the stack of operands.
            stack.append(element)

    return result


def get_postings_list(token):
    """
    Returns an existing, calculated result or
    reads from the postings file by the token.
    """
    if token in results:
        return results[token]
    else:
        return read_postings_list(token)


def read_postings_list(token):
    """
    Returns the entire postings list of a token.
    """
    if token not in ptr_dictionary:
        return []

    start_ptr, end_ptr = ptr_dictionary[token]
    postings_file.seek(start_ptr)
    postings_list_pickle = postings_file.read(end_ptr - start_ptr)
    postings_list = pickle.loads(postings_list_pickle)
    return postings_list


if __name__ == '__main__':
    # print intersect(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10'], ['1', '4', '9', '10'])

    # print union(['0', '2', '4', '6', '7', '8', '9', '10'], ['0', '1', '2', '3', '4', '5', '6'])
    # toRPN('bill OR Gates AND (vista OR XP) AND NOT mac')
    execute_queries()
