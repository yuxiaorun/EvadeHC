import json
import re

import sys
import os
import glob

SAMPLE_PATH = "mal/"
class FileRetrievalFailure(Exception):
    pass

def fetch_file(sha256):
    location = os.path.join(SAMPLE_PATH, sha256)
    try:
        with open(location, 'rb') as infile:
            bytez = infile.read()
    except IOError:
        raise FileRetrievalFailure(
            "Unable to read sha256 from {}".format(location))

    return bytez


def get_available_sha256():
    sha256list = []
    for fp in glob.glob(os.path.join(SAMPLE_PATH, '*')):
        fn = os.path.split(fp)[-1]
        result = re.match(r'^[0-9a-fA-F]{64}$', fn) # require filenames to be sha256
        sha256list.append(fn)
    assert len(sha256list)>0, "no files found in {} with sha256 names".format( SAMPLE_PATH )

    return sha256list

index=0
batch_size=20
def get_bytes_batch():
    data=[]
    shalist=get_available_sha256()
    global index
    print(shalist[0])
    if index >= len(shalist) / batch_size:
        batch = shalist[len(shalist) * index:]
        index=0
    else:
        batch=shalist[len(shalist)*index:len(shalist)*(index+1)]
        index+=1

    for i in shalist:
        data.append(fetch_file(i))

    return data

