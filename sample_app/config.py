import boto3
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth

from django_elasticsearch import settings


class Singleton:
    """
    This class is used to create singleton object of class. Just add this as wrapper to any Class.
    """

    def __init__(self, cls):
        self.cls = cls
        self.instance = None

    def __call__(self, *args, **kwargs):
        if self.instance is None:
            self.instance = self.cls(*args, **kwargs)
        return self.instance


@Singleton
class ESConfig:
    es_conn = None

    def get_connection(self):
        """
        :return: single instance of ES connection to nodes
        """
        if self.es_conn is None:
            credentials = boto3.Session(aws_access_key_id=settings.AWS_SES_ACCESS_KEY_ID,
                                        aws_secret_access_key=settings.AWS_SES_SECRET_ACCESS_KEY).get_credentials()
            # AWS4Auth provides AWS authentication for http requests to elasticsearch
            awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, settings.ES_CONFIG['aws-region'],
                               'es')
            # creates a secure connection to Elasticsearch hosts.
            # RequestsHttpConnection needs requests to be installed. Used this class as we are using custom aws requests auth.
            # hosts is a list of all nodes in Elasticsearch cluster
            self.es_conn = Elasticsearch(
                hosts=[{'host': settings.ES_CONFIG['host'], 'port': settings.ES_CONFIG['port']}],
                use_ssl=True,
                verify_certs=True,
                http_auth=awsauth,
                connection_class=RequestsHttpConnection)
        return self.es_conn
