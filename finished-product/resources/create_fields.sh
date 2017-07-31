#!/bin/bash

./solr-6.6.0/bin/solr delete -c simpleindex
./solr-6.6.0/bin/solr delete -c entityawareindex
./solr-6.6.0/bin/solr restart
./solr-6.6.0/bin/solr create -c simpleindex
./solr-6.6.0/bin/solr create -c entityawareindex

curl -X POST -H 'Content-type:application/json' --data-binary '{
  "add-field-type" : {
     "name":"simple_indexed_text",
     "class":"solr.TextField",
     "positionIncrementGap":"100",
     "analyzer" : {
        "tokenizer":{ 
           "class":"solr.WhitespaceTokenizerFactory" }
      }}
}' http://localhost:8983/solr/simpleindex/schema

curl -X POST -H 'Content-type:application/json' --data-binary '{
  "add-dynamic-field":{
     "name":"_news_*",
     "type":"simple_indexed_text",
     "indexed":true,
     "stored":true }
}' http://localhost:8983/solr/simpleindex/schema

curl -X POST -H 'Content-type:application/json' --data-binary '{
  "add-field-type" : {
     "name":"simple_indexed_text",
     "class":"solr.TextField",
     "positionIncrementGap":"100",
     "analyzer" : {
        "tokenizer":{ 
           "class":"solr.WhitespaceTokenizerFactory" }
      }}
}' http://localhost:8983/solr/entityawareindex/schema

curl -X POST -H 'Content-type:application/json' --data-binary '{
  "add-dynamic-field":{
     "name":"_news_*",
     "type":"simple_indexed_text",
     "indexed":true,
     "stored":true }
}' http://localhost:8983/solr/entityawareindex/schema
