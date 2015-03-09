'''
Created on Jul 15, 2012

@author: huhe
'''

from lib import Util
from isp import XPath
from isp.element import Element

class Provider(Element):
    
    _catalogServiceOfferingType = 'provider'
    _catalogServiceOfferingName = 'Service Provider'
    _catalogLinkTitle = 'Service Provider'
    
    def __init__(self, catalog, name=None, description=None, requestFileName='default-provider.xml', requestParams=None):
        self.logger = Util.getLogger(self.__class__.__name__)
        Element.__init__(self)
        Element.setCatalogMatchParameter(self, Provider._catalogServiceOfferingType, Provider._catalogServiceOfferingName, Provider._catalogLinkTitle)
        Element.setCreateParameter(self, name, description, requestFileName, requestParams)        
        Element.parseCatalog(self, catalog)
            

    def getGlobalIpAddressPoolUid(self):
        ipAddressPool = Util.getXpathValue(self.detailXml, XPath._LinkProviderGlobalIpAddressPool)
        self.logger.info('global ip address pool: ' + ipAddressPool)
        return ipAddressPool
        
        
    def getInfrastructureIpAddressPoolUid(self):
        ipAddressPool = Util.getXpathValue(self.detailXml, XPath._LinkProviderInfrastructureIpAddressPool)
        self.logger.info('infrastructure ip address pool: ' + ipAddressPool)
        return ipAddressPool
    
    
    def getPodList(self, testCaseId):
        podListUrl = Util.getXpathValue(self.detailXml, XPath._DetailLinkListPodHref)
        self.getList(podListUrl, 'pod', testCaseId)
        
        
        