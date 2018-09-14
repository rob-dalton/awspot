import json
import typing

def read_response(fpath: str):
    """ Given path to JSON file of boto3 response, read JSON file. """
    with open(fpath, 'r') as f:
        return json.loads(f.read())
