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
from isp.southZone import SouthZone
from isp.northZone import NorthZone
from isp.layer3ExplicitSubnet import Layer3ExplicitSubnet
from isp.providerNetworkContainer import ProviderNetworkContainer

if __name__ == '__main__':
 
    logger = Util.getLogger(__file__)
    
    fakeCatalogXml = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><root/>'
    content = Util.readFile(Define._PathUidDefault)
    lineList = content.split("\n")
    #print lineList
    index = 0
    for line in lineList:
        if line:
            index += 1
            items = line.split(';')
            objectUid   = items[0]
            objectClass = items[1]
            objectName  = items[2]
            print (str(index) + ': \t' + objectClass.ljust(32, ' ') + objectName.ljust(80, ' ') + objectUid)
            
    inputIndex = 0
    try:
        inputIndex = int(raw_input('\nwhich one to delete? please input a number: '))
    except ValueError:
        print 'Not a number, abort'
            
    index = 0
    newLines = ''
    for line in lineList:
        if line:
            index += 1
            if index == inputIndex:
                items = line.split(';')
                objectUid   = items[0]
                objectClass = items[1]
                objectName  = '[' + items[2] + ']'
                print (str(index) + ': \t' + objectClass.ljust(28, ' ') + objectName.ljust(80, ' ') + objectUid)
                inputYes = raw_input('\npress y to confirm ... ')
                if inputYes == 'y' or inputYes == 'Y':
                    myObject = eval(objectClass)(fakeCatalogXml, objectName, None, None, None)
                    myObject.setUid(objectUid)
                    myObject.setOnLine()
                    result = myObject.delete('999')
                    if result:
                        lineList.remove(line)
                        logger.info('-------------------> Delete Result: PASSED')
                    else:
                        logger.info('-------------------> Delete Result: FAILED')
                    break
                else:
                    print 'input is not confirmed, skip ...'
        newLines += line + '\n'
    Util.writeFile(Define._PathUidDefault, newLines)        
        
        
        