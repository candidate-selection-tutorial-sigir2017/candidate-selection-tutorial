stanford_title_ner_tags_case_sensitive.csv.gz# Assignment 2!

In this assignment we will be building a better index with fields specific to the entities recognized in the title. We will make use of Stanford NER along NLTK. In addition to building the index we will work on utilizing entities in the incoming query and writing a field specific query matching entities in the query with the fields containing those entities in the search index. 

## Building the Search Index
We will use our learnings from the previous assignment to build the entity based search index. To utilize the time better we have pregenerated the entity tags using the **Stanford NER** library and **english.all.3class.distsim.crf.ser.gz** classifier. The classifier provides three tags namely

* *PERSON*
* *ORGANIZATION*
* *LOCATION*

When building the index we will read through the tags and our dataset simultaneously. This will allow us to use the pregenerated tags when building the document to be indexed. 

Open the file **entity\_aware\_index.py** and you will need to implement the following parts

* Writing the function for creating the document. Similar to **Assignment 1** we will be building a dictionary with all the index fields. Our focus here will be to add additional title fields specifically for the NER tags. The specific fields \_news\_title\_person, \_news\_title\_organization and \_news\_title\_location need to be added in addition to \_news\_title. 

~~~
Your documents should have a structure similar to the one below -

{
	"_news_url": "http://www.ifamagazine.com/news/us-open-stocks-fall-after-fed-official-hints-at-accelerated-tapering-294436",
	"_news_title_organization": "Fed",
	"_news_title": "us open: stocks fall after fed official hints at accelerated tapering",
	"_news_story": "dduyu0vzz0brnemioxupqvp6sixvm",
	"_news_category": "b",
	"_news_hostname": "www.ifamagazine.com",
	"_news_publisher": "ifa magazine",
	"_news_timestamp": "1394470371550",
	"id": "3",
	"_news_title_location": "US"
}
~~~

* The second task involves writing code for addition a document to the Solr index. You can reuse your code from **Assignment 1** here.

To begin indexing follow the commands listed below, you need to be in the **assignment2** folder for running the commands.

~~~
cd exercise/src
python entity_aware_index.py --input /home/sigir/workspace/candidate-selection-tutorial/finished-product/data/news-aggregator-dataset/newsCorpora.csv --ner_tags /home/sigir/workspace/candidate-selection-tutorial/finished-product/resources/stanford_title_ner_tags_case_sensitive.csv.gz
~~~

## Query Rewriting and Searching
In this task we will define a query that is matched with the document on specific fields. We will make use of our entity understanding and utilize the **Stanford NER** server at runtime to generate tags. 

As next step open the file **frontend/app.py**. This is our middle tier that does serves the search requests and talks to the search backend. In this file you need to write the **GET** method of **SearchEntityAwareIndex** class. 

* **Match All Query** - Similar to **Assignment 1** add the logic to serve results when the query is empty.
* **Entity & Field Based Query** - For queries with keywords we will make use of the catch all field in solr. All content to be indexed in a predefined "catch-all" \_text\_ field, to enable single-field search that includes all fields' content. The query should look of the form:

~~~
Query: cooperman paypal
Tokens: ['cooperman', 'paypal']
NER Tags: {"ORGANIZATION": ["PayPal"], "PERSON": ["Cooperman"]}
Generated Query: _news_title_organization:paypal AND _news_title_person:Cooperman
~~~

#### Helper Code Snippets
* Calling the Stanford NER server to get NER tags, accumulate_tags function in SearchEntityAwareIndex is provided for aggregating the NER tags.

~~~
entity_tags = STANFORD_NER_SERVER.get_entities(query)
entity_tags = self.accumulate_tags(entity_tags)
~~~

* Boosting Paramter - You can pass in an optional boosting parameter of the form to boost matches in certain fields. Example

~~~
qf = '_news_title_person^10 _news_title_organization^5 _news_title_location^100 _news_title^2.0 _news_publisher^10.0'

~~~

### Running the server
To see the search in action follow the commands below:

~~~
cd frontend
python app.py
~~~

This should run the simple index search server on [http://0.0.0.0:8080](http://0.0.0.0:8080). The page should look like the image below. Try out some queries to see if you are getting results back.

Congratulations you have completed assignment 1!





