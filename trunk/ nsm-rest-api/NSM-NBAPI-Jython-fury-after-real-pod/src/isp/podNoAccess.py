'''
Created on Jul 15, 2012

@author: huhe
'''

from lib import Util
from isp.element import Element
from isp import XPath
from isp.pod import Pod


class PodNoAccess(Pod):
    
    _catalogServiceOfferingName = 'VMDC 2.1 Collapsed Compact POD with Edge Routers and no L2 Access Switches'
    _catalogLinkTitle = 'VMDC 2.1 Collapsed Compact POD with Edge Routers and no L2 Access Switches'
    
    
    def __init__(self, catalog, name=None, description=None, requestFileName='default-pod-no-access.xml', requestParams=None):
        Pod.__init__(self, catalog, name, description, requestFileName, requestParams, PodNoAccess._catalogServiceOfferingName, PodNoAccess._catalogLinkTitle)
        
        
        
        