'''
Created on Jul 27, 2012

@author: huhe
'''

from lib import Util
from isp import Define

from lib import Util
from isp import Define
from isp.element import Element
from isp.top import Top
from isp.provider import Provider
from isp.pod import Pod
from isp.tenant import Tenant
from isp.externalNetwork import ExternalNetwork
from isp.tenantNetworkContainer import TenantNetworkContainer
from isp.internetEdgeZone import InternetEdgeZone
from isp.layer3ExternalAccessVlan import Layer3ExternalAccessVlan
from isp.externalConnection import ExternalConnection
from isp.securedInternetEdgeZone import SecuredInternetEdgeZone
from isp.firewallService import FirewallService
from isp.privateEdgeZone import PrivateEdgeZone
from isp.layer3PrivateAccessVlan import Layer3PrivateAccessVlan
from isp.privateMplsConnection import PrivateMplsConnection
from isp.securedPrivateEdgeZone import SecuredPrivateEdgeZone
from isp.ipAddressPool import IpAddressPool
from isp.ipReservation import IpReservation
from isp.loadBalancerService import LoadBalancerService
from isp.dynamicPatService import DynamicPatService
from isp.staticNatService import StaticNatService
from isp.staticNatPortRedirectionService import StaticNatPortRedirectionService

if __name__ == '__main__':
 
    logger = Util.getLogger(__file__)
    
    fakeCatalogXml = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><root/>'
    content = Util.readFile(Define._PathUidDefault)
    lineList = content.split("\n")
    #print lineList
    for line in reversed(lineList):
        if line:
            items = line.split(';')
            print items
            objectUid   = items[0]
            objectClass = items[1]
            objectName  = items[2]
            ### will do these three afterwards
            if objectClass != 'Top' and objectClass != 'Provider' and objectClass != 'Pod':
                myObject = eval(objectClass)(fakeCatalogXml, objectName, None, None, None)
                myObject.setUid(objectUid)
                myObject.setOnLine()
                result = myObject.delete('888')
                if result:
                    logger.info('-------------------> Delete Result: PASSED')
                else:
                    logger.info('-------------------> Delete Result: FAILED')
        
        
        
        