'''
Created on Jul 15, 2012

@author: huhe
'''

from lib import Util
from isp import Define
from isp.element import Element
from isp.nsmUtil import NsmUtil


class LoadBalancerService(Element):
    
    _catalogServiceOfferingType = 'servicepolicy'
    _catalogServiceOfferingName = 'Load Balancer Service'
    _catalogLinkTitle = 'Load Balancer Service'
    
    
    def __init__(self, catalog, name=None, description=None, requestFileName='default-load-balancer-service.xml', requestParams=None):
        self.logger = Util.getLogger(self.__class__.__name__)
        Element.__init__(self)
        Element.setCatalogMatchParameter(self, LoadBalancerService._catalogServiceOfferingType, LoadBalancerService._catalogServiceOfferingName, LoadBalancerService._catalogLinkTitle)
        Element.setCreateParameter(self, name, description, requestFileName, requestParams)        
        Element.parseCatalog(self, catalog)     
        
   
    

