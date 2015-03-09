'''
Created on Jul 15, 2012

@author: huhe
'''

import simplejson as json

import sys
from pprint import pprint

from lib import Util
from isp import Define
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
from isp.loadBalancerService import LoadBalancerService
from isp.dynamicPatService import DynamicPatService
from isp.staticNatService import StaticNatService
from isp.staticNatPortRedirectionService import StaticNatPortRedirectionService


if __name__ == '__main__':
    
    NsmUtil.mkPresetDir()
    
    logger = Util.getLogger(__file__)
    descriptionPrefix = 'This is the description of '
    
    name = 'My Default NSM V1'
    myNsmV1 = NsmV1(None, name)
    myNsmV1.setOffLine()
    myNsmV1.create('001')
    myNsmV1Catalog = myNsmV1.getCatalog('201')
    myNsmV1ProviderList = myNsmV1.getProviderList('301')
    
    name = 'My Default Top'
    myTop = Top(myNsmV1Catalog, name)
    myTop.setOffLine()
    myTop.create('001')
    myTopCatalog = myTop.getCatalog('201')
    
    
    name = 'My Default Provider'
    description =  descriptionPrefix + name 
    requestParams = {
        'global.pool.subnet.1.ipv4': '179.0.0.0',
        'global.pool.subnet.1.mask': '20',
    }
    myProvider = Provider(myTopCatalog, name, description)
    myProvider.setRequestBodyParams(requestParams)
    myProvider.setOffLine()
    myProvider.create('001')
    myProviderDetailXml = myProvider.getDetail('101')
    myProviderCatalogXml = myProvider.getCatalog('201')
    
    myNsmV1ProviderList = myNsmV1.getProviderList('301')
    myProvider.getPodList('301')
    
    
    name = 'My Default Pod'
    description =  descriptionPrefix + name
    requestParams = {
        'infrastructure.pool.subnet.1.ipv4': '129.0.0.0',
        'infrastructure.pool.subnet.1.mask': '20',
    }
    myPod = Pod(myProviderCatalogXml, name, description)
    myPod.setOffLine()
    myPod.create('001')
    myPodDetailXml = myPod.getDetail('101')
    
    myProvider.getPodList('311')
        
    
    ############
    #sys.exit()
    ############
    
    name = 'My Default IP Address Pool of Provider Global'
    myGlobalIpAddressPoolUid = myProvider.getGlobalIpAddressPoolUid()
    myGlobalIpAddressPool = IpAddressPool(myGlobalIpAddressPoolUid, name, 'Provider', 'Global')
    myGlobalIpAddressPool.setOffLine()
    myGlobalIpAddressPoolDetail = myGlobalIpAddressPool.getDetail('101')
    myGlobalIpAddressPool.getAllocated('101')
    myGlobalIpAddressPool.getAvailable('101')
    myGlobalIpAddressPool.getReservations('101')
    
    
    name = 'My Default IP Address of Global Reservation Count'
    description = descriptionPrefix + name
    owner = 'My Owner'
    requestParams = {
        'owner': owner,
        'count': '4',
    }
    myIpReservationCount = IpReservation(myGlobalIpAddressPoolDetail, name, description, 'default-ip-reservation-count.xml', requestParams)
    myIpReservationCount.setOffLine()
    myIpReservationCount.create('011')
    myIpReservationCount.getDetail('111')
    myIpReservationCount.getAllocated('111')
    myIpReservationCount.getAvailable('111')
    myIpReservationCount.getReservations('111')
    
    
    name = 'My Default IP Address Pool of Provider Infrastructure'
    myInfrastructureIpAddressPoolUid = myProvider.getInfrastructureIpAddressPoolUid()
    myInfrastructureIpAddressPool = IpAddressPool(myInfrastructureIpAddressPoolUid, name, 'Provider', 'Infrastructure')
    myInfrastructureIpAddressPool.setOffLine()
    myInfrastructureIpAddressPoolDetail = myInfrastructureIpAddressPool.getDetail('101')
    myInfrastructureIpAddressPool.getAllocated('101')
    myInfrastructureIpAddressPool.getAvailable('101')
    myInfrastructureIpAddressPool.getReservations('101')
    
    name = 'My Default IP Address of Infrastructure Reservation Range'
    description = descriptionPrefix + name
    owner = 'My Owner'
    requestParams = {
        'owner': owner,
        'ipv4AddressRange.1.ipv4.start': '129.0.0.200',
        'ipv4AddressRange.1.ipv4.end': '129.0.0.210'
    }
    myIpReservationRange = IpReservation(myInfrastructureIpAddressPoolDetail, name, description, 'default-ip-reservation-range.xml', requestParams)
    myIpReservationRange.setOffLine()
    myIpReservationRange.create('011')
    myIpReservationRange.getDetail('111')
    myIpReservationRange.getAllocated('111')
    myIpReservationRange.getAvailable('111')
    myIpReservationRange.getReservations('111')
    
    
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
    myTenant.setOffLine()
    myTenant.create('001')
    myTenantDetailXml = myTenant.getDetail('101')
    myTenantCatalogXml = myTenant.getCatalog('201')
    myTenantRoutablePrivateIpAddressPoolUid = myTenant.getRoutablePrivateIpAddressPoolUid()
    
    name = 'My Default Tenant Network Container'
    description =  descriptionPrefix + name
    requestParams = {'tnc.pod.uid': myPod.uid}
    myTNC = TenantNetworkContainer(myTenantCatalogXml, name, description)
    myTNC.setRequestBodyParams(requestParams)
    myTNC.setOffLine()
    myTNC.create('001')
    myTncDetailXml = myTNC.getDetail('101')
    myTncCatalogXml = myTNC.getCatalog('201')
    
    
    
    name = 'My Default Internet External Network'
    description =  descriptionPrefix + name
    requestParams = {
        'external.subnet.1.ipv4': '89.48.0.0',
        'external.subnet.1.mask': '18',
    }
    myExternalNetwork = ExternalNetwork(myTenantCatalogXml, name, description)
    myExternalNetwork.setRequestBodyParams(requestParams)
    myExternalNetwork.setOffLine()
    myExternalNetwork.create('001')
    myExternalNetworkDetailXml = myExternalNetwork.getDetail('101')
    myExternalNetworkCatalogXml = myExternalNetwork.getCatalog('201')
    
    name = 'My Default Internet Edge Zone'
    description =  descriptionPrefix + name
    myInternetZone = InternetEdgeZone(myTncCatalogXml, name, description)
    myInternetZone.setOffLine()
    myInternetZone.create('001')
    myInternetZoneDetailXml = myInternetZone.getDetail('101')
    myInternetZoneCatalogXml = myInternetZone.getCatalog('201')
    
    name = 'My Default Internet Edge Zone Layer 3 VLAN'
    description =  descriptionPrefix + name
    requestParams = {'l3.vlan.netmask': '28'}
    myInternetZoneL3Vlan = Layer3ExternalAccessVlan(myInternetZoneCatalogXml, name, description)
    myInternetZoneL3Vlan.setRequestBodyParams(requestParams)
    myInternetZoneL3Vlan.setOffLine()
    myInternetZoneL3Vlan.create('001')
    myInternetZoneL3VlanDetailXml = myInternetZoneL3Vlan.getDetail('101')
    myInternetZoneL3VlanCatalogXml = myInternetZoneL3Vlan.getCatalog('201')
    
    name = 'My Default Internet External Connection'
    description =  descriptionPrefix + name
    requestParams = {
        'external.networks.1.uid': myExternalNetwork.uid,
        'assigned.zone.uid': myInternetZone.uid,
    }
    myPublicENC = ExternalConnection(myTncCatalogXml, name, description)
    myPublicENC.setRequestBodyParams(requestParams)
    myPublicENC.setOffLine()
    myPublicENC.create('001')
    myPublicEncDetailXml = myPublicENC.getDetail('101')
    myPublicEncCatalogXml = myPublicENC.getCatalog('201')
    
    name = 'My Default Secured Internet Edge Zone'
    description =  descriptionPrefix + name
    mySecuredInternetZone = SecuredInternetEdgeZone(myTncCatalogXml, name, description)
    mySecuredInternetZone.setOffLine()
    mySecuredInternetZone.create('001')
    mySecuredInternetZoneDetailXml = mySecuredInternetZone.getDetail('101')
    mySecuredInternetZoneCatalogXml = mySecuredInternetZone.getCatalog('201')
    
    name = 'My Default Secured Internet Edge Zone Layer 3 VLAN'
    description =  descriptionPrefix + name
    requestParams = {'l3.vlan.netmask': '28'}
    mySecuredInternetZoneL3Vlan = Layer3ExternalAccessVlan(mySecuredInternetZoneCatalogXml, name, description)
    mySecuredInternetZoneL3Vlan.setRequestBodyParams(requestParams)
    mySecuredInternetZoneL3Vlan.setOffLine()
    mySecuredInternetZoneL3Vlan.create('001')
    DetailXml = mySecuredInternetZoneL3Vlan.getDetail('101')
    mySecuredInternetZoneL3VlanCatalogXml = mySecuredInternetZoneL3Vlan.getCatalog('201')
    
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
    myFirewallService1.setOffLine()
    myFirewallService1.create('001')
    myFirewallServiceDetailXml1 = myFirewallService1.getDetail('101')
    FirewallServiceCatalogXml1 = myFirewallService1.getCatalog('201')
    
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
    myFirewallService2.setOffLine()
    myFirewallService2.create('001')
    myFirewallServiceDetailXml2 = myFirewallService2.getDetail('101')
    FirewallServiceCatalogXml2 = myFirewallService2.getCatalog('201')
    
    
    
    
    name = 'My Default Private External Network'
    description =  descriptionPrefix + name
    requestParams = {
        'external.subnet.1.ipv4': '10.68.0.0',
        'external.subnet.1.mask': '18',
    }
    myPrivateExternalNetwork = ExternalNetwork(myTenantCatalogXml, name, description)
    myPrivateExternalNetwork.setRequestBodyParams(requestParams)
    myPrivateExternalNetwork.setOffLine()
    myPrivateExternalNetwork.create('001')
    myExternalNetworkDetailXml = myPrivateExternalNetwork.getDetail('101')
    myExternalNetworkCatalogXml = myPrivateExternalNetwork.getCatalog('201')
    
    name = 'My Default Private Edge Zone'
    description =  descriptionPrefix + name
    myPrivateZone = PrivateEdgeZone(myTncCatalogXml, name, description)
    myPrivateZone.setOffLine()
    myPrivateZone.create('001')
    myPrivateZoneDetailXml = myPrivateZone.getDetail('101')
    myPrivateZoneCatalogXml = myPrivateZone.getCatalog('201')
    
    name = 'My Default Private Edge Zone Layer 3 VLAN'
    description =  descriptionPrefix + name
    requestParams = {'l3.vlan.netmask': '28'}
    myPrivateZoneL3Vlan = Layer3PrivateAccessVlan(myPrivateZoneCatalogXml, name, description)
    myPrivateZoneL3Vlan.setRequestBodyParams(requestParams)
    myPrivateZoneL3Vlan.setOffLine()
    myPrivateZoneL3Vlan.create('001')
    myPrivateZoneL3VlanDetailXml = myPrivateZoneL3Vlan.getDetail('101')
    myPrivateZoneL3VlanCatalogXml = myPrivateZoneL3Vlan.getCatalog('201')
    
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
    myPrivateENC.setOffLine()
    myPrivateENC.create('001')
    myPrivateEncDetailXml = myPrivateENC.getDetail('101')
    myPrivateEncCatalogXml = myPrivateENC.getCatalog('201')


    name = 'My Default Secured Private Edge Zone'
    description =  descriptionPrefix + name
    mySecuredPrivateZone = SecuredPrivateEdgeZone(myTncCatalogXml, name, description)
    mySecuredPrivateZone.setOffLine()
    mySecuredPrivateZone.create('001')
    mySecuredPrivateZoneDetailXml = mySecuredPrivateZone.getDetail('101')
    mySecuredPrivateZoneCatalogXml = mySecuredPrivateZone.getCatalog('201')
    
    
    name = 'My Default Secured Private Edge Zone Layer 3 VLAN'
    description =  descriptionPrefix + name
    requestParams = {'l3.vlan.netmask': '28'}
    mySecuredPrivateZoneL3Vlan = Layer3PrivateAccessVlan(mySecuredPrivateZoneCatalogXml, name, description)
    mySecuredPrivateZoneL3Vlan.setRequestBodyParams(requestParams)
    mySecuredPrivateZoneL3Vlan.setOffLine()
    mySecuredPrivateZoneL3Vlan.create('001')
    mySecuredPrivateZoneL3VlanDetailXml = mySecuredPrivateZoneL3Vlan.getDetail('101')
    mySecuredPrivateZoneL3VlanCatalogXml = mySecuredPrivateZoneL3Vlan.getCatalog('201')
    
    
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
    myFirewallService3.setOffLine()
    myFirewallService3.create('001')
    myFirewallServiceDetailXml3 = myFirewallService3.getDetail('101')
    FirewallServiceCatalogXml3 = myFirewallService3.getCatalog('201')
    
    
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
    myFirewallService4.setOffLine()
    myFirewallService4.create('001')
    myFirewallServiceDetailXml4 = myFirewallService4.getDetail('101')
    FirewallServiceCatalogXml4 = myFirewallService4.getCatalog('201')
    
    
    #############
    
    
    name = 'My Default IP Address Pool of Internet Edge Zone Layer 3 Vlan'
    myInternetZoneL3VlanSubPoolUid = myInternetZoneL3Vlan.getSubPoolUid()
    myInternetZoneL3VlanSubPool = IpAddressPool(myInternetZoneL3VlanSubPoolUid, name, 'Layer3ExternalAccessVlan', 'SubPool')
    myInternetZoneL3VlanSubPool.setOffLine()
    myInternetZoneL3VlanSubPoolDetail = myInternetZoneL3VlanSubPool.getDetail('101')
    myInternetZoneL3VlanSubPool.getAllocated('101')
    myInternetZoneL3VlanSubPool.getAvailable('101')
    myInternetZoneL3VlanSubPool.getReservations('101')
    
    
    
    name = 'My Default IP Address Reservation of Internet Edge Zone Layer 3 Vlan'
    description = descriptionPrefix + name
    requestParams = {
        'owner': 'My Default Internet Edge Zone Layer 3 Vlan Sub Pool Owner',
        'count': '8',
    }
    myInternetZoneIpReservationCount = IpReservation(myInternetZoneL3VlanSubPoolDetail, name, description, 'default-ip-reservation-count.xml', requestParams)
    myInternetZoneIpReservationCount.setOffLine()
    myInternetZoneIpReservationCount.create('011')
    myInternetZoneIpReservationCount.getDetail('111')
    myInternetZoneIpReservationCount.getAllocated('111')
    myInternetZoneIpReservationCount.getAvailable('111')
    reservationXml = myInternetZoneIpReservationCount.getReservations('111')
    internetZoneIpAddressReservationList = NsmUtil.getIpAddressListByReservation(reservationXml, 8)
    
    
    #sys.exit()
    
    name = 'My Default Load Balancer'
    description =  descriptionPrefix + name
    requestParams = {
        'traffic.src.filter.1.uid': myExternalNetwork.uid,
        'real.servers.trafficFilter.1.uid': myInternetZoneL3Vlan.uid,
        'real.servers.1.ipv4.start': internetZoneIpAddressReservationList[0],
        'real.servers.1.ipv4.end': internetZoneIpAddressReservationList[0],
        'real.servers.2.ipv4.start': internetZoneIpAddressReservationList[1],
        'real.servers.2.ipv4.end': internetZoneIpAddressReservationList[1],
        'real.servers.3.ipv4.start': internetZoneIpAddressReservationList[2],
        'real.servers.3.ipv4.end': internetZoneIpAddressReservationList[2],
        'lb.service.1.protocol': 'tcp',
        'lb.service.1.port.start': '80',
        'lb.service.1.port.end': '80',
        'vip.address.trafficFilter.uid': myInternetZone.uid,
        'vip.address.1.ipv4.start': internetZoneIpAddressReservationList[3],
        'vip.address.1.ipv4.end': internetZoneIpAddressReservationList[3],
        'lb.algorithm': 'roundrobin',
        'serverfarm.probe.1': 'icmp'
    }
    myLoadBalancerService = LoadBalancerService(myTenantCatalogXml, name, description)
    myLoadBalancerService.setRequestBodyParams(requestParams)
    myLoadBalancerService.setOffLine()
    myLoadBalancerService.create('001')
    myLoadBalancerService.getDetail('101')
    myLoadBalancerService.getCatalog('201')
    
    
    name = 'My Default Dynamic PAT Service Between Secured and External Network'
    description =  descriptionPrefix + name
    requestParams = {
        'traffic.src.filter.1.uid': mySecuredInternetZoneL3Vlan.uid,
        'traffic.dst.filter.1.uid': myExternalNetwork.uid,
        'mapped.address.uid': myInternetZone.uid,
        'mapped.address.1.ipv4.start': internetZoneIpAddressReservationList[7],
        'mapped.address.1.ipv4.end': internetZoneIpAddressReservationList[7],
    }
    myDynamicPat = DynamicPatService(myTenantCatalogXml, name, description)
    myDynamicPat.setRequestBodyParams(requestParams)
    myDynamicPat.setOffLine()
    myDynamicPat.create('001')
    myDynamicPatDetailXml = myFirewallService2.getDetail('101')
    myDynamicPatCatalogXml = myFirewallService2.getCatalog('201')
    
    
    #sys.exit()
    
    
    name = 'My Default IP Address Pool of Secured Internet Edge Zone Layer 3 Vlan'
    mySecuredInternetZoneL3VlanSubPoolUid = mySecuredInternetZoneL3Vlan.getSubPoolUid()
    mySecuredInternetZoneL3VlanSubPool = IpAddressPool(mySecuredInternetZoneL3VlanSubPoolUid, name, 'Layer3ExternalAccessVlan', 'SubPool')
    mySecuredInternetZoneL3VlanSubPool.setOffLine()
    mySecuredInternetZoneL3VlanSubPoolDetail = mySecuredInternetZoneL3VlanSubPool.getDetail('101')
    mySecuredInternetZoneL3VlanSubPool.getAllocated('101')
    mySecuredInternetZoneL3VlanSubPool.getAvailable('101')
    mySecuredInternetZoneL3VlanSubPool.getReservations('101')
    
    
    name = 'My Default IP Address Reservation of Secured Internet Edge Zone Layer 3 Vlan'
    description = descriptionPrefix + name
    requestParams = {
        'owner': 'My Default Secured Internet Edge Zone Layer 3 Vlan Sub Pool Owner',
        'count': '8',
    }
    mySecuredInternetZoneIpReservationCount = IpReservation(mySecuredInternetZoneL3VlanSubPoolDetail, name, description, 'default-ip-reservation-count.xml', requestParams)
    mySecuredInternetZoneIpReservationCount.setOffLine()
    mySecuredInternetZoneIpReservationCount.create('011')
    mySecuredInternetZoneIpReservationCount.getDetail('111')
    mySecuredInternetZoneIpReservationCount.getAllocated('111')
    mySecuredInternetZoneIpReservationCount.getAvailable('111')
    reservationXml = mySecuredInternetZoneIpReservationCount.getReservations('111')
    securedInternetZoneIpAddressReservationList = NsmUtil.getIpAddressListByReservation(reservationXml, 8)
    
    
    name = 'My Default Static NAT Service Between Secured and External Network'
    description =  descriptionPrefix + name
    requestParams = {
        'traffic.src.filter.uid': myExternalNetwork.uid,
        'traffic.dst.filter.uid': mySecuredInternetZoneL3Vlan.uid,
        'traffic.dst.1.ipv4.start': securedInternetZoneIpAddressReservationList[0],
        'traffic.dst.1.ipv4.end': securedInternetZoneIpAddressReservationList[0],
        'mapped.address.uid': myInternetZone.uid,
        'mapped.address.1.ipv4.start': internetZoneIpAddressReservationList[6],
        'mapped.address.1.ipv4.end': internetZoneIpAddressReservationList[6],
    }
    myStaticNat = StaticNatService(myTenantCatalogXml, name, description)
    myStaticNat.setRequestBodyParams(requestParams)
    myStaticNat.setOffLine()
    myStaticNat.create('001')
    myStaticNatDetailXml = myStaticNat.getDetail('101')
    myStaticNatCatalogXml = myStaticNat.getCatalog('201')
    
    
    name = 'My Default Static NAT Service with Port Redirection Between Secured and External Network'
    description =  descriptionPrefix + name
    requestParams = {
        'traffic.src.filter.uid': myExternalNetwork.uid,
        'traffic.dst.filter.uid': mySecuredInternetZoneL3Vlan.uid,
        'traffic.dst.1.ipv4.start': securedInternetZoneIpAddressReservationList[1],
        'traffic.dst.1.ipv4.end': securedInternetZoneIpAddressReservationList[1],
        'mapped.address.uid': myInternetZone.uid,
        'mapped.address.1.ipv4.start': internetZoneIpAddressReservationList[5],
        'mapped.address.1.ipv4.end': internetZoneIpAddressReservationList[5],
        'nat.service.ports.1.protocol': 'tcp',
        'nat.service.ports.1.start': '80',
        'nat.service.ports.1.redirect.port': '8080',
    }
    myStaticNatPortRedirection = StaticNatPortRedirectionService(myTenantCatalogXml, name, description)
    myStaticNatPortRedirection.setRequestBodyParams(requestParams)
    myStaticNatPortRedirection.setOnLine()
    myStaticNatPortRedirection.create('001')
    myStaticNatPortRedirectionDetailXml = myStaticNatPortRedirection.getDetail('101')
    myStaticNatPortRedirectionCatalogXml = myStaticNatPortRedirection.getCatalog('201')
    
    
    
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
    
    