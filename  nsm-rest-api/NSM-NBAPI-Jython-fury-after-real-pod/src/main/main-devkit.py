'''
Created on Jul 15, 2012

@author: huhe
'''

import simplejson as json

import sys
from pprint import pprint

from lib import Util
from isp import Define
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
    
    logger = Util.getLogger(__file__)
    descriptionPrefix = 'This is the description of '
    
    name = 'My Default NSM V1'
    myNsmV1 = NsmV1(None, name)
    myNsmV1.setOnLine()
    myNsmV1.create()
    myNsmV1Catalog = myNsmV1.getCatalog()
    
    name = 'My Default Top'
    myTop = Top(myNsmV1Catalog, name)
    myTop.setOnLine()
    myTop.create()
    myTopCatalog = myTop.getCatalog()
    
    name = 'My Default Provider'
    description =  descriptionPrefix + name 
    requestParams = {
        'global.pool.subnet.1.ipv4': '179.0.0.0',
        'global.pool.subnet.1.mask': '20',
        'infastructure.pool.subnet.1.ipv4': '129.0.0.0',
        'infastructure.pool.subnet.1.mask': '20',
    }
    myProvider = Provider(myTopCatalog, name, description)
    myProvider.setRequestBodyParams(requestParams)
    myProvider.setOnLine()
    
    ### it is for dev kit only start
    ### comment out 
    # myProvider.create()
    # myProviderDetailXml = myProvider.getDetail()
    ### add
    myProvider.uid = 'https://od-c3-nsve:8443/NetworkServicesManagerAPI/v1/provider/bf0b484f221447569ffe29b12040ab08'
    myProviderDetailXml = myProvider.getDetail()
    ### it is for dev kit only end
    myProviderCatalogXml = myProvider.getCatalog()
    
    tempList = myProvider.uid.split('/')
    getProviderListUrl = '/'.join(tempList[:-2])
    getProviderListUrl += '/top/provider'
    providerListFileName = myProvider.createName.replace(' ', '-')
    responseFilePath = Define._PathResponseCreateDefault + '/' + providerListFileName + '-list.xml'
    logger.info('write provider list to file ' + responseFilePath)
    myProviderListXml = myProvider.getList(getProviderListUrl, responseFilePath)

    
    name = 'POD1'
    description =  descriptionPrefix + name
    myPod = Pod(myProviderCatalogXml, name, description)
    myPod.setOnLine()
    
    #myPod.create()
    myPod.uid = 'https://od-c3-nsve:8443/NetworkServicesManagerAPI/v1/pod/0dcb467d401846e993b3488cc205dfed'
    myPodDetailXml = myPod.getDetail()
    
    
    myPodListUrl = myProvider.uid + '/pod'
    myPodListFileName = myPod.createName.replace(' ', '-')
    responseFilePath = Define._PathResponseCreateDefault + '/' + myPodListFileName + '-list.xml'
    logger.info('write pod list to file ' + responseFilePath)
    myPodListXml = myProvider.getList(myPodListUrl, responseFilePath)

    
    ############
    #sys.exit()
    ############
    
    '''
    myGlobalIpAddressPoolUid = myProvider.getGlobalIpAddressPoolUid()
    myGlobalIpAddressPool = IpAddressPool(myGlobalIpAddressPoolUid, 'Provider', 'Global')
    myGlobalIpAddressPool.setOnLine()
    myGlobalIpAddressPoolDetail = myGlobalIpAddressPool.getDetail()
    
    name = 'My Default IP Address of Global Reservation Count'
    description = descriptionPrefix + name
    owner = 'My Owner'
    requestParams = {
        'owner': owner,
        'count': '4',
    }
    myIpReservationCount = IpReservation(myGlobalIpAddressPoolDetail, name, description, 'default-ip-reservation-count.xml', requestParams)
    myIpReservationCount.setOnLine()
    myIpReservationCount.create()
    myIpReservationCount.getDetail()
    myIpReservationCount.getAllocated()
    myIpReservationCount.getAvailable()
    myIpReservationCount.getReservations()
    
    
    myInfrastructureIpAddressPoolUid = myProvider.getInfrastructureIpAddressPoolUid()
    myInfrastructureIpAddressPool = IpAddressPool(myInfrastructureIpAddressPoolUid, 'Provider', 'Infrastructure')
    myInfrastructureIpAddressPool.setOnLine()
    myInfrastructureIpAddressPoolDetail = myInfrastructureIpAddressPool.getDetail()
    
    name = 'My Default IP Address of Infrastructure Reservation Range'
    description = descriptionPrefix + name
    owner = 'My Owner'
    requestParams = {
        'owner': owner,
        'ipv4AddressRange.1.ipv4.start': '129.0.0.200',
        'ipv4AddressRange.1.ipv4.end': '129.0.0.210'
    }
    myIpReservationRange = IpReservation(myInfrastructureIpAddressPoolDetail, name, description, 'default-ip-reservation-range.xml', requestParams)
    myIpReservationRange.setOnLine()
    myIpReservationRange.create()
    myIpReservationRange.getDetail()
    myIpReservationRange.getAllocated()
    myIpReservationRange.getAvailable()
    myIpReservationRange.getReservations()

    '''
    ############
    #sys.exit()
    ############

    name = 'My Default Tenant'
    description =  descriptionPrefix + name
    requestParams = {
        'routable.private.address.pool.subnet.1.ipv4': '192.168.0.0',
        'routable.private.address.pool.subnet.1.mask': '16',
    }
    myTenant = Tenant(myProviderCatalogXml, name, description)
    myTenant.setRequestBodyParams(requestParams)
    myTenant.setOnLine()
    myTenant.create()
    myTenantDetailXml = myTenant.getDetail()
    myTenantCatalogXml = myTenant.getCatalog()
    myTenantRoutablePrivateIpAddressPoolUid = myTenant.getRoutablePrivateIpAddressPoolUid()
    
    name = 'My Default Tenant Network Container'
    description =  descriptionPrefix + name
    requestParams = {'tnc.pod.uid': myPod.uid}
    myTNC = TenantNetworkContainer(myTenantCatalogXml, name, description)
    myTNC.setRequestBodyParams(requestParams)
    myTNC.setOnLine()
    myTNC.create()
    myTncDetailXml = myTNC.getDetail()
    myTncCatalogXml = myTNC.getCatalog()
    
    
    
    name = 'My Default Internet External Network'
    description =  descriptionPrefix + name
    requestParams = {
        'external.subnet.1.ipv4': '89.48.0.0',
        'external.subnet.1.mask': '18',
    }
    myExternalNetwork = ExternalNetwork(myTenantCatalogXml, name, description)
    myExternalNetwork.setRequestBodyParams(requestParams)
    myExternalNetwork.setOnLine()
    myExternalNetwork.create()
    myExternalNetworkDetailXml = myExternalNetwork.getDetail()
    myExternalNetworkCatalogXml = myExternalNetwork.getCatalog()
    
    name = 'My Default Internet Edge Zone'
    description =  descriptionPrefix + name
    myInternetZone = InternetEdgeZone(myTncCatalogXml, name, description)
    myInternetZone.setOnLine()
    myInternetZone.create()
    myInternetZoneDetailXml = myInternetZone.getDetail()
    myInternetZoneCatalogXml = myInternetZone.getCatalog()
    
    name = 'My Default Internet Edge Zone Layer 3 VLAN'
    description =  descriptionPrefix + name
    requestParams = {'l3.vlan.netmask': '28'}
    myInternetZoneL3Vlan = Layer3ExternalAccessVlan(myInternetZoneCatalogXml, name, description)
    myInternetZoneL3Vlan.setRequestBodyParams(requestParams)
    myInternetZoneL3Vlan.setOnLine()
    myInternetZoneL3Vlan.create()
    myInternetZoneL3VlanDetailXml = myInternetZoneL3Vlan.getDetail()
    myInternetZoneL3VlanCatalogXml = myInternetZoneL3Vlan.getCatalog()
    
    name = 'My Default Internet External Connection'
    description =  descriptionPrefix + name
    requestParams = {
        'external.networks.1.uid': myExternalNetwork.uid,
        'assigned.zone.uid': myInternetZone.uid,
    }
    myPublicENC = ExternalConnection(myTncCatalogXml, name, description)
    myPublicENC.setRequestBodyParams(requestParams)
    myPublicENC.setOnLine()
    myPublicENC.create()
    myPublicEncDetailXml = myPublicENC.getDetail()
    myPublicEncCatalogXml = myPublicENC.getCatalog()
    
    name = 'My Default Secured Internet Edge Zone'
    description =  descriptionPrefix + name
    mySecuredInternetZone = SecuredInternetEdgeZone(myTncCatalogXml, name, description)
    mySecuredInternetZone.setOnLine()
    mySecuredInternetZone.create()
    mySecuredInternetZoneDetailXml = mySecuredInternetZone.getDetail()
    mySecuredInternetZoneCatalogXml = mySecuredInternetZone.getCatalog()
    
    name = 'My Default Secured Internet Edge Zone Layer 3 VLAN'
    description =  descriptionPrefix + name
    requestParams = {'l3.vlan.netmask': '28'}
    mySecuredInternetZoneL3Vlan = Layer3ExternalAccessVlan(mySecuredInternetZoneCatalogXml, name, description)
    mySecuredInternetZoneL3Vlan.setRequestBodyParams(requestParams)
    mySecuredInternetZoneL3Vlan.setOnLine()
    mySecuredInternetZoneL3Vlan.create()
    DetailXml = mySecuredInternetZoneL3Vlan.getDetail()
    mySecuredInternetZoneL3VlanCatalogXml = mySecuredInternetZoneL3Vlan.getCatalog()
    
    name = 'My Default Internet Firewall Service between Secured and Unsecured Zone'
    description =  descriptionPrefix + name
    requestParams = {
        'traffic.src.filter.1.uid': mySecuredInternetZoneL3Vlan.uid,
        'traffic.dst.filter.1.uid': myInternetZoneL3Vlan.uid,
        'fw.service.1.protocol': 'tcp',
        'fw.service.1.port.start': '80',
        'fw.service.1.port.end': '80',
    }
    myFirewallService1 = FirewallService(myTenantCatalogXml, name, description)
    myFirewallService1.setRequestBodyParams(requestParams)
    myFirewallService1.setOnLine()
    myFirewallService1.create()
    myFirewallServiceDetailXml1 = myFirewallService1.getDetail()
    FirewallServiceCatalogXml1 = myFirewallService1.getCatalog()
    
    name = 'My Default Internet Firewall Service Between Secured and External Network'
    description =  descriptionPrefix + name
    requestParams = {
        'traffic.src.filter.1.uid': myExternalNetwork.uid,
        'traffic.dst.filter.1.uid': mySecuredInternetZoneL3Vlan.uid,
        'fw.service.1.protocol': 'tcp',
        'fw.service.1.port.start': '80',
        'fw.service.1.port.end': '80',
    }
    myFirewallService2 = FirewallService(myTenantCatalogXml, name, description)
    myFirewallService2.setRequestBodyParams(requestParams)
    myFirewallService2.setOnLine()
    myFirewallService2.create()
    myFirewallServiceDetailXml2 = myFirewallService2.getDetail()
    FirewallServiceCatalogXml2 = myFirewallService2.getCatalog()
    
    
    
    
    name = 'My Default Private External Network'
    description =  descriptionPrefix + name
    requestParams = {
        'external.subnet.1.ipv4': '10.68.0.0',
        'external.subnet.1.mask': '18',
    }
    myPrivateExternalNetwork = ExternalNetwork(myTenantCatalogXml, name, description)
    myPrivateExternalNetwork.setRequestBodyParams(requestParams)
    myPrivateExternalNetwork.setOnLine()
    myPrivateExternalNetwork.create()
    myExternalNetworkDetailXml = myPrivateExternalNetwork.getDetail()
    myExternalNetworkCatalogXml = myPrivateExternalNetwork.getCatalog()
    
    name = 'My Default Private Edge Zone'
    description =  descriptionPrefix + name
    myPrivateZone = PrivateEdgeZone(myTncCatalogXml, name, description)
    myPrivateZone.setOnLine()
    myPrivateZone.create()
    myPrivateZoneDetailXml = myPrivateZone.getDetail()
    myPrivateZoneCatalogXml = myPrivateZone.getCatalog()
    
    name = 'My Default Private Zone Layer 3 VLAN'
    description =  descriptionPrefix + name
    requestParams = {'l3.vlan.netmask': '28'}
    myPrivateZoneL3Vlan = Layer3PrivateAccessVlan(myPrivateZoneCatalogXml, name, description)
    myPrivateZoneL3Vlan.setRequestBodyParams(requestParams)
    myPrivateZoneL3Vlan.setOnLine()
    myPrivateZoneL3Vlan.create()
    myPrivateZoneL3VlanDetailXml = myPrivateZoneL3Vlan.getDetail()
    myPrivateZoneL3VlanCatalogXml = myPrivateZoneL3Vlan.getCatalog()
    
    name = 'My Default Private MPLS Connection'
    description =  descriptionPrefix + name
    requestParams = {
        'external.networks.1.uid': myPrivateExternalNetwork.uid,
        'assigned.zone.uid': myPrivateZone.uid,
        'mpls.export.routes.routeTarget.1.ipv4': '10.50.0.0',
        'mpls.export.routes.routeTarget.1.ASNumber': '6500',
        'mpls.import.routes.routeTarget.1.ipv4': '10.40.0.0',
        'mpls.import.routes.routeTarget.1.ASNumber': '6500',
    }
    myPrivateENC = PrivateMplsConnection(myTncCatalogXml, name, description)
    myPrivateENC.setRequestBodyParams(requestParams)
    myPrivateENC.setOnLine()
    myPrivateENC.create()
    myPrivateEncDetailXml = myPrivateENC.getDetail()
    myPrivateEncCatalogXml = myPrivateENC.getCatalog()


    name = 'My Default Secured Private Edge Zone'
    description =  descriptionPrefix + name
    mySecuredPrivateZone = SecuredPrivateEdgeZone(myTncCatalogXml, name, description)
    mySecuredPrivateZone.setOnLine()
    mySecuredPrivateZone.create()
    mySecuredPrivateZoneDetailXml = mySecuredPrivateZone.getDetail()
    mySecuredPrivateZoneCatalogXml = mySecuredPrivateZone.getCatalog()
    
    
    name = 'My Default Secured Private Zone Layer 3 VLAN'
    description =  descriptionPrefix + name
    requestParams = {'l3.vlan.netmask': '28'}
    mySecuredPrivateZoneL3Vlan = Layer3PrivateAccessVlan(mySecuredPrivateZoneCatalogXml, name, description)
    mySecuredPrivateZoneL3Vlan.setRequestBodyParams(requestParams)
    mySecuredPrivateZoneL3Vlan.setOnLine()
    mySecuredPrivateZoneL3Vlan.create()
    mySecuredPrivateZoneL3VlanDetailXml = mySecuredPrivateZoneL3Vlan.getDetail()
    mySecuredPrivateZoneL3VlanCatalogXml = mySecuredPrivateZoneL3Vlan.getCatalog()
    
    
    name = 'My Default Private Firewall Service Between Secured and Unsecured Zone'
    description =  descriptionPrefix + name
    requestParams = {
        'traffic.src.filter.1.uid': mySecuredPrivateZoneL3Vlan.uid,
        'traffic.dst.filter.1.uid': myPrivateZoneL3Vlan.uid,
        'fw.service.1.protocol': 'tcp',
        'fw.service.1.port.start': '80',
        'fw.service.1.port.end': '80',
    }
    myFirewallService3 = FirewallService(myTenantCatalogXml, name, description)
    myFirewallService3.setRequestBodyParams(requestParams)
    myFirewallService3.setOnLine()
    myFirewallService3.create()
    myFirewallServiceDetailXml3 = myFirewallService3.getDetail()
    FirewallServiceCatalogXml3 = myFirewallService3.getCatalog()
    
    
    name = 'My Default Private Firewall Service Between Secured and External Network'
    description =  descriptionPrefix + name
    requestParams = {
        'traffic.src.filter.1.uid': myPrivateExternalNetwork.uid,
        'traffic.dst.filter.1.uid': mySecuredPrivateZoneL3Vlan.uid,
        'fw.service.1.protocol': 'tcp',
        'fw.service.1.port.start': '80',
        'fw.service.1.port.end': '80',
    }
    myFirewallService4 = FirewallService(myTenantCatalogXml, name, description)
    myFirewallService4.setRequestBodyParams(requestParams)
    myFirewallService4.setOnLine()
    myFirewallService4.create()
    myFirewallServiceDetailXml4 = myFirewallService4.getDetail()
    FirewallServiceCatalogXml4 = myFirewallService4.getCatalog()
    
    
    
    logger.info('')
    line = ''
    for pair in Element._uidList:
        objectUid   = pair[0]
        objectClass = pair[1]
        objectName  = pair[2]
        logger.debug('uid: ' + objectUid + ' for class ' + objectClass + " and object " + objectName)
        line += objectUid + ';' + objectClass + ';' + objectName + "\n"
    Util.writeFile(Define._PathUidDefault, line)
        
    
    logger.info('')
    logger.info('================= creation complete successfully ==================')
    logger.info('')
    
    