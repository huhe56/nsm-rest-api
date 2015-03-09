'''
Created on Aug 3, 2012

@author: huhe
'''
import simplejson as json
import sys, traceback
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

class Test(object):

    def __init__(self):
        self._logger = Util.getLogger(self.__class__.__name__)
        self._topName = 'My Default Top'
        self._thisObject = None
        self._dataStore = {}
        self._uidList = []
        self._resultList = []
        self._totalTestCase = 0


    def getUid(self, className, objectName):
        for oneUid in self._uidList:
            if oneUid[1] == className and oneUid[2] == objectName: 
                return oneUid[0]
        return None  
    
        
    def addUid(self, newUid):
        for oneUid in self._uidList:
            if oneUid[1] == newUid[1] and oneUid[2] == newUid[2]: 
                self._uidList.remove(oneUid)
        self._uidList.append(newUid)
            
            
    def testIpAddressPool(self, provider, poolType, online):
        NsmUtil.printHeadLine2('IpAddressPool' + ' [' + poolType + '] - ' + 'detail' + ' - ' + 'positive' + ' - test case ' + str(1))
        self._totalTestCase += 1
        
        ipAddressPoolUid = None
        if poolType == 'Global': ipAddressPoolUid = provider.getGlobalIpAddressPoolUid()
        else: ipAddressPoolUid = provider.getInfrastructureIpAddressPoolUid()
        
        ipAddressPool = IpAddressPool(ipAddressPoolUid, 'Provider', poolType)
        if not online: ipAddressPool.setOffLine()
        ipAddressPoolDetail = ipAddressPool.getDetail()
        assert ipAddressPoolDetail
        result = NsmUtil.printResult(ipAddressPoolDetail, 'positive')
        self._resultList.append(['IpAddressPool', poolType, 'detail', 'positive', str(1), str(result)])
        return ipAddressPool
        
        
    def testIpReservation(self, poolType, ipAddressPool, testCaseFileName, online):
        ipReservation = self.run(ipAddressPool.getDetail(), testCaseFileName, online)
        
        self._totalTestCase += 1
        ipReservation.getAllocated()
        
        self._totalTestCase += 1
        ipReservation.getAvailable()
        
        self._totalTestCase += 1
        ipReservation.getReservations()
        
        
    def run(self, catalog, testCaseFileName, online):
        testCaseFilePath = Define._PathTestCase + '/' + testCaseFileName
        json_data = open(testCaseFilePath)
        self._logger.debug('test case json file path: ' + testCaseFilePath)
        data = json.load(json_data)
        #pprint(data)
        json_data.close()
        
        for className, testSuite in data.items():
            NsmUtil.printHeadLine1(' class: ' + className )
            thisObject = eval(className)(catalog, None, None, None, None)
            
            index = 0;
            name = None
            for testCase in testSuite:
                index += 1
                self._totalTestCase += 1
                skip = None
                action = None
                category = None
                requestBodyFileName = None
                description = None
                
                action = testCase['action']
                category = testCase['category']
                if 'skip' in testCase.keys(): skip = testCase['skip']
                if 'request.body.file' in testCase.keys(): requestBodyFileName = testCase['request.body.file']
                if 'name' in testCase.keys(): name = testCase['name']
                if 'description' in testCase.keys(): description = testCase['description']
                if 'uids' in testCase.keys():
                    for oneUid in testCase['uids']:
                        uidVariable = oneUid['variable']
                        uidClassName = oneUid['class']
                        uidObjectName = oneUid['name'] 
                        testCase[uidVariable] = self.getUid(uidClassName, uidObjectName)
                        if not testCase[uidVariable]:
                            self._logger.error('-------->>>>>> uid for ' + uidClassName + ' [' + uidObjectName + '] can not be None' )
                            continue
                    del testCase['uids']
                
                NsmUtil.printHeadLine2(className + ' [' + name + '] - ' + action + ' - ' + category + ' - test case ' + str(index))
                
                if skip: 
                    self._logger.info('skip this test case')
                    self._resultList.append([className, name, action, category, str(index), 'skipped'])
                    continue
                
                if action == 'create' or action == 'update':
                    if name: thisObject.setCreateName(name)
                    if description: thisObject.setCreateDescription(description)
                    if requestBodyFileName: thisObject.setRequestBodyFile(requestBodyFileName)
                    if testCase: thisObject.setRequestBodyParams(testCase)                    
                
                if action == 'create':
                    if not online: thisObject.setOffLine()
                    result = thisObject.create()
                    name = thisObject.createName
                    result = NsmUtil.printResult(result, category)
                    self._resultList.append([className, name, action, category, str(index), str(result)])
                    self._dataStore[className] = {}
                    self._dataStore[className][name] = {}
                    self._dataStore[className][name]['object'] = thisObject
                    self._thisObject = thisObject
                    
                elif action == 'detail':
                    if not online: thisObject.setOffLine()
                    detail = thisObject.getDetail()
                    name = thisObject.createName
                    result = NsmUtil.printResult(detail, category)
                    self._resultList.append([className, name, action, category, str(index), str(result)])
                    newUid = [thisObject.uid, thisObject.mySubClassName, thisObject.createName]
                    self.addUid(newUid)
                    self._dataStore[className][name]['detail'] = detail
                    
                elif action == 'catalog':
                    if not online: thisObject.setOffLine()
                    catalog = thisObject.getCatalog()
                    name = thisObject.createName
                    result = NsmUtil.printResult(catalog, category)
                    self._resultList.append([className, name, action, category, str(index), str(result)])
                    self._dataStore[className][name]['catalog'] = catalog
                    
                elif action == 'update' and online:
                    result = thisObject.update(className, testCase, category, index)
                    name = thisObject.createName
                    result = NsmUtil.printResult(result, category)
                    self._resultList.append([className, name, action, category, str(index), str(result)])
                    
                elif action == 'delete' and online:
                    result = thisObject.delete()
                    name = thisObject.createName
                    result = NsmUtil.printResult(result, category)
                    self._resultList.append([className, name, action, category, str(index), str(result)])
                    
                elif action == 'list':
                    if not online: thisObject.setOffLine()
                    listUrl = None
                    if className == 'Provider': 
                        listUrl = Define._UrlApiRoot + '/top/provider'
                    elif className == 'Pod':
                        providerName = testCase['provider-name']
                        providerUid = self.getUid('Provider', providerName)
                        listUrl = providerUid + '/pod'
                    fileDashName = thisObject.createName.replace(' ', '-')
                    responseFilePath = Define._PathResponseCreateDefault + '/' + fileDashName + '-list.xml'
                    objectList = thisObject.getList(listUrl, responseFilePath)
                    name = thisObject.createName
                    self._logger.debug('write ' + className + ' [' + name + '] list to file ' + responseFilePath)
                    result = NsmUtil.printResult(objectList, category)
                    self._resultList.append([className, name, action, category, str(index), str(result)])
                        
        return self._thisObject
    
    

if __name__ == "__main__":
    
    NsmUtil.mkPresetDir()
        
    online1 = False
    online2 = True
    online3 = True
    online4 = True
    
    
    try:
    
        test = Test()
        
        nsmV1 = test.run(None, 'test-nsm-v1.json', True)
        
        catalog = nsmV1.getCatalog()
        top = test.run(catalog, 'test-top.json', True)
        
        catalog = top.getCatalog()
        provider = test.run(catalog, 'test-provider.json', online1)
        
        '''
        ipAddressPoolGlobal         = test.testIpAddressPool(provider, 'Global', online1)
        ipAddressPoolInfrastructure = test.testIpAddressPool(provider, 'Infrastructure', online1)
    
        test.testIpReservation('Global', ipAddressPoolGlobal, 'test-ip-reservation-global.json', online1)
        test.testIpReservation('Infrastructure', ipAddressPoolInfrastructure, 'test-ip-reservation-infrastructure.json', online1)
        '''
        
        catalog = provider.getCatalog()
        pod = test.run(catalog, 'test-pod.json', online1)
        
        
        
        if online1: 
            NsmUtil.printHeadLine1('test completed up to Pod')
            sys.exit()
        
        
        
        catalog = provider.getCatalog()
        tenant = test.run(catalog, 'test-tenant.json', online2)
        
        catalog = tenant.getCatalog()
        tenantNetworkContainer = test.run(catalog, 'test-tenant-network-container.json', online2)
        
        
    
        catalog = tenant.getCatalog()
        internetExtenalNetwork = test.run(catalog, 'test-internet-external-network.json', online3)
        
        catalog = tenantNetworkContainer.getCatalog()
        internetEdgeZone = test.run(catalog, 'test-internet-edge-zone.json', online3)
        
        catalog = internetEdgeZone.getCatalog()
        internetEdgeZoneLayer3Vlan = test.run(catalog, 'test-internet-edge-zone-layer3-vlan.json', online3)
        
        catalog = tenantNetworkContainer.getCatalog()
        externalConnection = test.run(catalog, 'test-internet-external-connection.json', online3)
        
        catalog = tenantNetworkContainer.getCatalog()
        securedInternetEdgeZone = test.run(catalog, 'test-secured-internet-edge-zone.json', online3)
        
        catalog = securedInternetEdgeZone.getCatalog()
        internetEdgeZoneLayer3Vlan = test.run(catalog, 'test-secured-internet-edge-zone-layer3-vlan.json', online3)
        
        catalog = tenant.getCatalog()
        internetFirewallService1 = test.run(catalog, 'test-internet-firewall-service-between-secured-and-unsecured-zone.json', online3)
        
        catalog = tenant.getCatalog()
        internetFirewallService2 = test.run(catalog, 'test-internet-firewall-service-between-secured-and-external-network.json', online3)
        
        
        
        catalog = tenant.getCatalog()
        privateExtenalNetwork = test.run(catalog, 'test-private-external-network.json', online4)
        
        catalog = tenantNetworkContainer.getCatalog()
        privateEdgeZone = test.run(catalog, 'test-private-edge-zone.json', online4)
        
        catalog = privateEdgeZone.getCatalog()
        privateEdgeZoneLayer3Vlan = test.run(catalog, 'test-private-edge-zone-layer3-vlan.json', online4)
        
        catalog = tenantNetworkContainer.getCatalog()
        privateMplsConnection = test.run(catalog, 'test-private-mpls-connection.json', online4)
        
        catalog = tenantNetworkContainer.getCatalog()
        securedPrivateEdgeZone = test.run(catalog, 'test-secured-private-edge-zone.json', online4)
        
        catalog = securedPrivateEdgeZone.getCatalog()
        privateEdgeZoneLayer3Vlan = test.run(catalog, 'test-secured-private-edge-zone-layer3-vlan.json', online4)
        
        
        
        catalog = tenant.getCatalog()
        privateFirewallService1 = test.run(catalog, 'test-private-firewall-service-between-secured-and-unsecured-zone.json', True)
        
        catalog = tenant.getCatalog()
        privateFirewallService2 = test.run(catalog, 'test-private-firewall-service-between-secured-and-external-network.json', True)
    
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
    
    