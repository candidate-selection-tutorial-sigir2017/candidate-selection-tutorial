#!/bin/bash

rm -rf solr-6.6.0
wget -nc http://www-eu.apache.org/dist/lucene/solr/6.6.0/solr-6.6.0.tgz
tar -zxf solr-6.6.0.tgz
cd solr-6.6.0
bin/solr restart
cd ..
./create_fields.sh
