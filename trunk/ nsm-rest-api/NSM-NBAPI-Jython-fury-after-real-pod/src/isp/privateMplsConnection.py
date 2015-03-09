'''
Created on Jul 15, 2012

@author: huhe
'''

from lib import Util
from isp.element import Element
from isp.connection import Connection


class PrivateMplsConnection(Connection):
    
    _catalogServiceOfferingType = 'externalnetworkconnection'
    _catalogServiceOfferingName = 'Private MPLS Connection'
    _catalogLinkTitle = 'Private MPLS Connection'
    
    
    def __init__(self, catalog, name=None, description=None, requestFileName='default-private-mpls-connection.xml', requestParams=None):
        self.logger = Util.getLogger(self.__class__.__name__)
        Element.__init__(self)
        Element.setCatalogMatchParameter(self, PrivateMplsConnection._catalogServiceOfferingType, PrivateMplsConnection._catalogServiceOfferingName, PrivateMplsConnection._catalogLinkTitle)
        Element.setCreateParameter(self, name, description, requestFileName, requestParams)        
        Element.parseCatalog(self, catalog)
        
        
    