'''
Created on Jul 15, 2012

@author: huhe
'''

from lib import Util
from isp import XPath
from isp.element import Element


class Tenant(Element):
    
    _catalogServiceOfferingType = 'tenant'
    _catalogServiceOfferingName = 'Four Zone Tenant'
    _catalogLinkTitle = 'Four Zone Tenant'
    
    
    def __init__(self, catalog, name=None, description=None, requestFileName='default-tenant.xml', requestParams=None):
        self.logger = Util.getLogger(self.__class__.__name__)
        Element.__init__(self)
        Element.setCatalogMatchParameter(self, Tenant._catalogServiceOfferingType, Tenant._catalogServiceOfferingName, Tenant._catalogLinkTitle)
        Element.setCreateParameter(self, name, description, requestFileName, requestParams)        
        if catalog: Element.parseCatalog(self, catalog)
    

    def getRoutablePrivateIpAddressPoolUid(self):
        ipAddressPool = Util.getXpathValue(self.detailXml, XPath._LinkTenantRoutablePrivateIpAddressPool)
        self.logger.info('routable private ip address pool: ' + ipAddressPool)
        return ipAddressPool
    
    
    