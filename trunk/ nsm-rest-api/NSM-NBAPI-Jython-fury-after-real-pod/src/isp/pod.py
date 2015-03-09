'''
Created on Jul 15, 2012

@author: huhe
'''

from lib import Util
from isp.element import Element
from isp import XPath

class Pod(Element):
    
    _catalogServiceOfferingType = 'pod'
    
    def __init__(self, catalog, name=None, description=None, requestFileName='default-pod.xml', requestParams=None, catalogServiceOfferingName=None, catalogLinkTitle=None):
        self.logger = Util.getLogger(self.__class__.__name__)
        Element.__init__(self)
        Element.setCatalogMatchParameter(self, Pod._catalogServiceOfferingType, catalogServiceOfferingName, catalogLinkTitle)
        Element.setCreateParameter(self, name, description, requestFileName, requestParams)        
        Element.parseCatalog(self, catalog)
        
            
    # pod doesn't have catalog
    def getCatalog(self):
        return None
    
    
    def getInfrastructureIpAddressPoolUid(self):
        ipAddressPool = Util.getXpathValue(self.detailXml, XPath._LinkProviderInfrastructureIpAddressPool)
        self.logger.info('infrastructure ip address pool: ' + ipAddressPool)
        return ipAddressPool
            

    def getParameterStringValueByName(self, parameterName):
        xpath = XPath._PodStringTypeValue
        xpath = xpath.replace('${parameter-name}', parameterName)
        parameterValue = Util.getXpathValue(self.createTaskXml, xpath)
        return parameterValue
    
    def getVlanRange(self):
        vlanRangeStart = Util.getXpathValue(self.createTaskXml, XPath._PodVlanRangeStart)
        vlanRangeEnd   = Util.getXpathValue(self.createTaskXml, XPath._PodVlanRangeEnd)
        return [vlanRangeStart, vlanRangeEnd]
        
        