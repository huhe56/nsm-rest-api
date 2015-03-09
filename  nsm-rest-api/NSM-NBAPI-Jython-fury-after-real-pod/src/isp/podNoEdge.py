'''
Created on Jul 15, 2012

@author: huhe
'''

from lib import Util
from isp.element import Element
from isp import XPath
from isp.pod import Pod


class PodNoEdge(Pod):
    
    _catalogServiceOfferingType = 'pod'
    _catalogServiceOfferingName = 'VMDC 2.1 Compact POD with no Edge Routers'
    _catalogLinkTitle = 'VMDC 2.1 Compact POD with no Edge Routers'
    
    
    def __init__(self, catalog, name=None, description=None, requestFileName='default-pod-no-edge.xml', requestParams=None):
        Pod.__init__(self, catalog, name, description, requestFileName, requestParams, PodNoEdge._catalogServiceOfferingName, PodNoEdge._catalogLinkTitle)
        
        
        
        