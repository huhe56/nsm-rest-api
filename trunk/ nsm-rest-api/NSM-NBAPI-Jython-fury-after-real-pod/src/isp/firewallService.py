'''
Created on Jul 15, 2012

@author: huhe
'''

from lib import Util
from isp.element import Element
from isp.nsmUtil import NsmUtil


class FirewallService(Element):
    
    _catalogServiceOfferingType = 'servicepolicy'
    _catalogServiceOfferingName = 'Firewall Service'
    _catalogLinkTitle = 'Firewall Service'
    
    
    def __init__(self, catalog, name=None, description=None, requestFileName='default-firewall-service.xml', requestParams=None):
        self.logger = Util.getLogger(self.__class__.__name__)
        Element.__init__(self)
        Element.setCatalogMatchParameter(self, FirewallService._catalogServiceOfferingType, FirewallService._catalogServiceOfferingName, FirewallService._catalogLinkTitle)
        Element.setCreateParameter(self, name, description, requestFileName, requestParams)        
        Element.parseCatalog(self, catalog)
        

