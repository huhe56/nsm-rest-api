'''
Created on Jul 15, 2012

@author: huhe
'''

from lib import Util
from isp.element import Element
from isp.connection import Connection


class ExternalConnection(Connection):
    
    _catalogServiceOfferingType = 'externalnetworkconnection'
    _catalogServiceOfferingName = 'External Connection'
    _catalogLinkTitle = 'External Connection'
    
    
    def __init__(self, catalog, name=None, description=None, requestFileName='default-external-connection.xml', requestParams=None):
        self.logger = Util.getLogger(self.__class__.__name__)
        Element.__init__(self)
        Element.setCatalogMatchParameter(self, ExternalConnection._catalogServiceOfferingType, ExternalConnection._catalogServiceOfferingName, ExternalConnection._catalogLinkTitle)
        Element.setCreateParameter(self, name, description, requestFileName, requestParams)        
        Element.parseCatalog(self, catalog)
        
        
    
    
