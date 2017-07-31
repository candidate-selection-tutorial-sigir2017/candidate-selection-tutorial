from __future__ import unicode_literals

from subprocess import call
import argparse
import csv
import pysolr

INDEX_NAME = 'simpleindex'
INDEX_MAP = ["ID", "TITLE", "URL", "PUBLISHER", "CATEGORY", "STORY", "HOSTNAME", "TIMESTAMP"]
SOLR_URL = 'http://localhost:8983/solr'


def create_document(record):
    """
    This function creates a representation for the document to be
    put in the solr index.
    """
    # TODO: Write an iterator over the INDEX_MAP to fetch fields from the record and
    # return a dictionary representing the document.
    return None


def index(input_file, num_records):
    """
    Creates a representation of the document and puts the document
    in the solr index. The index name is defined as a part of the url.
    """
    solr_interface = pysolr.Solr(url="%s/%s" % (SOLR_URL, INDEX_NAME))
    with open(input_file) as csvfile:
        records = csv.reader(csvfile, delimiter=b'\t')
        batched_documents = []
        for idx, record in enumerate(records):
            if idx == num_records:
                break
            # TODO: Write code for creating the document and passing it for indexing
    # Commit the changes to the index after adding the documents
    solr_interface.commit()
    print 'Finished adding the documents to the solr index'
    return


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--input', action='store', dest='input', )
    arg_parser.add_argument('--num_records', action='store', dest='num_records', default=250000)
    args = arg_parser.parse_args()
    index(input_file=args.input, num_records=args.num_records)

if __name__ == '__main__':
    main()