'''
Created on Jul 15, 2012

@author: huhe
'''

from lib import Util
from isp.element import Element
from isp import XPath
from isp.pod import Pod


class PodFury(Pod):
    
    _catalogServiceOfferingName = 'Telstra POD with ASA 5585 Firewalls'
    _catalogLinkTitle = 'Telstra POD with ASA 5585 Firewalls'
    
    
    def __init__(self, catalog, name=None, description=None, requestFileName='default-pod-full.xml', requestParams=None):
        Pod.__init__(self, catalog, name, description, requestFileName, requestParams, PodFury._catalogServiceOfferingName, PodFury._catalogLinkTitle)
        
        
