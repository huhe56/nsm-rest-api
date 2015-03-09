'''
Created on Oct 18, 2012

@author: huhe
'''

from expect4j import Closure, ExpectState


class MyClosure(Closure):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
    def run(self, state):
        state.addVar("inside", "out")