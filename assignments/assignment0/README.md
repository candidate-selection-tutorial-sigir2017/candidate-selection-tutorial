# Assignment 0!

In this assignment we will be working to make sure our development environment has been set up completely. We will be working with opensource systems, links and documentation to each of the parts will be included for reference as well. 

We will also take a quick look at our open source dataset to familiarize ourselves with it. 

## Building Blocks
We look at the tools that will lay out the foundation for helping us build a full stack search engine capable of serving an opensource dataset. 

### Python

![Python Logo](https://www.python.org/static/community_logos/python-powered-w-200x80.png)

We will be working through our hands on tutorial utilizing [**Python 2.7**](https://www.python.org/download/releases/2.7/) as our primary coding language. Python has grown to become very mature and is very easy to use. There also exists a plethora of libraries contributed by academia, industry and enthusiasts. Along with good infrastructure support there is also very well documented libraries for data science and machine learning. 

In our tutorial we will be using the following dependencies - 

* [**PySolr**](https://github.com/django-haystack/pysolr) is a lightweight Python wrapper for Apache Solr. It provides an interface that queries the server and returns results based on the query.

* [**NLTK**](http://www.nltk.org/) is a leading platform for building Python programs to work with human language data. It provides easy-to-use interfaces to over 50 corpora and lexical resources such as WordNet, along with a suite of text processing libraries for classification, tokenization, stemming, tagging, parsing, and semantic reasoning, wrappers for industrial-strength NLP libraries, and an active discussion forum.

* [**Web.py**](http://webpy.org/) is a web framework for Python that is as simple as it is powerful. web.py is in the public domain; you can use it for whatever purpose with absolutely no restrictions.


* [**Pandas**](http://pandas.pydata.org/) is an open source, BSD-licensed library providing high-performance, easy-to-use data structures and data analysis tools for the Python programming language.


### Solr

![Solr Logo](http://www.mcplusa.com/wp-content/uploads/2016/05/platform-solr-logo-330x200.png)

[**Apache Solr**](http://lucene.apache.org/solr/) is an open source search platform built upon a Java library called Lucene. Solr is a popular search platform for Web sites because it can index and search multiple sites and return recommendations for related content based on the search query's taxonomy.


### Stanford CoreNLP
[**Stanford CoreNLP**](https://stanfordnlp.github.io/CoreNLP/) provides a set of human language technology tools. It can give the base forms of words, their parts of speech, whether they are names of companies, people, etc., normalize dates, times, and numeric quantities, mark up the structure of sentences in terms of phrases and syntactic dependencies, indicate which noun phrases refer to the same entities, indicate sentiment, extract particular or open-class relations between entity mentions, get the quotes people said, etc.

### spaCy NLP
[**spaCy NLP**](https://spacy.io/) excels at large-scale information extraction tasks. It's written from the ground up in carefully memory-managed Cython.

### Ubuntu Linux

## Dataset
We will be using an open source News Aggregator Dataset. It references to news pages collected from a web aggregator in the period from 10-March-2014 to 10-August-2014. The resources are grouped into clusters that represent pages discussing the same story.

Full details about the dataset can be found at [**UCI Machine Learning Repository - News Aggregator Dataset**](http://archive.ics.uci.edu/ml/datasets/News+Aggregator#)

####Acknowledgement
Lichman, M. (2013). UCI Machine Learning Repository [http://archive.ics.uci.edu/ml]. Irvine, CA: University of California, School of Information and Computer Science.



## Setup Instructions
####Download Ubuntu Virtual Machine

The virtual machine is currently running Ubuntu and has all the dependencies setup for you. This is a good option if you do not want to corrupt or change things in python installed on your machine.

[**Virtual Box VM Download**]()
Username: **sigir** Password: **sigir2017**

Open Terminal and follow the commands. These commands do the following tasks

* Clone the repository from github
* Setup the Python Virtual Environment with all dependencies
* Download and extract the dataset
* Setup a solr instance and create index schema for the dataset

~~~
cd ~/
mkdir workspace
github clone <Link>
source ~/.sigir-venv/bin/actiate
cd candidate-selection-tutorial
cd assignments/assignment0/excercise
./python-env.sh
./get_dataset.sh
./setup_solr.sh
~~~

Open another Terminal window and start the **Stanford NER** server. This will be used in subsequent assignments for Named Entity Recognition.

~~~
java -Djava.ext.dirs=./lib -cp /home/sigir/workspace/candidate-selection-tutorial/finished-product/data/stanford-ner/stanford-ner.jar edu.stanford.nlp.ie.NERServer -port 9199 -loadClassifier /home/sigir/workspace/candidate-selection-tutorial/finished-product/data/stanford-ner/classifiers/english.muc.7class.distsim.crf.ser.gz  -tokenizerFactory edu.stanford.nlp.process.WhitespaceTokenizer -tokenizerOptions tokenizeNLs=false
~~~

Once you have completed the above steps your development environment has been setup and you are ready to proceed to Assignment 1!