from __future__ import unicode_literals

from subprocess import call
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

# Person, Norp (Nationalities or religious or political groups.), Facility, Org, GPE (Countries, cities, states.)
# Loc (Non GPE Locations ex. mountain ranges, water), Product (Objects, vehicles, foods, etc. (Not services.),
# EVENT (Named hurricanes, battles, wars, sports events, etc.), WORK_OF_ART (Titles of books, songs, etc), LANGUAGE
# Refer to https://spacy.io/docs/usage/entity-recognition (SPACY NER)


def create_document(record, ner_tags):
    """
    This function creates a representation for the document to be
    put in the solr index.
    """
    document = {}
    for idx, field in enumerate(INDEX_MAP):
        if field.lower() == 'id':
            document[field.lower()] = record[idx]
        elif field.lower() == 'title':
            for ner_tag, tokens in ner_tags.iteritems():
                # generate field like title_<ner_tag> ex. title_person, title_organization etc.
                document["_news_%s_%s" % (field.lower(), ner_tag.lower())] \
                    = " ".join(map(lambda x:x.lower(), tokens))
            document["_news_%s" % (field.lower())] = record[idx].lower()
        else:
            document["_news_%s" % (field.lower())] = record[idx].lower()
    return document


def index(input_file, ner_tags_filename, num_records):
    """
    Creates a representation of the document and puts the document
    in the solr index. The index name is defined as a part of the url.
    """

    # create the solr core
    call(["./../../resources/solr-6.6.0/bin/solr", "create", "-c", INDEX_NAME])

    solr_interface = pysolr.Solr(url="%s/%s" % (SOLR_URL, INDEX_NAME))
    with open(input_file) as csvfile, gzip.open(ner_tags_filename) as ner_tags_file:
        records = csv.reader(csvfile, delimiter=b'\t')
        ner_tags = csv.reader(ner_tags_file, delimiter=b'\t')
        batched_documents = []
        for idx, (record, ner_tag_serialized) in enumerate(izip(records, ner_tags)):
            if idx == num_records:
                break

            if len(record) != 8:
                continue

            if idx % 5000 == 0:
                solr_interface.add(batched_documents)
                batched_documents = []
                print 'Added %d documents to the %s index' % (idx, INDEX_NAME)
            ner_tag = json.loads(ner_tag_serialized[1])
            batched_documents.append(create_document(record, ner_tag))
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