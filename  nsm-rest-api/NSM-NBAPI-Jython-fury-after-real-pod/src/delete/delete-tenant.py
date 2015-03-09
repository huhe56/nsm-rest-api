'''
Created on Jul 15, 2012

@author: huhe
'''

import simplejson as json

import sys
from pprint import pprint

from lib import Util
from isp import Define
from isp import XPath
from isp.nsmUtil import NsmUtil
from isp.element import Element
from isp.nsmV1 import NsmV1
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


if __name__ == '__main__':
    
    NsmUtil.mkPresetDir()
    
    logger = Util.getLogger(__file__)
    descriptionPrefix = 'This is the description of '
    
    name = 'My Default NSM V1'
    myNsmV1 = NsmV1(None, name)
    myNsmV1.setOnLine()
    myNsmV1.create('001')
    myNsmV1Catalog = myNsmV1.getCatalog('201')
    myNsmV1ProviderList = myNsmV1.getProviderList('301')
    
    firstProviderUidUrl =  Util.getXpathValue(myNsmV1ProviderList, XPath._DetailFirstUidFromList)
    print firstProviderUidUrl
    
    tenantListUrl = firstProviderUidUrl + '/tenant'
    print tenantListUrl

    tenantListXml = NsmUtil.getRequest(tenantListUrl)
    print tenantListXml

    firstTenantUidUrl =  Util.getXpathValue(tenantListXml, XPath._DetailFirstUidFromList)
    print firstTenantUidUrl
    
    name = 'My Default Tenant'
    myTenant = Tenant(None, name, None)
    myTenant.setOnLine()
    myTenant.setUid(firstTenantUidUrl)
    myTenant.delete('501')
    
    NsmUtil.printHeadLine1('Delete tenant completed')
    
    
    