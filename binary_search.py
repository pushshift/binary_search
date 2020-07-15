#!/usr/bin/env python3

import sys
import time
import numpy as np
import logging
import psycopg2
import os
logging.basicConfig(level=logging.INFO)


fh = open("authors.dat", "rb")
FILE_SIZE = os.path.getsize("authors.dat")
RECORD_SIZE = 44

def fetch_record(pos):
    '''Fetch a specific record'''
    file_position = pos * RECORD_SIZE
    fh.seek(file_position)
    data = fh.read(RECORD_SIZE)
    record = {}
    record['author'] = data[0:32].replace(b'\0',b'').decode()
    record['id'] = int.from_bytes(data[32:40], byteorder='little')
    record['created_utc'] = int.from_bytes(data[40:], byteorder='little')
    return record


def search_record(author):
    '''Returns record position if there is a match. Otherwise, returns False.'''
    total_seeks = 0
    author = author.lower()
    NUM_RECORDS = FILE_SIZE / RECORD_SIZE
    record_pos = int(NUM_RECORDS / 2)
    r_bound = NUM_RECORDS
    l_bound = 0

    while True:
        total_seeks += 1
        if total_seeks > 250:
            logging.debug("Maximum seeks circuit-breaker. There is probably an issue with the search logic.")
            return False
        pos = record_pos * RECORD_SIZE
        fh.seek(pos)
        record = fh.read(RECORD_SIZE)
        r_author = record[0:32].replace(b'\0',b'').decode().lower()
        if author == r_author:
            logging.debug(f"Found author at record position: {record_pos}.")
            return record_pos
        elif author > r_author:
            logging.debug(f"Match {r_author} is too small. Seeking...")
            l_bound = record_pos
            record_pos = int((record_pos + r_bound) / 2)
            if record_pos == l_bound:
                logging.info("Boundary hit. Stopping.")
                return False
        elif author < r_author:
            logging.debug(f"Match {r_author} is too large. Seeking...")
            r_bound = record_pos
            record_pos = int((record_pos + l_bound) / 2)
            if record_pos == r_bound:
                logging.debug("Boundary hit. Stopping.")
                return False


author = "stuck_in_the_matrix"
record_pos = search_record(author)
if record_pos:
    data = fetch_record(record_pos)
    print(data)
