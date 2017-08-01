import web
import pysolr
import json
from nltk.tokenize import word_tokenize

urls = (
    '/', 'SimpleIndexSearchPage',
    '/searchSimpleIndex', 'SearchSimpleIndex',
)

CATEGORY = {'b': 'Business', 'e': 'Entertainment', 't': 'Science and Technology', 'm': 'Health'}
render = web.template.render('templates/', base='layout')
SOLR_SIMPLEINDEX = pysolr.Solr('http://localhost:8983/solr/simpleindex')


def get_web_input(web_input):
    draw = web_input['draw']
    query = web_input['search[value]']
    if len(query) == 0:
        query = '*:*'
    offset = web_input['start']
    count = web_input['length']
    return draw, query, offset, count


def search(query, offset, count, draw, solr_endpoint):
    """
    This function is responsible for hitting the solr endpoint
    and returning the results back.
    """
    results = solr_endpoint.search(q=query, **{
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


class SimpleIndexSearchPage:
    def GET(self):
        return render.simpleIndexSearchPage()


class SearchSimpleIndex:
    def GET(self):
        draw, query, offset, count = get_web_input(web_input=web.input())
        # TODO: Write code for handling the empty query (no keywords)
        # TODO: Write code for tokenizing the search query and creating must clauses for each token
        return None



if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()