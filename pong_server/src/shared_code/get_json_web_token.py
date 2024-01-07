def get_json_web_token(query_string):
    """ Returns JWT payload if the token is valid,
        otherwise raises Exception """

    json_web_token = query_string.get('json_web_token', None)
    if json_web_token is None:
        raise Exception('json_web_token was not found in query string')

    json_web_token_errors = check_json_web_token_errors(json_web_token)
    if json_web_token_errors is not None:
        raise Exception(json_web_token_errors)
    return json_web_token


def check_json_web_token_errors(json_web_token):
    # TODO check signature

    if json_web_token.get('user_id') is None:
        # TODO Remove this if as if the signature is correct, 'user_id' must exist
        return 'user_id field was not found in json_web_token'
    return None
