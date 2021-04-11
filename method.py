'''HTTP protocol method classes

   Tom Söderlund <tom.soderlund@iki.fi> 2021-04-21'''

class Method:
    '''Super class for HTTP protocol methods'''
    def __init__(self, name):
        self.name = name

class Trace(Method):
    '''Class for HTTP protocol method TRACE'''
    def __init__(self):
        super().__init__('TRACE')

class Options(Method):
    '''Class for HTTP protocol method OPTIONS'''
    def __init__(self):
        super().__init__('OPTIONS')

class Get(Method):
    '''Class for HTTP protocol method GET'''
    def __init__(self):
        super().__init__('GET')
