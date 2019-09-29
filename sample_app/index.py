from elasticsearch import helpers

from django_elasticsearch import settings
from sample_app.config import ESConfig
from sample_app.mappings import get_es_settings_mappings


class ESIndex:

    def __init__(self):
        self.es_conn = ESConfig().get_connection()
        self.index_name = settings.ES_CONFIG['index_name']
        self.alias_name = settings.ES_CONFIG['alias_name']

    def create_index(self):
        """
        This creates an index with specified settings and mappings.
        If index already present, deletes an existing one and creates new.
        """
        if self.es_conn.indices.exists(index=self.index_name):
            self.es_conn.indices.delete(index=self.index_name)
        # create index
        self.es_conn.indices.create(index=self.index_names, body=get_es_settings_mappings())

    def create_alias(self):
        """
        This creates an alias for one or a list of indices.
        An alias is like a pointer to an index or list of indices or selected documents from list of
        indices based on filters.
        """
        self.es_conn.indices.put_alias(index=self.index_name,
                                       name=self.alias_name)

    def indexing_doc(self, obj):
        """This syncs object in django models to elasticsearch doc. Throws error if index not present."""
        self.es_conn.index(index=self.index_name,
                           doc_type='doc',
                           id=obj['id'],
                           body=obj)

    def deleting_doc(self, doc_id):
        """This deletes document from elasticsearch. Throws error if index not present."""
        self.es_conn.delete(index=self.index_name,
                            doc_type='doc',
                            id=doc_id)

    def bulk_indexing_to_es(self, qs):
        """
        :param qs: queryset
        This indexes documents to elasticsearch in chunks of 50.
        Can customize this depending on resources availability
        """
        data_to_index = self._gen_data(qs)
        helpers.bulk(self.es_conn, data_to_index, chunk_size=50)

    def _gen_data(self, qs):
        """
        This returns a generator with doc model as required by helpers class.
        """
        for qs_obj in qs:
            # should serialize qs_obj here one by one.
            # data = _get_serialized_data(qs_obj, source)
            yield {
                "_index": self.index_name,
                "_type": "doc",
                "_id": qs_obj['id'],
                "_source": qs_obj
            }
