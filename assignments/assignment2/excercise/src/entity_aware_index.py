from __future__ import unicode_literals
from itertools import izip
import argparse
import json
import csv
import pysolr
import gzip

INDEX_NAME = 'entityawareindex'
INDEX_MAP = ["ID", "TITLE", "URL", "PUBLISHER", "CATEGORY", "STORY", "HOSTNAME", "TIMESTAMP"]
SOLR_URL = 'http://localhost:8983/solr'

# Location, Time, Person, Organization, Money, Percent, Date (Stanford NER)

def create_document(record, ner_tags):
    """
    This function creates a representation for the document to be
    put in the solr index.
    """
    # TODO: Write an iterator over the INDEX_MAP to fetch fields from the record and
    # return a dictionary representing the document.
    return None


def index(input_file, ner_tags_filename, num_records):
    """
    Creates a representation of the document and puts the document
    in the solr index. The index name is defined as a part of the url.
    """

    solr_interface = pysolr.Solr(url="%s/%s" % (SOLR_URL, INDEX_NAME))
    with open(input_file) as csvfile, gzip.open(ner_tags_filename) as ner_tags_file:
        records = csv.reader(csvfile, delimiter=b'\t')
        ner_tags = csv.reader(ner_tags_file, delimiter=b'\t')
        batched_documents = []
        for idx, (record, ner_tag_serialized) in enumerate(izip(records, ner_tags)):
            if idx == num_records:
                break
            # ner_tag is a dictionary of the form {"ORGANIZATION": ["Omega", "PayPal", "CNBC"], "PERSON": ["Cooperman"]}
            ner_tag = json.loads(ner_tag_serialized[1])
            # TODO: Write code for creating the document and passing it for indexing
    # Commit the changes to the index after adding the documents
    solr_interface.commit()
    print 'Finished adding the documents to the solr index'
    return


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--input', action='store', dest='input', )
    arg_parser.add_argument('--ner_tags', action='store', dest='ner_tags', )
    arg_parser.add_argument('--num_records', action='store', dest='num_records', default=250000)
    args = arg_parser.parse_args()
    index(input_file=args.input, ner_tags_filename=args.ner_tags, num_records=args.num_records)

if __name__ == '__main__':
    main()