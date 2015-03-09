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

    __online1,  __online2, __online3, __online4, __online5 = True, True, True, True, True
    #__online1,  __online2, __online3, __online4, __online5 = False, True, True, True, True
    #__online1,  __online2, __online3, __online4, __online5 = False, False, True, True, True
    #__online1,  __online2, __online3, __online4, __online5 = False, False, False, True, True
    #__online1,  __online2, __online3, __online4, __online5 = False, False, False, False, True
    #__online1,  __online2, __online3, __online4, __online5 = False, False, False, False, False
    
    __descriptionPrefix = 'This is the description of '
        
    def __init__(self):
        self._logger = Util.getLogger(self.__class__.__name__)
        Test.__init__(self)

        
    def start(self):
        
        #if Define._TenantStartIndex != 1:
        #    TestSimple.__online1 = False
            
        Define._PathTestCase = Define._PathTestCase + '-simplified-fury'
        
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
        pod = self.run(catalog, 'test-pod-full-fury.json', TestSimple.__online1)                                    
                                   
                                                               
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
        
            
            providerNetworkContainer = self.run(catalog, 'test-provider-network-container.json', TestSimple.__online2)
            catalogPNC = providerNetworkContainer.getCatalog()
            
            internetExtenalNetwork = self.run(catalogPNC, 'test-internet-external-network.json', TestSimple.__online2)
            catalog = internetExtenalNetwork.getCatalog()
            
            northZone = self.run(catalogPNC, 'test-north-zone.json', TestSimple.__online2)
            catalog = northZone.getCatalog() 
            
            externalConnection = self.run(catalogPNC, 'test-internet-external-connection-fury.json', TestSimple.__online2, pod)
            catalog = externalConnection.getCatalog()
            
            southZone = self.run(catalogPNC, 'test-south-zone.json', TestSimple.__online2)
            catalog = southZone.getCatalog() 
            
            layer3ExplicitSubnet = self.run(catalog, 'test-south-zone-layer3-explicit-subnet.json', TestSimple.__online2)
            catalog = layer3ExplicitSubnet.getCatalog() 
                                                  
            self._internetEdgeZoneLayer3VlanReservedIpAddressList = self.reserveIpAddress(layer3ExplicitSubnet, 'Layer3ExplicitSubnet', 16, 1, TestSimple.__online4)
            
            #internetFirewallService0 = self.run(catalogPNC, 'test-internet-firewall-service-between-south-zone-and-external-network.json', TestSimple.__online5)
            internetFirewallService1 = self.run(catalogPNC, 'test-internet-firewall-service-between-south-zone-and-external-network-any-1.json', TestSimple.__online5)
            internetFirewallService2 = self.run(catalogPNC, 'test-internet-firewall-service-between-south-zone-and-external-network-any-2.json', TestSimple.__online5)

            if Define._Performance:
                Define._PerformanceData.setCurrentTenantEndTime(datetime.now(), Define._TenantIndex)
                #Define._PerformanceData.debug()
        
        
    ''' internet zone ip reservation '''
    def reserveIpAddress(self, internetEdgeZoneLayer3Vlan, parentName, count, reservationIndex, online):
        
        name = 'My Default IP Address Pool of ' + parentName + ' ' + str(reservationIndex)
        
        myInternetZoneL3VlanSubPoolUid = internetEdgeZoneLayer3Vlan.getSubPoolUid()
        myInternetZoneL3VlanSubPool = IpAddressPool(myInternetZoneL3VlanSubPoolUid, name, parentName, 'SubPool')
        
        if online: myInternetZoneL3VlanSubPool.setOnLine()
        elif not online: myInternetZoneL3VlanSubPool.setOffLine()
        
        myInternetZoneL3VlanSubPoolDetail = myInternetZoneL3VlanSubPool.getDetail('101')
        
        name = 'My Default IP Address Reservation of ' + parentName + ' ' + str(reservationIndex)
        owner = name + ' owner'
        
        description = TestSimple.__descriptionPrefix + name
        requestParams = {
            'owner': owner,
            'count': str(count),
        }
        myInternetZoneIpReservationCount = IpReservation(myInternetZoneL3VlanSubPoolDetail, name, description, 'default-ip-reservation-count.xml', requestParams)
        
        if online: myInternetZoneIpReservationCount.setOnLine()
        elif not online: myInternetZoneIpReservationCount.setOffLine()
        
        myInternetZoneIpReservationCount.create('011')
        myInternetZoneIpReservationCount.getDetail('111')
        
        reservationXml = myInternetZoneIpReservationCount.getReservations('111')
        return NsmUtil.getIpAddressListByReservation(reservationXml, count)
            
        
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
    TestSimple.start1()
    
    
    
    
    
    