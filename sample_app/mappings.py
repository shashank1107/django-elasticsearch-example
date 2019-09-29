def get_es_settings_mappings():
    """
    This returns settings and mappings for elasticsearch.
    It has analyzers for autocomplete and applied mappings on particular fields.
    """
    settings = {
        # no of primary shards (by default 5)
        "number_of_shards": 1,
        "number_of_replicas": 1,
        "analysis": {
            "analyzer": {
                "autocomplete": {
                    "type": "custom",
                    "tokenizer": "edge_ngram",
                    "filter": [
                        "english_stop",
                        "lowercase"
                    ]
                }
            },
            # it breaks words from edge with minimum of 1 letter and upto 20 letters in a word
            "tokenizer": {
                "edge_ngram": {
                    "type": "edge_ngram",
                    "min_gram": "1",
                    "max_gram": "20",
                    # chars other than mentioned will break the word into different words called tokens
                    "token_chars": [
                        "letter",
                        "digit",
                        "symbol"
                    ]
                }
            },
            # it removes frequently occuring words like prepositions, from indexing
            "filter": {
                "english_stop": {
                    "type": "stop",
                    "stopwords": "_english_"
                }
            }
        }
    }
    mappings = {
        "doc": {
            # it detects fields which store date information and indexes accordingly
            "date_detection": True,
            # all those fields which are not mentioned explicitly below indexes like in dynamic templates
            "dynamic_templates": [
                {
                    "string_fields": {
                        "mapping": {
                            "type": "string",
                            "fields": {
                                "raw": {
                                    # not_analyzed means this field stores as it is
                                    "index": "not_analyzed",
                                    "type": "string"
                                }
                            }
                        },
                        "match_mapping_type": "string"
                    }
                }
            ],
            "properties": {
                # name indexes in two ways. one raw which is same as in django models, other is autocomplete. For automplete queries, use name.autocomplete.
                "name": {
                    "type": "string",
                    "fields": {
                        "raw": {
                            "index": "not_analyzed",
                            "type": "string"
                        },
                        "autocomplete": {
                            "type": "string",
                            "analyzer": "autocomplete",
                            "search_analyzer": "standard"
                        }
                    },
                    "analyzer": "standard"
                },
                "skills_set": {
                    "type": "string",
                    "fields": {
                        "raw": {
                            "index": "not_analyzed",
                            "type": "string"
                        },
                        "autocomplete": {
                            "type": "string",
                            "analyzer": "autocomplete",
                            "search_analyzer": "standard"
                        }
                    },
                    "analyzer": "standard"
                }
            }
        }
    }

    return {
        "settings": settings,
        "mappings": mappings
    }
