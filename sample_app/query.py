from elasticsearch_dsl import Search, Q

from sample_app.config import ESConfig
from django_elasticsearch import settings


class ESQueryAndSearch:
    """
    Implementation of most common elasticsearch queries.
    Using elasticsearch_dsl, an abstraction library built on top of ES python client.
    It makes it easier towrite and run ES queries.
    """

    def __init__(self):
        # instance of elasticsearch_dsl Search class
        # querying on aliases helps you achieve near zero downtime in case of reindexing
        # also, aliases help to query multiple indices or filtered documents from multiple indices
        self.search_instance = Search(using=ESConfig().get_connection(),
                                      index=settings.ES_CONFIG['alias_name'])

    def _multi_match_query(self, search_query, search_fields):
        """
        This generates es query for querying across multiple fields in a doc.
        :return es query of type multi match
        """
        return Q('multi_match',
                 query=search_query,
                 fields=search_fields)

    def _term_filter_query(self, **kwargs):
        """
        This generates es term filter query for filtering docs based on one field in a doc.
        :return es query of type term filter
        """
        return Q('term', **kwargs)

    def bool_query(self, search_query, search_fields, **kwargs):
        """
        This function generates a bool query combining multimatch and term queries.
        It can be generalized to include many different kinds of queries inside bool query
        """
        return Q('bool',
                 must=[self._multi_match_query(search_query, search_fields),
                       self._term_filter_query(**kwargs)])

    def execute_query(self, es_query, response_fields):
        """Executes query with es search object"""
        return self.search_obj \
            .query(es_query) \
            .source(response_fields) \
            .execute() \
            .to_dict()

    def parse_es_response(self, response):
        """
        :param response: Elasticsearch response==
        {"hits":{"total":10,"max_score":1,"hits":[{"_index":"YOUR_INDEX_NAME","_type":"doc","_id":"1","_score":1,"_source":{"id":1,"name":"Shashank Pareta","department":"IT","skills_set":"Django, elasticsearch"}}]}}

        :return
        [{"id":1,"name":"Shashank Pareta","department":"IT","skills_set":"Django, elasticsearch"}]
        """
        return list(map(lambda r: r['_source'], response['hits']['hits']))
