'''
Created on Jul 15, 2012

@author: huhe
'''

from lib import Util
from isp.element import Element
from isp import XPath
from isp.pod import Pod


class PodNoEdgeAccess(Pod):
    
    _catalogServiceOfferingName = 'VMDC 2.1 Collapsed Compact POD with no Edge Routers and no L2 Access Switches'
    _catalogLinkTitle = 'VMDC 2.1 Collapsed Compact POD with no Edge Routers and no L2 Access Switches'
    
    
    def __init__(self, catalog, name=None, description=None, requestFileName='default-pod-no-edge-access.xml', requestParams=None):
        Pod.__init__(self, catalog, name, description, requestFileName, requestParams, PodNoEdgeAccess._catalogServiceOfferingName, PodNoEdgeAccess._catalogLinkTitle)
        
