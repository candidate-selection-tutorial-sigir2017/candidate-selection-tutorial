#!/bin/bash

set -e

# Escape code
esc=`echo -en "\033"`

# Set colors
cc_red="${esc}[0;31m"
cc_green="${esc}[0;32m"
cc_yellow="${esc}[0;33m"
cc_blue="${esc}[0;34m"
cc_normal=`echo -en "${esc}[m\017"`

function ec () {
    echo -e "${cc_green}${1}${cc_normal}"
}

ec "Downloading the NewsAggregator dataset"
wget -nc http://archive.ics.uci.edu/ml/machine-learning-databases/00359/NewsAggregatorDataset.zip
rm -r news-aggregator-dataset
mkdir news-aggregator-dataset
cd news-aggregator-dataset
unzip ./../NewsAggregatorDataset.zip
cd ..
rm NewsAggregatorDataset.zip
ec "NewsAggregator dataset has been downloaded!"
ec "\nFetching Stanford NER library and dependencies"
wget -nc "https://nlp.stanford.edu/software/stanford-ner-2017-06-09.zip"
unzip stanford-ner-2017-06-09.zip
mv stanford-ner-2017-06-09 stanford-ner
rm -r stanford-ner-2017-06-09.zip
ec "\nDownloading Stanford Core NLP english models"
wget -nc http://nlp.stanford.edu/software/stanford-english-corenlp-2017-06-09-models.jar
rm -r stanford-english-corenlp-models
mkdir stanford-english-corenlp-models
cd stanford-english-corenlp-models
jar -xvf ./../stanford-english-corenlp-2017-06-09-models.jar
cd ..
cp -r stanford-english-corenlp-models/edu/stanford/nlp/models/ner/* stanford-ner/classifiers/
rm -r stanford-english-corenlp-models
ec "\n\nData dependency setup completed!"

