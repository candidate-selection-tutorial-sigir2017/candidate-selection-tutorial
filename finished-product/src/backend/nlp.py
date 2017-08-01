# from __future__ import unicode_literals
import argparse
from tqdm import tqdm
import ner
from collections import defaultdict
from itertools import groupby
from operator import itemgetter
from nltk.tokenize import StanfordTokenizer
from nltk.tag.stanford import StanfordNERTagger
from sner import Ner
import json
import csv
import sys
reload(sys)
sys.setdefaultencoding('utf8')


INDEX_MAP = ["ID", "TITLE", "URL", "PUBLISHER", "CATEGORY", "STORY", "HOSTNAME", "TIMESTAMP"]

# Location, Time, Person, Organization, Money, Percent, Date
CASELESS_CLASSIFIER = '/usr/share/stanford-ner/classifiers/english.muc.7class.caseless.distsim.crf.ser.gz'

# To use the Stanford NER server run the following command in the stanford-ner directory
'''
java -Xmx3g -Djava.ext.dirs=./lib -cp stanford-ner.jar edu.stanford.nlp.ie.NERServer -port 9199 -loadClassifier
./classifiers/english.muc.7class.distsim.crf.ser.gz  -tokenizerFactory edu.stanford.nlp.process.WhitespaceTokenizer
-tokenizerOptions tokenizeNLs=false
'''
STANFORD_NER_HANDLER = Ner(host='localhost',port=9199)


def accumulate(list_of_tuples):
    tokens, entities = zip(*list_of_tuples)
    recognised = defaultdict(set)
    duplicates = defaultdict(list)

    for i, item in enumerate(entities):
        duplicates[item].append(i)

    for key, value in duplicates.items():
        for k, g in groupby(enumerate(value), lambda x: x[0] - x[1]):
            indices = list(map(itemgetter(1), g))
            recognised[key].add(' '.join(tokens[index] for index in indices))
    recognised.pop('O', None)

    recognised = dict(recognised)
    ner_info = {}
    for key, value in recognised.iteritems():
        ner_info[key] = list(value)
    return ner_info


def _generate_ner_tags(sentence):
    token_entity_pairs = STANFORD_NER_HANDLER.get_entities(sentence)
    accumulated = accumulate(token_entity_pairs)
    return accumulated


def generate_ner_tags(input_file, output_file, num_records):
    with open(input_file) as csvfile:
        with open(output_file, 'w+') as csvoutputfile:
            records = csv.reader(csvfile, delimiter=b'\t')
            for idx, record in tqdm(enumerate(records)):
                if idx == num_records:
                    break
                title = record[1]
                ner_tags = _generate_ner_tags(title)
                csvoutputfile.write("%s\t%s" % (record[0], json.dumps(ner_tags)))
                csvoutputfile.write("\n")
                csvoutputfile.flush()




def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--input', action='store', dest='input', )
    arg_parser.add_argument('--output', action='store', dest='output', )
    arg_parser.add_argument('--num_records', action='store', dest='num_records', default=500000)
    args = arg_parser.parse_args()
    generate_ner_tags(input_file=args.input, output_file=args.output, num_records=args.num_records)

if __name__ == '__main__':
    main()
