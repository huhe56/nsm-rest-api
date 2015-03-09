'''
Created on Jul 15, 2012

@author: huhe
'''

from lib import Util
from isp.element import Element

class StaticNatPortRedirectionService(Element):
    
    _catalogServiceOfferingType = 'servicepolicy'
    _catalogServiceOfferingName = 'Static NAT Service With Port Redirection'
    _catalogLinkTitle = 'Static NAT Service With Port Redirection'
    
    
    def __init__(self, catalog, name=None, description=None, requestFileName='default-static-nat-port-redirection-service.xml', requestParams=None):
        self.logger = Util.getLogger(self.__class__.__name__)
        Element.__init__(self)
        Element.setCatalogMatchParameter(self, StaticNatPortRedirectionService._catalogServiceOfferingType, StaticNatPortRedirectionService._catalogServiceOfferingName, StaticNatPortRedirectionService._catalogLinkTitle)
        Element.setCreateParameter(self, name, description, requestFileName, requestParams)        
        Element.parseCatalog(self, catalog)
        
        
   
    
