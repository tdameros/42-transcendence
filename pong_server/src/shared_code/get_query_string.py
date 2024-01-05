from urllib.parse import unquote
import json


def get_query_string(environ):
    query_string = environ.get('QUERY_STRING', None)
    if query_string is None:
        raise Exception('environ does not contain query string')

    query_string = unquote(query_string).split('=undefined')
    if len(query_string) == 0:
        raise Exception(f'invalid query string: '
                        f'{environ.get('QUERY_STRING')}')
    query_string = query_string[0]

    try:
        return json.loads(query_string)
    except json.JSONDecodeError as e:
        raise Exception(f'Failed to parse query string: {e}')
