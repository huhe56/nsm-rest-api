'''
Created on Aug 3, 2012

@author: huhe
'''

from isp.nsmUtil import NsmUtil

import subprocess
import simplejson as json
import sys, traceback, time
from pprint import pprint
from datetime import datetime

from lib import Util
from lib import XmlSchemaValidator
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
from isp.loadBalancerService import LoadBalancerService
from isp.dynamicPatService import DynamicPatService
from isp.staticNatService import StaticNatService
from isp.staticNatPortRedirectionService import StaticNatPortRedirectionService
from isp.performance import Performance, PerfTenant
from test import Test
import ACP
from device.main.mainReset import Reset


class TestSimple(Test):

    #__online1,  __online2, __online3, __online4, __online5 = True, True, True, True, True
    #__online1,  __online2, __online3, __online4, __online5 = False, True, True, True, True
    #__online1,  __online2, __online3, __online4, __online5 = False, False, True, True, True
    #__online1,  __online2, __online3, __online4, __online5 = False, False, False, False, True
    __online1,  __online2, __online3, __online4, __online5 = False, False, False, False, False
    
    __descriptionPrefix = 'This is the description of '
        
    def __init__(self):
        self._logger = Util.getLogger(self.__class__.__name__)
        Test.__init__(self)

        
    def start(self):
        
        #if Define._TenantStartIndex != 1:
        #    TestSimple.__online1 = False
            
        Define._PathTestCase = Define._PathTestCase + '-simplified-stress'
        
        if (TestSimple.__online1 and TestSimple.__online2 and TestSimple.__online3 and TestSimple.__online4 and TestSimple.__online5): 
            NsmUtil.moveLogResponse()
            NsmUtil.mkPresetDir()
            
            if Define._ResetNSM: Reset.resetNSM()
            
            if not Define._DummyAgent:
                if Define._ResetDevice: 
                    Reset.resetDevice()
                if Define._CopyCleanRunningConfig:
                    Reset.copyRunningConfigToTFTPServer()
                    Reset.copyRunningConfigToTemp('copy-to-tmp-clean')
                if Define._DiffClean:
                    Reset.diffCleanClean()
        

        test = Test()
        nsmV1 = self.run(None, 'test-nsm-v1.json', TestSimple.__online1)
        nsmV1.getProviderList('301')
        
        catalog = nsmV1.getCatalog()
        top = self.run(catalog, 'test-top.json', TestSimple.__online1)
        
        catalog = top.getCatalog()
        provider = self.run(catalog, 'test-provider.json', TestSimple.__online1)
        
        catalog = provider.getCatalog()
        pod = self.run(catalog, 'test-pod-full.json', TestSimple.__online1)       
                                                    
                                                    
                                                               
        if TestSimple.__online1: 
            NsmUtil.printHeadLine1('test completed up to Pod')
            if Define._DummyAgent:
                ''' acp not working any more because of new firefox upgrade, need to work on it later '''
                sys.exit()
                acp = ACP()
                acp.start(Define._UrlHostPortEngine, Define._PathScreenShotFile)
                time.sleep(10)
            else:
                #sys.exit()
                Reset.startController()
                time.sleep(300)
                if Define._SetDSCLoggingDebug:
                    Reset.setDSCLogDebug()
                
                
        for tenantIndex in range(Define._TenantStartIndex, Define._TenantStartIndex + Define._TenantCount):         
            
            #if tenantIndex != 1: time.sleep(15*60)
            
            if Define._Performance:
                currentPerfTenant = PerfTenant()
                Define._PerformanceData.addCurrentTenant(currentPerfTenant)
                Define._PerformanceData.setCurrentTenantStartTime(datetime.now())
                
            
            Define._TenantIndex = tenantIndex
        
            catalog = provider.getCatalog()
            tenant = self.run(catalog, 'test-tenant.json', TestSimple.__online2)
            
            catalogTenant = tenant.getCatalog()
            tenantNetworkContainer = self.run(catalogTenant, 'test-tenant-network-container.json', TestSimple.__online2)
            
                
            ''' internet zone '''
            #catalog = tenant.getCatalog()
            internetExtenalNetwork = self.run(catalogTenant, 'test-internet-external-network.json', TestSimple.__online3)
            
            catalog = tenantNetworkContainer.getCatalog()
            internetEdgeZone = self.run(catalog, 'test-internet-edge-zone.json', TestSimple.__online3, pod)        
            
            catalog = internetEdgeZone.getCatalog()
            internetEdgeZoneLayer3Vlan = self.run(catalog, 'test-internet-edge-zone-layer3-vlan.json', TestSimple.__online3, pod)
            
            
            
            catalog = tenantNetworkContainer.getCatalog()
            externalConnection = self.run(catalog, 'test-internet-external-connection.json', TestSimple.__online3, pod)
                    
                    
            ''' secured internet zone '''
            catalog = tenantNetworkContainer.getCatalog()
            securedInternetEdgeZone = self.run(catalog, 'test-secured-internet-edge-zone.json', TestSimple.__online3, pod)
            
            catalog = securedInternetEdgeZone.getCatalog()
            securedInternetEdgeZoneLayer3Vlan = self.run(catalog, 'test-secured-internet-edge-zone-layer3-vlan.json', TestSimple.__online3, pod)
        
            
            ''' internet zone firewall '''
            #catalog = tenant.getCatalog()
            internetFirewallService1 = self.run(catalogTenant, 'test-internet-firewall-service-between-secured-and-unsecured-zone.json', TestSimple.__online3)
            
            #catalog = tenant.getCatalog()
            internetFirewallService2 = self.run(catalogTenant, 'test-internet-firewall-service-between-secured-and-external-network.json', TestSimple.__online3)
            
            
            
            ''' private zone '''
            #catalog = tenant.getCatalog()
            privateExtenalNetwork = self.run(catalogTenant, 'test-private-external-network.json', TestSimple.__online4)
            
            catalog = tenantNetworkContainer.getCatalog()
            privateEdgeZone = self.run(catalog, 'test-private-edge-zone.json', TestSimple.__online4, pod)
            
            catalog = privateEdgeZone.getCatalog()
            privateEdgeZoneLayer3Vlan = self.run(catalog, 'test-private-edge-zone-layer3-vlan.json', TestSimple.__online4, pod)
            
            catalog = tenantNetworkContainer.getCatalog()
            privateMplsConnection = self.run(catalog, 'test-private-mpls-connection.json', TestSimple.__online4, pod)
            
            catalog = tenantNetworkContainer.getCatalog()
            securedPrivateEdgeZone = self.run(catalog, 'test-secured-private-edge-zone.json', TestSimple.__online4, pod)
            
            catalog = securedPrivateEdgeZone.getCatalog()
            privateEdgeZoneLayer3Vlan = self.run(catalog, 'test-secured-private-edge-zone-layer3-vlan.json', TestSimple.__online4, pod)
            
            
            ''' private zone firewall '''
            #catalog = tenant.getCatalog()
            privateFirewallService1 = self.run(catalogTenant, 'test-private-firewall-service-between-secured-and-unsecured-zone.json', TestSimple.__online4)
            
            #catalog = tenant.getCatalog()
            privateFirewallService2 = self.run(catalogTenant, 'test-private-firewall-service-between-secured-and-external-network.json', TestSimple.__online4)
            
            
            
            
            ''' internet zone ip reservation '''
            
            name = 'My Default IP Address Pool of Internet Edge Zone Layer 3 Vlan'
            myInternetZoneL3VlanSubPoolUid = internetEdgeZoneLayer3Vlan.getSubPoolUid()
            myInternetZoneL3VlanSubPool = IpAddressPool(myInternetZoneL3VlanSubPoolUid, name, 'Layer3ExternalAccessVlan', 'SubPool')
            
            if TestSimple.__online4: myInternetZoneL3VlanSubPool.setOnLine()
            elif not TestSimple.__online4: myInternetZoneL3VlanSubPool.setOffLine()
            
            myInternetZoneL3VlanSubPoolDetail = myInternetZoneL3VlanSubPool.getDetail('101')
            
            name = 'My Default IP Address Reservation of Internet Edge Zone Layer 3 Vlan'
            description = TestSimple.__descriptionPrefix + name
            requestParams = {
                'owner': 'My Default Internet Edge Zone Layer 3 Vlan Sub Pool Owner',
                'count': '16',
            }
            myInternetZoneIpReservationCount = IpReservation(myInternetZoneL3VlanSubPoolDetail, name, description, 'default-ip-reservation-count.xml', requestParams)
            
            if TestSimple.__online4: myInternetZoneIpReservationCount.setOnLine()
            elif not TestSimple.__online4: myInternetZoneIpReservationCount.setOffLine()
            
            myInternetZoneIpReservationCount.create('011')
            myInternetZoneIpReservationCount.getDetail('111')
            
            reservationXml = myInternetZoneIpReservationCount.getReservations('111')
            self._internetEdgeZoneLayer3VlanReservedIpAddressList = NsmUtil.getIpAddressListByReservation(reservationXml, 16)
            
                
            
            ''' secured internet zone ip reservation '''
            
            name = 'My Default IP Address Pool of Secured Internet Edge Zone Layer 3 Vlan'
            mySecuredInternetZoneL3VlanSubPoolUid = securedInternetEdgeZoneLayer3Vlan.getSubPoolUid()
            mySecuredInternetZoneL3VlanSubPool = IpAddressPool(mySecuredInternetZoneL3VlanSubPoolUid, name, 'Layer3ExternalAccessVlan', 'SubPool')
            
            if TestSimple.__online4: 
                mySecuredInternetZoneL3VlanSubPool.setOnLine()
            elif not TestSimple.__online4: 
                mySecuredInternetZoneL3VlanSubPool.setOffLine()
            
            mySecuredInternetZoneL3VlanSubPoolDetail = mySecuredInternetZoneL3VlanSubPool.getDetail('101')
            
            
            name = 'My Default IP Address Reservation of Secured Internet Edge Zone Layer 3 Vlan'
            description = TestSimple.__descriptionPrefix + name
            requestParams = {
                'owner': 'My Default Secured Internet Edge Zone Layer 3 Vlan Sub Pool Owner',
                'count': '16',
            }
            mySecuredInternetZoneIpReservationCount = IpReservation(mySecuredInternetZoneL3VlanSubPoolDetail, name, description, 'default-ip-reservation-count.xml', requestParams)
            
            if TestSimple.__online4: 
                mySecuredInternetZoneIpReservationCount.setOnLine()
            elif not TestSimple.__online4: 
                mySecuredInternetZoneIpReservationCount.setOffLine()
            
            mySecuredInternetZoneIpReservationCount.create('011')
            mySecuredInternetZoneIpReservationCount.getDetail('111')
            
            reservationXml = mySecuredInternetZoneIpReservationCount.getReservations('111')
            self._securedInternetEdgeZoneLayer3VlanReservedIpAddressList = NsmUtil.getIpAddressListByReservation(reservationXml, 16)
            
            
            ''' internet zone lb service '''
            #catalog = tenant.getCatalog()
            self.run(catalogTenant, 'test-internet-load-balancer.json', TestSimple.__online5)
            
            
            ''' internet zone NAT service '''
            #catalog = tenant.getCatalog()
            self.run(catalogTenant, 'test-internet-dynamic-pat.json', TestSimple.__online5)
                     
            #catalog = tenant.getCatalog()
            self.run(catalogTenant, 'test-internet-static-nat.json', TestSimple.__online5)
            
            #catalog = tenant.getCatalog()
            self.run(catalogTenant, 'test-internet-static-nat-port-redirection.json', TestSimple.__online5)
            
            
            ''' secured internet zone lb service '''
            #catalog = tenant.getCatalog()
            securedInternetLoadBalancer = self.run(catalogTenant, 'test-secured-internet-load-balancer.json', TestSimple.__online5)
            
            if Define._Performance:
                Define._PerformanceData.setCurrentTenantEndTime(datetime.now(), Define._TenantIndex)
                #Define._PerformanceData.debug()
        
        
    @staticmethod
    def start1():
        test = TestSimple()
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
        
        if (not Define._DummyAgent and TestSimple.__online1 and TestSimple.__online2 and TestSimple.__online3 and TestSimple.__online4 and TestSimple.__online5):
            time.sleep(300)
            
        if Define._SaveNSMLog:
            Reset.saveNSMLog()
        if Define._CopyCreateRunningConfig:
            Reset.copyCreateRunningConfig()
                
        if Define._DeviceVerification:
            perl = '/usr/local/ActivePerl-5.16/bin/perl'
            dirNSMPerl = '/Users/huhe/Install/workspace/NSM-NBAPI-Perl'
            dirDeviceVerification = dirNSMPerl + '/device-verification'
            cmdPerlNSM = dirDeviceVerification + '/NSM.pl'
            cmdPerlParse = dirDeviceVerification + '/Parse.pl'
            cmdPerlProcess = dirDeviceVerification + '/Process.pl'
            
            p = subprocess.Popen(perl + ' ' + cmdPerlNSM, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            for line in p.stdout.readlines(): print line
            retval = p.wait()
            
            p = subprocess.Popen(perl + ' ' + cmdPerlParse, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            for line in p.stdout.readlines(): print line
            retval = p.wait()

            p = subprocess.Popen(perl + ' ' + cmdPerlProcess, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            for line in p.stdout.readlines(): print line
            retval = p.wait()

       
    @staticmethod         
    def start2():
        test = TestSimple()
        test.start()
        NsmUtil.saveUid(test._uidList)
        NsmUtil.saveResult(test._resultList)
        NsmUtil.printHeadLine2('total test case: ' + str(test._totalTestCase))
        NsmUtil.printHeadLine1('test completed')


if __name__ == "__main__":
    TestSimple.start2()
    
    
    
    
    
    