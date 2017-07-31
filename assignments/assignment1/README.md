# Assignment 1!

In this assignment we will take a look at our dataset, the fields available and setup a basic search index using solr. We will read through the dataset and build our search index. Once we have the index setup we will write a very simple query to retrieve search results and show them on the ui.

## Exploring the News Aggregator Dataset
The first step of building a search index is to understand the dataset and the fields that you want to allow the user to search on. To do this we will read a first few records of the dataset into a tabular form. This will allow us to understand how does the data look like. 

This analysis allows us to understand to what degree are the following tasks needed

* Tokenization and Segmentation
* Term Normalization
* Data transformation 

We have provided you with a basic script that prints out the data in a tabular form along with some statistics about field values. 

To run the script issue the following command or run it with arguments from PyCharm.

~~~
cd ~/workspace/candidate-selection-tutorial/assignments/assignment1/excercise/src
python understand_data.py --input /home/sigir/workspace/candidate-selection-tutorial/finished-product/data/news-aggregator-dataset/newsCorpora.csv
~~~


## Building the Search Index
Now that we have gotten a glimpse of the dataset we will proceed further to build out a simple search index on top of Solr which we can query. 

The goal here is make a baseline index that we will use to compare with another index that we will be building in the assignment later.

We will be indexing the following fields in the search index. To get a broader understanding we will be using the minimal tokenization and analysis functionality from Solr. In **Assignment 0** when we setup Solr we made use of [**Solr Schema API**](https://lucene.apache.org/solr/guide/6_6/schema-api.html) to create a [**Dynamic Field**](https://lucene.apache.org/solr/guide/6_6/dynamic-fields.html) for storing our index fields. This will allow our indexed fields from the dataset to be tokenized and be searchable on the tokens.

In the first command we define a simple **TextField** which is the type of field we want our data to be present in. 

In the next command we add a **dynamic field** as we prefix all fields from the dataset with  \_news\_ prefix and declare it of type **simple_indexed_text** which we defined previously.


~~~
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

~~~

We will start by building a very basic document with prefix \_news\_ and utilizing **pysolr** for batch indexing the documents. 

As next steps open **simple_index.py** and complete the function for creating a document. This involves completing two steps 

* Writing the function for creating the document. **Pysolr** expects a dictionary containing all the fields to be put in the index. A special field with name **id** representing the unique id must be added. 
The fields to be added must be prefixed with \_news\_ to allow use of our custom TextField type.

* The second task involves writing code for adding a document to the solr index. Frequent additions can be slow, consider utilizing batched addition of documents into Solr. 

Refer to [**pysolr documentation**](https://github.com/django-haystack/pysolr)

Run the following command to start the indexing process.

~~~
python simple_index.py --input /home/sigir/workspace/candidate-selection-tutorial/finished-product/data/news-aggregator-dataset/newsCorpora.csv
~~~

## Query Rewriting and Searching
In this task we will connect our middletier and the frontend to the index. We will accept the query from the search front end, rewrite the query to search our index and send the results back to the frontend for displaying.

As next step open the file **frontend/app.py**. This is our middle tier that does serves the search requests and talks to the search backend. In this file you need to write the **GET** method of **SearchSimpleIndex** class. 

* **Match All Query** - This query will be useful for serving queries with no keywords. Refer to [**solr documentation**](http://lucene.apache.org/solr/quickstart.html#searching) on how to construct it.
* **Text Based Query** - For queries with keywords we will make use of the catch all field in solr. All content to be indexed in a predefined "catch-all" \_text\_ field, to enable single-field search that includes all fields' content. The query should look of the form:

~~~
Query: la times
Tokens: ['la', 'times']
Generated Query: _text_:la AND _text_:times
~~~

### Running the server
To see the search in action follow the commands below:

~~~
cd frontend
python app.py
~~~

This should run the simple index search server on [http://0.0.0.0:8080](http://0.0.0.0:8080). The page should look like the image below. Try out some queries to see if you are getting results back.

Congratulations you have completed assignment 1!





