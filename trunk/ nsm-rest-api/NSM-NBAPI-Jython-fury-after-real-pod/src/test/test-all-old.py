'''
Created on Aug 3, 2012

@author: huhe
'''
import simplejson as json
import sys, traceback
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


class Test(object):

    __online1,  __online2, __online3, __online4, __online5 = True, True, True, True, True
    #__online1,  __online2, __online3, __online4, __online5 = False, True, True, True, True
    #__online1,  __online2, __online3, __online4, __online5 = False, False, False, False, True
    #__online1,  __online2, __online3, __online4, __online5 = False, False, False, False, False
    
    __descriptionPrefix = 'This is the description of '
        
    def __init__(self):
        self._logger = Util.getLogger(self.__class__.__name__)
        self._topName = 'My Default Top'
        self._thisObject = None
        self._dataStore = {}
        self._uidList = []
        self._resultList = []
        self._totalTestCase = 0
        self._metaPropertyTestCases = {}

        self._internetEdgeZoneLayer3VlanReservedIpAddressList = None
        self._securedInternetEdgeZoneLayer3VlanReservedIpAddressList = None
        
        
        
    def start(self):
        
        if (Test.__online1 and Test.__online2 and Test.__online3 and Test.__online4 and Test.__online5):
            NsmUtil.deleteLogResponse()
            
        NsmUtil.mkPresetDir()

        test = Test()
        nsmV1 = self.run(None, 'test-nsm-v1.json', Test.__online1)
        nsmV1.getProviderList('301')
        
        catalog = nsmV1.getCatalog()
        top = self.run(catalog, 'test-top.json', Test.__online1)
        
        catalog = top.getCatalog()
        provider = self.run(catalog, 'test-provider.json', Test.__online1)
                
        
        nsmV1.getProviderList('311')
        provider.getPodList('301')
        
        name = 'My Default IP Address Pool of Provider Global'
        ipAddressPoolGlobal         = self.testProviderIpAddressPool(provider, name, 'Global', '101', Test.__online1)
        name = 'My Default IP Address Pool of Provider Infrastructure'
        ipAddressPoolInfrastructure = self.testProviderIpAddressPool(provider, name, 'Infrastructure', '101', Test.__online1)
        
        self.testIpReservation('Global', ipAddressPoolGlobal, 'test-ip-reservation-global.json', '111', Test.__online1)
        self.testIpReservation('Infrastructure', ipAddressPoolInfrastructure, 'test-ip-reservation-infrastructure.json', '111', Test.__online1)
        
        
        catalog = provider.getCatalog()
        pod = self.run(catalog, 'test-pod.json', Test.__online1)
        
        provider.getPodList('311')
        
        
        if Test.__online1: 
            NsmUtil.printHeadLine1('test completed up to Pod')
            #sys.exit()
        
        
        catalog = provider.getCatalog()
        tenant = self.run(catalog, 'test-tenant.json', Test.__online2)
        
        catalog = tenant.getCatalog()
        tenantNetworkContainer = self.run(catalog, 'test-tenant-network-container.json', Test.__online2)
        
        
    
        catalog = tenant.getCatalog()
        internetExtenalNetwork = self.run(catalog, 'test-internet-external-network.json', Test.__online3)
        
        catalog = tenantNetworkContainer.getCatalog()
        internetEdgeZone = self.run(catalog, 'test-internet-edge-zone.json', Test.__online3)
        
        catalog = internetEdgeZone.getCatalog()
        internetEdgeZoneLayer3Vlan = self.run(catalog, 'test-internet-edge-zone-layer3-vlan.json', Test.__online3)
        
        catalog = tenantNetworkContainer.getCatalog()
        externalConnection = self.run(catalog, 'test-internet-external-connection.json', Test.__online3)
        
        catalog = tenantNetworkContainer.getCatalog()
        securedInternetEdgeZone = test.run(catalog, 'test-secured-internet-edge-zone.json', Test.__online3)
        
        catalog = securedInternetEdgeZone.getCatalog()
        securedInternetEdgeZoneLayer3Vlan = self.run(catalog, 'test-secured-internet-edge-zone-layer3-vlan.json', Test.__online3)
        
        
        catalog = tenant.getCatalog()
        internetFirewallService1 = self.run(catalog, 'test-internet-firewall-service-between-secured-and-unsecured-zone.json', Test.__online3)
        
        
        catalog = tenant.getCatalog()
        internetFirewallService2 = self.run(catalog, 'test-internet-firewall-service-between-secured-and-external-network.json', Test.__online3)
        
        
        catalog = tenant.getCatalog()
        privateExtenalNetwork = self.run(catalog, 'test-private-external-network.json', Test.__online4)
        
        catalog = tenantNetworkContainer.getCatalog()
        privateEdgeZone = self.run(catalog, 'test-private-edge-zone.json', Test.__online4)
        
        catalog = privateEdgeZone.getCatalog()
        privateEdgeZoneLayer3Vlan = self.run(catalog, 'test-private-edge-zone-layer3-vlan.json', Test.__online4)
        
        catalog = tenantNetworkContainer.getCatalog()
        privateMplsConnection = self.run(catalog, 'test-private-mpls-connection.json', Test.__online4)
        
        catalog = tenantNetworkContainer.getCatalog()
        securedPrivateEdgeZone = self.run(catalog, 'test-secured-private-edge-zone.json', Test.__online4)
        
        catalog = securedPrivateEdgeZone.getCatalog()
        privateEdgeZoneLayer3Vlan = self.run(catalog, 'test-secured-private-edge-zone-layer3-vlan.json', Test.__online4)
        
        #sys.exit()
        
        catalog = tenant.getCatalog()
        privateFirewallService1 = self.run(catalog, 'test-private-firewall-service-between-secured-and-unsecured-zone.json', Test.__online4)
        
        catalog = tenant.getCatalog()
        privateFirewallService2 = self.run(catalog, 'test-private-firewall-service-between-secured-and-external-network.json', Test.__online4)
        

        name = 'My Default IP Address Pool of Internet Edge Zone Layer 3 Vlan'
        myInternetZoneL3VlanSubPoolUid = internetEdgeZoneLayer3Vlan.getSubPoolUid()
        myInternetZoneL3VlanSubPool = IpAddressPool(myInternetZoneL3VlanSubPoolUid, name, 'Layer3ExternalAccessVlan', 'SubPool')
        
        if Test.__online5: myInternetZoneL3VlanSubPool.setOnLine()
        elif not Test.__online5: myInternetZoneL3VlanSubPool.setOffLine()
        
        myInternetZoneL3VlanSubPoolDetail = myInternetZoneL3VlanSubPool.getDetail('101')
        myInternetZoneL3VlanSubPool.getAllocated('101')
        myInternetZoneL3VlanSubPool.getAvailable('101')
        myInternetZoneL3VlanSubPool.getReservations('101')
        
        name = 'My Default IP Address Reservation of Internet Edge Zone Layer 3 Vlan'
        description = Test.__descriptionPrefix + name
        requestParams = {
            'owner': 'My Default Internet Edge Zone Layer 3 Vlan Sub Pool Owner',
            'count': '16',
        }
        myInternetZoneIpReservationCount = IpReservation(myInternetZoneL3VlanSubPoolDetail, name, description, 'default-ip-reservation-count.xml', requestParams)
        
        if Test.__online5: myInternetZoneIpReservationCount.setOnLine()
        elif not Test.__online5: myInternetZoneIpReservationCount.setOffLine()
        
        myInternetZoneIpReservationCount.create('011')
        myInternetZoneIpReservationCount.getDetail('111')
        myInternetZoneIpReservationCount.getAllocated('111')
        myInternetZoneIpReservationCount.getAvailable('111')
        reservationXml = myInternetZoneIpReservationCount.getReservations('111')
        self._internetEdgeZoneLayer3VlanReservedIpAddressList = NsmUtil.getIpAddressListByReservation(reservationXml, 16)
        
        
        name = 'My Default IP Address Pool of Secured Internet Edge Zone Layer 3 Vlan'
        mySecuredInternetZoneL3VlanSubPoolUid = securedInternetEdgeZoneLayer3Vlan.getSubPoolUid()
        mySecuredInternetZoneL3VlanSubPool = IpAddressPool(mySecuredInternetZoneL3VlanSubPoolUid, name, 'Layer3ExternalAccessVlan', 'SubPool')
        
        if Test.__online5: 
            mySecuredInternetZoneL3VlanSubPool.setOnLine()
        elif not Test.__online5: 
            mySecuredInternetZoneL3VlanSubPool.setOffLine()
        
        mySecuredInternetZoneL3VlanSubPoolDetail = mySecuredInternetZoneL3VlanSubPool.getDetail('101')
        mySecuredInternetZoneL3VlanSubPool.getAllocated('101')
        mySecuredInternetZoneL3VlanSubPool.getAvailable('101')
        mySecuredInternetZoneL3VlanSubPool.getReservations('101')
        
        
        name = 'My Default IP Address Reservation of Secured Internet Edge Zone Layer 3 Vlan'
        description = Test.__descriptionPrefix + name
        requestParams = {
            'owner': 'My Default Secured Internet Edge Zone Layer 3 Vlan Sub Pool Owner',
            'count': '16',
        }
        mySecuredInternetZoneIpReservationCount = IpReservation(mySecuredInternetZoneL3VlanSubPoolDetail, name, description, 'default-ip-reservation-count.xml', requestParams)
        
        if Test.__online5: 
            mySecuredInternetZoneIpReservationCount.setOnLine()
        elif not Test.__online5: 
            mySecuredInternetZoneIpReservationCount.setOffLine()
        
        mySecuredInternetZoneIpReservationCount.create('011')
        mySecuredInternetZoneIpReservationCount.getDetail('111')
        mySecuredInternetZoneIpReservationCount.getAllocated('111')
        mySecuredInternetZoneIpReservationCount.getAvailable('111')
        reservationXml = mySecuredInternetZoneIpReservationCount.getReservations('111')
        self._securedInternetEdgeZoneLayer3VlanReservedIpAddressList = NsmUtil.getIpAddressListByReservation(reservationXml, 16)
        
        
        Test.__online5 = True
        
        catalog = tenant.getCatalog()
        self.run(catalog, 'test-internet-load-balancer.json', Test.__online5)
        
        catalog = tenant.getCatalog()
        self.run(catalog, 'test-internet-dynamic-pat.json', Test.__online5)
        
        catalog = tenant.getCatalog()
        self.run(catalog, 'test-internet-static-nat.json', Test.__online5)
        
        catalog = tenant.getCatalog()
        self.run(catalog, 'test-internet-static-nat-port-redirection.json', Test.__online5)

        

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
            
            
    def testProviderIpAddressPool(self, provider, name, poolType, testCaseId, online):
        NsmUtil.printHeadLine2('Provider IpAddressPool' + ' [' + poolType + '] - ' + 'detail' + ' - ' + 'positive' + ' - test case ' + str(testCaseId))
        self._totalTestCase += 1
        
        ipAddressPoolUid = None
        if poolType == 'Global': ipAddressPoolUid = provider.getGlobalIpAddressPoolUid()
        else: ipAddressPoolUid = provider.getInfrastructureIpAddressPoolUid()
        
        ipAddressPool = IpAddressPool(ipAddressPoolUid, name, 'Provider', poolType)
        
        if online: ipAddressPool.setOnLine()
        elif not online: ipAddressPool.setOffLine()
        
        ipAddressPoolDetail = ipAddressPool.getDetail(testCaseId)
        assert ipAddressPoolDetail
        
        result = NsmUtil.printResult(ipAddressPoolDetail, 'positive')
        self._resultList.append(['IpAddressPool', poolType, 'detail', 'positive', str(testCaseId), str(result)])
        return ipAddressPool
        
        
    def testIpReservation(self, poolType, ipAddressPool, testCaseFileName, testCaseId, online):
        ipReservation = self.run(ipAddressPool.getDetail(testCaseId), testCaseFileName, online)
        
        self._totalTestCase += 1
        ipReservation.getAllocated(testCaseId)
        
        self._totalTestCase += 1
        ipReservation.getAvailable(testCaseId)
        
        self._totalTestCase += 1
        ipReservation.getReservations(testCaseId)
        
    
    def testUpdate(self, className, requestBody, category, testCaseId):
        if Define._SchemaValidateRequestBody:
            XmlSchemaValidator.validate(self._thisObject._xsd, requestBody)
        result = self._thisObject.update(className, requestBody, category, testCaseId)
        return result
        
        
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
            
            name = None
            for testCase in testSuite:
                
                self._totalTestCase += 1
                
                testCaseId = None
                action = None
                category = None
                requestBodyFileName = None
                description = None
                
                testCaseId = testCase['id']
                action = testCase['action']
                category = testCase['category']
                
                
                if 'skip' in testCase.keys() and testCase['skip'] == 'true': 
                    self._logger.info('skip this test case')
                    self._resultList.append([className, name, action, category, str(testCaseId), 'skipped'])
                    continue
                
                if 'online' in testCase.keys() and testCase['online'] == 'true': online = True
                if 'request.body.file' in testCase.keys(): requestBodyFileName = testCase['request.body.file']
                if 'name' in testCase.keys(): name = testCase['name']
                if 'description' in testCase.keys(): description = testCase['description']
                
                for ipv4StartKey, ipv4StartValue in testCase.items():
                    if ipv4StartKey.endswith('ipv4.start'):
                        if ipv4StartValue == 'InternetEdgeZoneLayer3VlanReservedIpAddress':
                            oneIpAddress = self._internetEdgeZoneLayer3VlanReservedIpAddressList.pop()
                            testCase[ipv4StartKey] = oneIpAddress
                            ipv4EndKey = ipv4StartKey.replace('.ipv4.start', '.ipv4.end')
                            testCase[ipv4EndKey] = oneIpAddress
                        elif ipv4StartValue == 'SecuredInternetEdgeZoneLayer3VlanReservedIpAddress':
                            oneIpAddress = self._securedInternetEdgeZoneLayer3VlanReservedIpAddressList.pop()
                            testCase[ipv4StartKey] = oneIpAddress
                            ipv4EndKey = ipv4StartKey.replace('.ipv4.start', '.ipv4.end')
                            testCase[ipv4EndKey] = oneIpAddress   
                
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
                
                if action != 'update':
                    NsmUtil.printHeadLine2(className + ' [' + name + '] - ' + action + ' - ' + category + ' - test case ' + str(testCaseId))
                
            
                try:
                
                    if action == 'create':
                        if online: thisObject.setOnLine()
                        elif not online: thisObject.setOffLine()
                        
                        if name: thisObject.setCreateName(name)
                        if description: thisObject.setCreateDescription(description)
                        if requestBodyFileName: thisObject.setRequestBodyFile(requestBodyFileName)
                        if testCase: thisObject.setRequestBodyParams(testCase)                    
                    
                        result = thisObject.create(testCaseId)
                        name = thisObject.createName
                        result = NsmUtil.printResult(result, category)
                        self._resultList.append([className, name, action, category, str(testCaseId), str(result)])
                        
                        if not className in self._dataStore.keys(): self._dataStore[className] = {}
                        if not name in self._dataStore[className].keys(): self._dataStore[className][name] = {}
                        self._dataStore[className][name]['object'] = thisObject
                        self._thisObject = thisObject
                        
                    elif action == 'detail':
                        if online: thisObject.setOnLine()
                        elif not online: thisObject.setOffLine()
                        
                        detail = thisObject.getDetail(testCaseId)
                        name = thisObject.createName
                        result = NsmUtil.printResult(detail, category)
                        self._resultList.append([className, name, action, category, str(testCaseId), str(result)])
                        
                        self.addUid([thisObject.uid, thisObject.mySubClassName, thisObject.createName])
                        self._dataStore[className][name]['detail'] = detail
                        
                        if className == 'IpReservation' or className == 'IpAddressPool':
                            thisObject.getAllocated(testCaseId)
                            thisObject.getAvailable(testCaseId)
                            thisObject.getReservations(testCaseId)
                        
                    elif action == 'catalog':
                        if online: thisObject.setOnLine()
                        elif not online: thisObject.setOffLine()
                        
                        catalog = thisObject.getCatalog(testCaseId)
                        name = thisObject.createName
                        result = NsmUtil.printResult(catalog, category)
                        self._resultList.append([className, name, action, category, str(testCaseId), str(result)])
                        self._dataStore[className][name]['catalog'] = catalog
                        
                    elif action == 'update' and online and Define._Update:
                        if 'test.case.file' in testCase.keys():
                            metaPropertyTestCaseFileName = testCase['test.case.file']
                            if not metaPropertyTestCaseFileName in self._metaPropertyTestCases.keys():
                                testCaseFilePath = Define._PathTestCase + '/' + testCase['test.case.file']
                                metaProperties = NsmUtil.getMetaProperties(testCaseFilePath)
                                self._metaPropertyTestCases[metaPropertyTestCaseFileName] = metaProperties
                            self._logger.debug('className: ' + className + '; name: ' + name)
                            metaPropertiesLines = self._metaPropertyTestCases[metaPropertyTestCaseFileName][className][name]
                            
                            requestBody = None
                            if testCase['test.case.file'] == 'update-all-meta-properties.csv':
                                self._totalTestCase += 1
                                NsmUtil.printHeadLine2(className + ' [' + name + '] - ' + action + ' description - ' + category + ' - test case ' + str(testCaseId) + '-' + str(self._totalTestCase))
                                updateDescription = 'This is the default update description of my ' + className
                                requestBody = NsmUtil.createRequestBodyProperty(className, thisObject.createName, updateDescription)
                                result = self.testUpdate(className, requestBody, category, testCaseId)
                                result = NsmUtil.printResult(result, category)
                                self._resultList.append([className, name, action, category, str(testCaseId)+'-'+str(self._totalTestCase), str(result)])
                                
                                ### can't udpate pod name at this moment
                                if className != 'Pod':
                                    self._totalTestCase += 1
                                    NsmUtil.printHeadLine2(className + ' [' + name + '] - ' + action + ' name - ' + category + ' - test case ' + str(testCaseId) + '-' + str(self._totalTestCase))
                                    updateName = 'My Default Update ' + className
                                    requestBody = NsmUtil.createRequestBodyProperty(className, updateName)
                                    result = self.testUpdate(className, requestBody, category, testCaseId)
                                    result = NsmUtil.printResult(result, category)
                                    self._resultList.append([className, name, action, category, str(testCaseId)+'-'+str(self._totalTestCase), str(result)])
                                
                            for oneMetaProperties in metaPropertiesLines:
                                self._totalTestCase += 1
                                NsmUtil.printHeadLine2(className + ' [' + name + '] - ' + action + ' - ' + category + ' - test case ' + str(testCaseId) + '-' + str(self._totalTestCase))
                                
                                storage = {}
                                storage['_uidList'] = self._uidList
                                storage['_internetEdgeZoneLayer3VlanReservedIpAddressList'] = self._internetEdgeZoneLayer3VlanReservedIpAddressList
                                storage['_securedInternetEdgeZoneLayer3VlanReservedIpAddressList'] = self._securedInternetEdgeZoneLayer3VlanReservedIpAddressList
                                
                                metaPropertiesWrapperList = []
                                metaPropertiesWrapperList.append(oneMetaProperties)
                                requestBody = NsmUtil.createRequestBodyProperty(className, thisObject.createName, None, metaPropertiesWrapperList, storage)
                                result = self.testUpdate(className, requestBody, category, testCaseId)
                                result = NsmUtil.printResult(result, category)
                                self._resultList.append([className, name, action, category, str(testCaseId)+'-'+str(self._totalTestCase), str(result)])
                            
                            # all meta properties
                            if Define._UpdateAllMetaProperties:
                                self._totalTestCase += 1
                                fullUpdateName = 'My Default All Meta Properties Update ' + className
                                fullUpdateDescription = 'This is the description of my default all meta properties update for ' + className
                                requestBody = NsmUtil.createRequestBodyProperty(className, fullUpdateName, fullUpdateDescription, metaPropertiesLines, storage)
                                result = self.testUpdate(className, requestBody, category, testCaseId)
                                result = NsmUtil.printResult(result, category)
                                self._resultList.append([className, name, action, category, str(testCaseId)+'-all', str(result)])
                            
                        ### for ip reservation and key = request.body.file.
                        else:
                            self._totalTestCase += 1
                            NsmUtil.printHeadLine2(className + ' [' + name + '] - ' + action + ' - ' + category + ' - test case ' + str(testCaseId) + '-' + str(self._totalTestCase))
                            result = thisObject.updateByTemplate(className, testCase, category, testCaseId)
                            name = thisObject.createName
                            result = NsmUtil.printResult(result, category)
                            self._resultList.append([className, name, action, category, str(testCaseId)+'-'+str(self._totalTestCase), str(result)])
                        
                    elif action == 'delete' and online:
                        result = thisObject.delete(testCaseId)
                        name = thisObject.createName
                        result = NsmUtil.printResult(result, category)
                        self._resultList.append([className, name, action, category, str(testCaseId), str(result)])
                        
                    ## it may be a dead code now
                    elif action == 'list':
                        if online: thisObject.setOnLine()
                        elif not online: thisObject.setOffLine()
                        
                        listUrl = None
                        if className == 'Provider': 
                            listUrl = Define._UrlApiRoot + '/top/provider'
                        elif className == 'Pod':
                            providerName = testCase['provider-name']
                            providerUid = self.getUid('Provider', providerName)
                            listUrl = providerUid + '/pod'
                        fileDashName = thisObject.createName.replace(' ', '-')
                        responseFilePath = Define._PathResponseCreateDefault + '/' + fileDashName + '-list-' + testCaseId + '.xml'
                        objectList = thisObject.getList(listUrl, responseFilePath)
                        name = thisObject.createName
                        self._logger.debug('write ' + className + ' [' + name + '] list to file ' + responseFilePath)
                        result = NsmUtil.printResult(objectList, category)
                        self._resultList.append([className, name, action, category, str(testCaseId), str(result)])
     
                except:
                    self._logger.error('!!!!!!!!!!!!! error !!!!!!!!!!!!!')
                    errorType = sys.exc_info()[0]
                    errorValue = sys.exc_info()[1]
                    errorTraceBack = traceback.extract_tb(sys.exc_info()[2])
                    self._logger.error('Error Type: ' + str(errorType))
                    self._logger.error('Error Value: ' + str(errorValue))
                    self._logger.error('Traceback: ')
                    for oneStack in errorTraceBack:
                        self._logger.error(oneStack)
                    
                    
        return self._thisObject
    
    
            
        

    @staticmethod
    def start1():
        test = Test()
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
        test = Test()
        test.start()
        NsmUtil.saveUid(test._uidList)
        NsmUtil.saveResult(test._resultList)
        NsmUtil.printHeadLine2('total test case: ' + str(test._totalTestCase))
        NsmUtil.printHeadLine1('test completed')

if __name__ == "__main__":
    Test.start1()
    
    
    
    
    
    