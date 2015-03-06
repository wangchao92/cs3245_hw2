This is the README file for A0078774L’s and A0110546R's submission

== General Notes about this assignment ==

The IGNORE_STOPWORDS option at the top of index.py may be changed so as to ignore stopwords when indexing.

When indexing the documents, the character '.' was used as the token for the universal set of documents.

Stemming of words and converting them to lowercase is done before any indexing or querying process.

Pickle is used to save both dictionary.txt and postings.txt.
The dictionary file stores the start and end pointers of each term in the postings file.
The pointers are then used to extract the respective pickled postings list data from the file.

The Shunting-yard algorithm as well as reverse polish notation were used to process the query strings.

a AND NOT b sub-queries were optimised to avoid taking the complement of b. This is done by iterating over a and discarding elements that were found in b.

De Morgan’s law was used to convert sub-queries like NOT a AND NOT b to NOT (a OR b) as well as NOT a OR NOT b to NOT(a AND b). This optimisation performs a single complement of an intermediate posting list instead of taking the likely large complement of both postings lists.

The program can also execute queries with nested parentheses.

== Files included with this submission ==

index.py
Program that indexes documents.

search.py
Program that queries index.

dictionary.txt
Dictionary that stores pointers to each postings list.

postings.txt
Postings lists.

ESSAY.txt
Answers to essay questions.

README.txt
This file.

== Statement of individual work ==

[I] I, A0078774L, certify that I have followed the CS 3245 Information
Retrieval class guidelines for homework assignments.  In particular, I
expressly vow that I have followed the Facebook rule in discussing
with others in doing the assignment and did not take notes (digital or
printed) from the discussions.

[I] I, A0110546R, certify that I have followed the CS 3245 Information
Retrieval class guidelines for homework assignments.  In particular, I
expressly vow that I have followed the Facebook rule in discussing
with others in doing the assignment and did not take notes (digital or
printed) from the discussions.

== References ==

IVLE forum


