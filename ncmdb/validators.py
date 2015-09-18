"""
The Regex validation strings provided here were created by the MongoEngine team
and released under the MIT license. They have been reproduced here instead of
importing and instantiating various field classes so as to reduce the total
dependencies of the Nicolas Cage Movie Database and simplify the validation
process.
"""

import re
import translationstring
from colander import Invalid

_ = translationstring.TranslationStringFactory('colander')


_URI_REGEX = re.compile(
    r'^(?:[a-z0-9\.\-]*)://'  # scheme is validated separately
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}(?<!-)\.?)|'  # domain...
    r'localhost|'  # localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # ...or ipv4
    r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # ...or ipv6
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)


_URI_SCHEMES = ['http', 'https', 'ftp', 'ftps']


def validate_uri(url):
    scheme = url.split('://')[0].lower()
    if scheme in _URI_SCHEMES and _URI_REGEX.match(url):
        return url
    return


class URIValidator(object):
    """
    A Colander style URL validator. Returns a :class:`colendar.Invalid`
    exception if the URL is invalid.
    """
    def __init__(self, msg=None):
        if msg is None:
            self.msg = _('Invalid URL')
        else:
            self.msg = msg

    def __call__(self, node, value):
        if not validate_uri(value):
            raise Invalid(node, self.msg)
