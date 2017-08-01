from __future__ import unicode_literals

import argparse
import csv

from prettytable import PrettyTable
import pandas as pd


HEADERS = ["ID", "TITLE", "URL", "PUBLISHER", "CATEGORY", "STORY", "HOSTNAME", "TIMESTAMP"]

def run(input_file, num_records):

    # printing data in a structured form
    with open(input_file) as csvfile:
        csvreader = csv.reader(csvfile, delimiter=b'\t')
        pretty_table = PrettyTable()
        pretty_table.field_names = HEADERS
        for count, row in enumerate(csvreader):
            if count == num_records:
                break
            pretty_table.add_row(row)
        print pretty_table

    raw_input('Enter to continue: ')
    # analyze the dataset
    dataset = pd.read_csv(input_file, nrows=500000, sep=b'\t', names=HEADERS)
    print 'Shape of the dataset - %s' % (dataset.shape,)

    raw_input('Enter to continue: ')
    print 'Category values in the dataset -'
    print(dataset.CATEGORY.value_counts())

    raw_input('Enter to continue: ')
    print 'Most common hostnames in the dataset -'
    print(dataset.HOSTNAME.value_counts()[dataset.HOSTNAME.value_counts() > 50])




def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--input', action='store', dest='input', )
    arg_parser.add_argument('--num_records', action='store', dest='num_records', default=10)
    args = arg_parser.parse_args()
    run(input_file=args.input, num_records=args.num_records)


if __name__ == '__main__':
    main()