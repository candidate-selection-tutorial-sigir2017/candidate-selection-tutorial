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
    document = {}
    for idx, field in enumerate(INDEX_MAP):
        if field.lower() == 'id':
            document[field.lower()] = record[idx]
        else:
            document["_news_%s" % (field.lower())] = record[idx].lower()
    return document


def index(input_file, num_records):
    """
    Creates a representation of the document and puts the document
    in the solr index. The index name is defined as a part of the url.
    """

    # create the solr core
    call(["./../../resources/solr-6.6.0/bin/solr", "create", "-c", INDEX_NAME])

    solr_interface = pysolr.Solr(url="%s/%s" % (SOLR_URL, INDEX_NAME))
    with open(input_file) as csvfile:
        records = csv.reader(csvfile, delimiter=b'\t')
        batched_documents = []
        for idx, record in enumerate(records):
            if idx == num_records:
                break
            if idx % 5000 == 0:
                solr_interface.add(batched_documents)
                batched_documents = []
                print 'Added %d documents to the %s index' % (idx, INDEX_NAME)
            batched_documents.append(create_document(record))
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