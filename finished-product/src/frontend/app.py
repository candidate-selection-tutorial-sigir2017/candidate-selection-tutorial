from collections import defaultdict
from itertools import groupby
from operator import itemgetter
import web
import pysolr
import string
import json
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet as wn
from sner import Ner

urls = (
    '/', 'SimpleIndexSearchPage',
    '/entityAwareSearchPage', 'EntityAwareSearch',
    '/searchSimpleIndex', 'SearchSimpleIndex',
    '/searchEntityAwareIndex', 'SearchEntityAwareIndex'
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
            'rows': int(count),
            'cache': 'false'
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


def search_entity_aware_index(query, offset, count, draw, qf, time_in_ms):
        """
        This function is responsible for hitting the solr endpoint
        and returning the results back.
        """
        results = SOLR_ENTITYAWAREINDEX.search(q=query, **{
            'start': int(offset),
            'rows': int(count),
            'segmentTerminatedEarly': 'true',
            'timeAllowed': time_in_ms,
            'cache': 'false',
            'qf': qf,
            'pf': qf,
            'debugQuery': 'true',
            'defType': 'edismax',
            'ps': 10
        })
        print("Saw {0} result(s) for query {1}.".format(len(results), query))
        formatted_hits = []
        print results.debug
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


    def get_synonyms(self, text):
        syn_set = []
        for synset in wn.synsets(str):
            for item in synset.lemma_names:
                syn_set.append(item)
        return syn_set


    def tokenize_text(self, text):
        # title = unicode(query, "utf-8")
        stop = stopwords.words('english') + list(string.punctuation)
        return [i for i in word_tokenize(text) if i not in stop]


    def build_clauses(self, prefix, tagged_segments):
        clauses = []
        for tagged_segment in tagged_segments:
            tokens = self.tokenize_text(tagged_segment)
            if len(tokens) == 1:
                clauses.append("%s:%s" % (prefix, tokens[0]))
            else:
                clauses.append("%s:\"%s\"" % (prefix, " ".join(tokens)))
        return clauses


    def GET(self):
        draw, query, offset, count = get_web_input(web_input=web.input())

        if query == '*:*':
            return search_entity_aware_index(query=query, offset=offset, count=count,
                          draw=draw, qf='_text_^1', time_in_ms=100)

        # Utilize entity tagger to give out entities and remove unwanted tags
        entity_tags = STANFORD_NER_SERVER.get_entities(query)
        entity_tags = self.accumulate_tags(entity_tags)
        print 'Entity tags for query - %s, %s' % (query, entity_tags)

        clauses = []
        for entity_tag, tagged_segments in entity_tags.iteritems():
            if entity_tag == 'PERSON':
                clauses.extend(self.build_clauses("_news_title_person", tagged_segments))
            elif entity_tag == 'LOCATION':
                clauses.extend(self.build_clauses("_news_title_location", tagged_segments))
            elif entity_tag == 'ORGANIZATION':
                clauses.extend(self.build_clauses("_news_title_organization", tagged_segments))
                clauses.extend(self.build_clauses("_news_title_publisher", tagged_segments))
            else:
                clauses.extend(self.build_clauses("_news_title", tagged_segments))

        query = " AND ".join(clauses)
        qf = '_news_title_person^10 _news_title_organization^5 _news_title_location^100 _news_title^2.0 _news_publisher^10.0'

        return search_entity_aware_index(query=query, offset=offset, count=count,
                      draw=draw, qf=qf, time_in_ms=250)


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
