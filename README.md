# Binary Search implementation using Python

This code gives an example of implementing binary search using Python. This is a bare-bones example of how to implement a binary search using sorted data (Reddit Authors). Each record is 44 bytes and consists of three fields -- author name, id and the author creation time (epoch).

- The first field is author and is 32 bytes in size. The author name is null padded.
- The second field is the id of the author and is an 8 byte integer.
- The third field is the author creation time (in epoch seconds) and is a 4 byte integer.

There are two methods in binary_search.py.

- The search_record method returns the record position if a match is found or returns False if no match is found.
- The fetch_record method fetches a record from authors.dat

This code could be further optimized by including a cache for the search and fetch methods.

You will need to download the authors.dat file from https://files.pushshift.io/reddit/authors.dat.zst. When you download the file, decompress the file and put it in the same directory as the binary_search.py script.

