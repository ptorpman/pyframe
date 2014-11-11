


class NoReferencesException(Exception):
    ''' Exception raised when all references to an instances are removed '''
    def __init__(self, output):
        self.output = output

    def __str__(self):
        return 'NoReferencesException: %s' % self.output

class NoInterfaceException(Exception):
    ''' Exception raised when an interface is not supported '''
    def __init__(self, output):
        self.output = output

    def __str__(self):
        return 'NoInterfaceException: %s' % self.output

class TooManyReleaseException(Exception):
    ''' Exception raised when an interfaces has been released one too many times '''
    def __init__(self, output):
        self.output = output

    def __str__(self):
        return 'TooManyReleaseException: %s' % self.output

