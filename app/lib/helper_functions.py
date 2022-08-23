from urllib.parse import urlencode


def url_with_querystring(path, **kwargs) -> str:
    return f'{path}?{urlencode(kwargs)}'
