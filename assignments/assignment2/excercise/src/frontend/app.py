from itertools import groupby
from operator import itemgetter

import web
import pysolr
import string
import json

from collections import defaultdict
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sner import Ner

urls = (
    '/', 'SimpleIndexSearchPage',
    '/entityAwareSearchPage', 'EntityAwareSearch',
    '/searchSimpleIndex', 'SearchSimpleIndex',
    '/searchEntityAwareIndex', 'SearchEntityAwareIndex',
    '/searchEntityAwareWithEfficientQuery', 'SearchEntityAwareWithEfficientQuery'
)

CATEGORY = {'b': 'Business', 'e': 'Entertainment', 't': 'Science and Technology', 'm': 'Health'}
render = web.template.render('templates/', base='layout')
SOLR_SIMPLEINDEX = pysolr.Solr('http://localhost:8983/solr/simpleindex')
SOLR_ENTITYAWAREINDEX = pysolr.Solr('http://localhost:8983/solr/entityawareindex')
STANFORD_NER_SERVER = Ner(host='localhost', port=9199)


def get_web_input(web_input):
    draw = web_input['draw']
    query = web_input['search[value]']
    if len(query) == 0:
        query = '*:*'
    offset = web_input['start']
    count = web_input['length']
    return draw, query, offset, count


def search_simple_index(query, offset, count, draw):
        """
        This function is responsible for hitting the solr endpoint
        and returning the results back.
        """
        results = SOLR_SIMPLEINDEX.search(q=query, **{
            'start': int(offset),
            'rows': int(count)
        })
        print("Saw {0} result(s) for query {1}.".format(len(results), query))
        formatted_hits = []
        for hit in results.docs:
            formatted_hits.append(
                [hit['_news_title'], hit['_news_publisher'], CATEGORY[hit['_news_category'][0]], hit['_news_url']])
        response = {'draw': draw,
                    'recordsFiltered': results.hits,
                    'data': formatted_hits}
        web.header('Content-Type', 'application/json')
        return json.dumps(response)


def search_entity_aware_index(query, offset, count, draw, qf):
        """
        This function is responsible for hitting the solr endpoint
        and returning the results back.
        """
        results = SOLR_ENTITYAWAREINDEX.search(q=query, **{
            'start': int(offset),
            'rows': int(count),
            'qf': qf
        })
        print("Saw {0} result(s) for query {1}.".format(len(results), query))
        formatted_hits = []
        for hit in results.docs:
            formatted_hits.append(
                [hit['_news_title'], hit['_news_publisher'], CATEGORY[hit['_news_category'][0]], hit['_news_url']])
        response = {'draw': draw,
                    'recordsFiltered': results.hits,
                    'data': formatted_hits}
        web.header('Content-Type', 'application/json')
        return json.dumps(response)


class SimpleIndexSearchPage:
    def GET(self):
        return render.simpleIndexSearchPage()


class EntityAwareSearch:
    def GET(self):
        return render.entityAwareSearchPage()


class SearchSimpleIndex:
    def GET(self):
        draw, query, offset, count = get_web_input(web_input=web.input())

        if query == '*:*':
            return search_simple_index(query=query, offset=offset, count=count, draw=draw)

        clauses = []
        for token in word_tokenize(query):
            clauses.append("+_text_:%s" % token)
        query = " AND ".join(clauses)
        return search_simple_index(query=query, offset=offset, count=count, draw=draw)


class SearchEntityAwareIndex:
    def accumulate_tags(self, list_of_tuples):
        tokens, entities = zip(*list_of_tuples)
        recognised = defaultdict(set)
        duplicates = defaultdict(list)

        for i, item in enumerate(entities):
            duplicates[item].append(i)

        for key, value in duplicates.items():
            for k, g in groupby(enumerate(value), lambda x: x[0] - x[1]):
                indices = list(map(itemgetter(1), g))
                recognised[key].add(' '.join(tokens[index] for index in indices))
        # recognised.pop('O', None)

        recognised = dict(recognised)
        ner_info = {}
        for key, value in recognised.iteritems():
            ner_info[key] = list(value)
        return ner_info


    def GET(self):
        draw, query, offset, count = get_web_input(web_input=web.input())

        # TODO: Write code for handling the empty query (no keywords)
        # TODO: Write code for tokenizing the search query
        # TODO: Use the Stanford NER server to get NER tags for the query
        # TODO: Write out the candidate query with NER index fields
        # TODO: Define the boosting parameters for different NER index field matches

        return None


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()