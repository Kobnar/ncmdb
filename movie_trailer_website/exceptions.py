__author__ = 'kobnar'


class ValidationError(Exception):
    """
    A simple validation error.
    """
    def __init__(self, field, value, msg=None):
        self.field = field
        self.value = value
        if msg:
            self.msg = msg
        else:
            self.msg = 'Invalid value for \'{}\': {}'.format(field, value)

    def __str__(self):
        return repr(self.msg)

    def __repr__(self):
        return repr(self.msg)
