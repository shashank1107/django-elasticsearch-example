from sample_app.query import ESQueryAndSearch


def fetch_employees(search_query):
    """
    :param search_query: this can be either partial name or skill set.
    :return: Do a full text search on name and skills set in elasticsearch and
            return all relevant employees list
    """
    bool_query = ESQueryAndSearch().bool_query(search_query, ['name.autocomplete', 'skills_set.autocomplete'])
    # results only returns selected fields from ES. By default, it retrieves entire document.
    result = ESQueryAndSearch().execute_query(bool_query, ['id', 'name', 'skills_set', 'department'])
    parsed_response = ESQueryAndSearch().parse_es_response(result)
    return parsed_response
