'''
Created on Aug 3, 2012

@author: huhe
'''
import simplejson as json
import sys, traceback, time
from pprint import pprint

from lib import Util
from lib import XmlSchemaValidator
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
from test import Test
import ACP

class TestAll(Test):

    __online1,  __online2, __online3, __online4, __online5 = True, True, True, True, True
    #__online1,  __online2, __online3, __online4, __online5 = False, True, True, True, True
    #__online1,  __online2, __online3, __online4, __online5 = False, False, False, False, True
    #__online1,  __online2, __online3, __online4, __online5 = False, False, False, False, False
    
    __descriptionPrefix = 'This is the description of '
        
    def __init__(self):
        self._logger = Util.getLogger(self.__class__.__name__)
        Test.__init__(self)
        
        
    def start(self):
        
        if (TestAll.__online1 and TestAll.__online2 and TestAll.__online3 and TestAll.__online4 and TestAll.__online5): NsmUtil.moveLogResponse()
            
        NsmUtil.mkPresetDir()

        test = Test()
        nsmV1 = self.run(None, 'test-nsm-v1.json', TestAll.__online1)
        nsmV1.getProviderList('301')
        
        catalog = nsmV1.getCatalog()
        top = self.run(catalog, 'test-top.json', TestAll.__online1)
        
        catalog = top.getCatalog()
        provider = self.run(catalog, 'test-provider.json', TestAll.__online1)
                                
        nsmV1.getProviderList('311')
        provider.getPodList('301')
        
        name = 'My Default IP Address Pool of Provider Global'
        ipAddressPoolGlobal         = self.testProviderIpAddressPool(provider, name, 'Global', '101', TestAll.__online1)
        self.testIpReservation('Global', ipAddressPoolGlobal, 'test-ip-reservation-global.json', '111', TestAll.__online1)
        
        catalog = provider.getCatalog()
        pod = self.run(catalog, 'test-pod.json', TestAll.__online1)
        
        provider.getPodList('311')
        
        
        name = 'My Default IP Address Pool of Pod Infrastructure'
        #ipAddressPoolInfrastructure = self.testProviderIpAddressPool(pod, name, 'Infrastructure', '101', TestAll.__online1)
        #self.testIpReservation('Infrastructure', ipAddressPoolInfrastructure, 'test-ip-reservation-infrastructure.json', '111', TestAll.__online1)
        
        
        if TestAll.__online1: 
            NsmUtil.printHeadLine1('test completed up to Pod')
            if Define._DummyAgent:
                acp = ACP()
                acp.start(Define._UrlHostPortEngine, Define._PathScreenShotFile)
                time.sleep(10)
        
        
        catalog = provider.getCatalog()
        tenant = self.run(catalog, 'test-tenant.json', TestAll.__online2)
        
        catalog = tenant.getCatalog()
        tenantNetworkContainer = self.run(catalog, 'test-tenant-network-container.json', TestAll.__online2)
        
        
    
        catalog = tenant.getCatalog()
        internetExtenalNetwork = self.run(catalog, 'test-internet-external-network.json', TestAll.__online3)
        
        catalog = tenantNetworkContainer.getCatalog()
        internetEdgeZone = self.run(catalog, 'test-internet-edge-zone.json', TestAll.__online3, pod)
        
        catalog = internetEdgeZone.getCatalog()
        internetEdgeZoneLayer3Vlan = self.run(catalog, 'test-internet-edge-zone-layer3-vlan.json', TestAll.__online3, pod)
        
        catalog = tenantNetworkContainer.getCatalog()
        externalConnection = self.run(catalog, 'test-internet-external-connection.json', TestAll.__online3, pod)
        
        catalog = tenantNetworkContainer.getCatalog()
        securedInternetEdgeZone = self.run(catalog, 'test-secured-internet-edge-zone.json', TestAll.__online3, pod)
        
        catalog = securedInternetEdgeZone.getCatalog()
        securedInternetEdgeZoneLayer3Vlan = self.run(catalog, 'test-secured-internet-edge-zone-layer3-vlan.json', TestAll.__online3, pod)
        
        
        catalog = tenant.getCatalog()
        internetFirewallService1 = self.run(catalog, 'test-internet-firewall-service-between-secured-and-unsecured-zone.json', TestAll.__online3)
        
        
        catalog = tenant.getCatalog()
        internetFirewallService2 = self.run(catalog, 'test-internet-firewall-service-between-secured-and-external-network.json', TestAll.__online3)
        
        
        catalog = tenant.getCatalog()
        privateExtenalNetwork = self.run(catalog, 'test-private-external-network.json', TestAll.__online4)
        
        catalog = tenantNetworkContainer.getCatalog()
        privateEdgeZone = self.run(catalog, 'test-private-edge-zone.json', TestAll.__online4, pod)
        
        catalog = privateEdgeZone.getCatalog()
        privateEdgeZoneLayer3Vlan = self.run(catalog, 'test-private-edge-zone-layer3-vlan.json', TestAll.__online4, pod)
        
        catalog = tenantNetworkContainer.getCatalog()
        privateMplsConnection = self.run(catalog, 'test-private-mpls-connection.json', TestAll.__online4, pod)
        
        catalog = tenantNetworkContainer.getCatalog()
        securedPrivateEdgeZone = self.run(catalog, 'test-secured-private-edge-zone.json', TestAll.__online4, pod)
        
        catalog = securedPrivateEdgeZone.getCatalog()
        privateEdgeZoneLayer3Vlan = self.run(catalog, 'test-secured-private-edge-zone-layer3-vlan.json', TestAll.__online4, pod)
        
        #sys.exit()
        
        catalog = tenant.getCatalog()
        privateFirewallService1 = self.run(catalog, 'test-private-firewall-service-between-secured-and-unsecured-zone.json', TestAll.__online4)
        
        catalog = tenant.getCatalog()
        privateFirewallService2 = self.run(catalog, 'test-private-firewall-service-between-secured-and-external-network.json', TestAll.__online4)
        


        name = 'My Default IP Address Pool of Internet Edge Zone Layer 3 Vlan'
        myInternetZoneL3VlanSubPoolUid = internetEdgeZoneLayer3Vlan.getSubPoolUid()
        myInternetZoneL3VlanSubPool = IpAddressPool(myInternetZoneL3VlanSubPoolUid, name, 'Layer3ExternalAccessVlan', 'SubPool')
        
        if TestAll.__online5: myInternetZoneL3VlanSubPool.setOnLine()
        elif not TestAll.__online5: myInternetZoneL3VlanSubPool.setOffLine()
        
        myInternetZoneL3VlanSubPoolDetail = myInternetZoneL3VlanSubPool.getDetail('101')
        myInternetZoneL3VlanSubPool.getAllocated('101')
        myInternetZoneL3VlanSubPool.getAvailable('101')
        myInternetZoneL3VlanSubPool.getReservations('101')
        
        name = 'My Default IP Address Reservation of Internet Edge Zone Layer 3 Vlan'
        description = TestAll.__descriptionPrefix + name
        requestParams = {
            'owner': 'My Default Internet Edge Zone Layer 3 Vlan Sub Pool Owner',
            'count': '24',
        }
        myInternetZoneIpReservationCount = IpReservation(myInternetZoneL3VlanSubPoolDetail, name, description, 'default-ip-reservation-count.xml', requestParams)
        
        if TestAll.__online5: myInternetZoneIpReservationCount.setOnLine()
        elif not TestAll.__online5: myInternetZoneIpReservationCount.setOffLine()
        
        myInternetZoneIpReservationCount.create('011')
        myInternetZoneIpReservationCount.getDetail('111')
        myInternetZoneIpReservationCount.getAllocated('111')
        myInternetZoneIpReservationCount.getAvailable('111')
        reservationXml = myInternetZoneIpReservationCount.getReservations('111')
        self._internetEdgeZoneLayer3VlanReservedIpAddressList = NsmUtil.getIpAddressListByReservation(reservationXml, 24)
        
        
        name = 'My Default IP Address Pool of Secured Internet Edge Zone Layer 3 Vlan'
        mySecuredInternetZoneL3VlanSubPoolUid = securedInternetEdgeZoneLayer3Vlan.getSubPoolUid()
        mySecuredInternetZoneL3VlanSubPool = IpAddressPool(mySecuredInternetZoneL3VlanSubPoolUid, name, 'Layer3ExternalAccessVlan', 'SubPool')
        
        if TestAll.__online5: 
            mySecuredInternetZoneL3VlanSubPool.setOnLine()
        elif not TestAll.__online5: 
            mySecuredInternetZoneL3VlanSubPool.setOffLine()
        
        mySecuredInternetZoneL3VlanSubPoolDetail = mySecuredInternetZoneL3VlanSubPool.getDetail('101')
        mySecuredInternetZoneL3VlanSubPool.getAllocated('101')
        mySecuredInternetZoneL3VlanSubPool.getAvailable('101')
        mySecuredInternetZoneL3VlanSubPool.getReservations('101')
        
        
        name = 'My Default IP Address Reservation of Secured Internet Edge Zone Layer 3 Vlan'
        description = TestAll.__descriptionPrefix + name
        requestParams = {
            'owner': 'My Default Secured Internet Edge Zone Layer 3 Vlan Sub Pool Owner',
            'count': '24',
        }
        mySecuredInternetZoneIpReservationCount = IpReservation(mySecuredInternetZoneL3VlanSubPoolDetail, name, description, 'default-ip-reservation-count.xml', requestParams)
        
        if TestAll.__online5: 
            mySecuredInternetZoneIpReservationCount.setOnLine()
        elif not TestAll.__online5: 
            mySecuredInternetZoneIpReservationCount.setOffLine()
        
        mySecuredInternetZoneIpReservationCount.create('011')
        mySecuredInternetZoneIpReservationCount.getDetail('111')
        mySecuredInternetZoneIpReservationCount.getAllocated('111')
        mySecuredInternetZoneIpReservationCount.getAvailable('111')
        reservationXml = mySecuredInternetZoneIpReservationCount.getReservations('111')
        self._securedInternetEdgeZoneLayer3VlanReservedIpAddressList = NsmUtil.getIpAddressListByReservation(reservationXml, 24)
        
                
        catalog = tenant.getCatalog()
        self.run(catalog, 'test-internet-load-balancer.json', TestAll.__online5)
        
        catalog = tenant.getCatalog()
        self.run(catalog, 'test-internet-dynamic-pat.json', TestAll.__online5)
        
        catalog = tenant.getCatalog()
        self.run(catalog, 'test-internet-static-nat.json', TestAll.__online5)
        
        catalog = tenant.getCatalog()
        self.run(catalog, 'test-internet-static-nat-port-redirection.json', TestAll.__online5)

        
            
        

    @staticmethod
    def start1():
        test = TestAll()
        try:
            test.start()
        except:
            test._logger.error('!!!!!!!!!!!!! something is wrong !!!!!!!!!!!!!')
            errorType = sys.exc_info()[0]
            errorValue = sys.exc_info()[1]
            errorTraceBack = traceback.extract_tb(sys.exc_info()[2])
            test._logger.error('Error Type: ' + str(errorType))
            test._logger.error('Error Value: ' + str(errorValue))
            test._logger.error('Traceback: ')
            for oneStack in errorTraceBack:
                test._logger.error(oneStack)
                
        NsmUtil.saveUid(test._uidList)
        NsmUtil.saveResult(test._resultList)
        NsmUtil.printHeadLine2('total test case: ' + str(test._totalTestCase))
        NsmUtil.printHeadLine1('test completed')
          
       
    @staticmethod         
    def start2():
        test = TestAll()
        test.start()
        NsmUtil.saveUid(test._uidList)
        NsmUtil.saveResult(test._resultList)
        NsmUtil.printHeadLine2('total test case: ' + str(test._totalTestCase))
        NsmUtil.printHeadLine1('test completed')

if __name__ == "__main__":
    TestAll.start2()
    
    
    
    
    
    