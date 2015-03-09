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
from isp.podFull import PodFull
from isp.podFury import PodFury
from isp.podNoEdge import PodNoEdge
from isp.podNoAccess import PodNoAccess
from isp.podNoEdgeAccess import PodNoEdgeAccess
from isp.tenant import Tenant
from isp.externalNetwork import ExternalNetwork
from isp.tenantNetworkContainer import TenantNetworkContainer
from isp.providerNetworkContainer import ProviderNetworkContainer
from isp.internetEdgeZone import InternetEdgeZone
from isp.southZone import SouthZone
from isp.northZone import NorthZone
from isp.layer3ExplicitSubnet import Layer3ExplicitSubnet
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


class Test(object):

    #__online1,  __online2, __online3, __online4, __online5 = True, True, True, True, True
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
            
            
    def testProviderIpAddressPool(self, providerPod, name, poolType, testCaseId, online):
        NsmUtil.printHeadLine2('Provider IpAddressPool' + ' [' + poolType + '] - ' + 'detail' + ' - ' + 'positive' + ' - test case ' + str(testCaseId))
        self._totalTestCase += 1
        
        ipAddressPoolUid = None
        if poolType == 'Global': ipAddressPoolUid = providerPod.getGlobalIpAddressPoolUid()
        else: ipAddressPoolUid = providerPod.getInfrastructureIpAddressPoolUid()
        
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
        
    
    def testUpdate(self, className, requestBody, category, testCaseId, totalTestCaseId):
        testCaseIdStr = str(testCaseId) + '-' + str(totalTestCaseId)
        result = self._thisObject.update(className, requestBody, category, testCaseIdStr)
        return result
        
        
    def testUpdateVerification(self, result, thisObject, pod, updateVerificationPatternList, className, name, category, testCaseId,storage):
        if result and Define._Verfiy and Define._VerifyUpdate:
            thisObject.setPod(pod)
            result = thisObject.verifyUpdate(updateVerificationPatternList, storage)
            result = NsmUtil.printResult(result, category)
            self._resultList.append([className, name, 'update-verify', category, str(testCaseId), str(result)])
            return result
        else:
            return None
           

    def getStressObjectName(self, name, className):
        if className in ['NsmV1', 'Top', 'Provider']:
            return name
        elif className.startswith('Pod'):
            name += ' pod' + str(Define._PodIndex)
            return name
        else:
            name += ' pod' + str(Define._PodIndex) + ' tenant' + str(Define._TenantIndex)
            return name
        
        
    def getStressObjectName1(self, name, className):
        if className in ['NsmV1', 'Top', 'Provider']:
            return name
        elif className.startswith('Pod'):
            name += ' pod' + str(Define._PodIndex)
            return name
        elif className == 'Tenant':
            name += ' pod' + str(Define._PodIndex) + ' tenant' + str(Define._TenantIndex)
            return name
        else:
            return name

    def run(self, catalog, testCaseFileName, online, pod=None, currentObject=None):
        testCaseFilePath = Define._PathTestCase + '/' + testCaseFileName
        json_data = open(testCaseFilePath)
        self._logger.debug('test case json file path: ' + testCaseFilePath)
        data = json.load(json_data)
        #pprint(data)
        json_data.close()
                                
        for className, testSuite in data.items():
            NsmUtil.printHeadLine1(' class: ' + className )
            
            #thisObject = eval(className)(catalog, None, None, None, None)
            #name = None
            
            thisObject = None
            name = None
            if currentObject:
                thisObject = currentObject
                name = thisObject.createName
                self._thisObject = thisObject
            else:
                thisObject = eval(className)(catalog, None, None, None, None)
                
                            
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
                
                
                if 'name' in testCase.keys(): 
                    name = testCase['name']
                    
                    if Define._StressTest:
                        name = self.getStressObjectName(name, className)
                            
                         
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
                        
                        if Define._StressTest:
                            uidObjectName = self.getStressObjectName(uidObjectName, uidClassName)
                            
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
                        
                        
                        if Define._Performance and NsmUtil.isPerfClass(className):
                            Define._CurrentPerfClassName = className
                            Define._CurrentPerfObjectName = name
                            Define._CurrentPerfAction = action
                            
                            
                        if name: thisObject.setCreateName(name)
                        if description: thisObject.setCreateDescription(description)
                        if requestBodyFileName: thisObject.setRequestBodyFile(requestBodyFileName)
                        if testCase: thisObject.setRequestBodyParams(testCase)                    
                    
                        result = thisObject.create(testCaseId)
                        name = thisObject.createName
                        result = NsmUtil.printResult(result, category)
                        self._resultList.append([className, name, action, category, str(testCaseId), str(result)])
                        
                        
                        if Define._Performance and NsmUtil.isPerfClass(className):
                            Define._CurrentPerfClassName = None
                            Define._CurrentPerfObjectName = None
                            Define._CurrentPerfAction = None
                            
                            
                        if Define._Performance and (className == 'Tenant' or className == 'ProviderNetworkContainer'):
                            Define._PerformanceData.setCurrentTenantName(name)
                            
            
                        if not className in self._dataStore.keys(): self._dataStore[className] = {}
                        if not name in self._dataStore[className].keys(): self._dataStore[className][name] = {}
                        self._dataStore[className][name]['object'] = thisObject
                        self._thisObject = thisObject
                        
                        if result and Define._Verfiy and Define._VerifyCreate:
                            thisObject.setPod(pod)
                            result = thisObject.verifyCreate()
                            result = NsmUtil.printResult(result, category)
                            self._resultList.append([className, name, 'create-verify', category, str(testCaseId), str(result)])
            
                    elif action == 'detail':
                        if online: thisObject.setOnLine()
                        elif not online: thisObject.setOffLine()
                        
                        detail = thisObject.getDetail(testCaseId)
                        name = thisObject.createName
                        result = NsmUtil.printResult(detail, category)
                        self._resultList.append([className, name, action, category, str(testCaseId), str(result)])
                        
                        finalSubClassName = thisObject.mySubClassName
                        if thisObject.mySubClassName in ['PodFull', 'PodNoEdge', 'PodNoAccess', 'PodNoEdgeAccess', 'PodFury']:
                            finalSubClassName = 'Pod'
                            
                        self.addUid([thisObject.uid, finalSubClassName, thisObject.createName])
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
                        
                    elif action == 'update' and Define._Update:

                        if online: thisObject.setOnLine()
                        elif not online: thisObject.setOffLine()
                        
                        NsmUtil.printHeadLine2('Test update is being called')
                        updateIndex = 1
                        storage = {}
                        metaPropertiesLines = None
                        ### for csv file defined in test case json file
                        if 'test.case.file' in testCase.keys():
                            metaPropertyTestCaseFileName = testCase['test.case.file']
                            if not metaPropertyTestCaseFileName in self._metaPropertyTestCases.keys():
                                testCaseFilePath = Define._PathReqeustBodyUpdate + '/' + testCase['test.case.file']
                                metaProperties = NsmUtil.getMetaProperties(testCaseFilePath)
                                self._metaPropertyTestCases[metaPropertyTestCaseFileName] = metaProperties
                            self._logger.debug('className: ' + className + '; name: ' + name)     
                            metaPropertiesLines = self._metaPropertyTestCases[metaPropertyTestCaseFileName][className][name]        
                            
                            requestBody = None
                            
                            storage['_uidList'] = self._uidList
                            storage['_internetEdgeZoneLayer3VlanReservedIpAddressList'] = self._internetEdgeZoneLayer3VlanReservedIpAddressList
                            storage['_securedInternetEdgeZoneLayer3VlanReservedIpAddressList'] = self._securedInternetEdgeZoneLayer3VlanReservedIpAddressList

                            
                            if testCase['test.case.file'] == 'update-all-meta-properties.csv' or testCase['test.case.file'] == 'update-all-meta-properties-simplified.csv':
                                
                                if Define._UpdateSingleMetaProperties:
                                    NsmUtil.printHeadLine2(className + ' [' + name + '] - ' + action + ' description - ' + category + ' - test case ' + str(testCaseId) + '-' + str(updateIndex))
                                    updateDescription = 'This is the update description of my ' + name
                                    requestBody, updateVerificationPatternList = NsmUtil.createRequestBodyProperty(className, thisObject.createName, updateDescription)
                                    result = self.testUpdate(className, requestBody, category, testCaseId, updateIndex)
                                    updateIndex += 1
                                    self._totalTestCase += 1
                                    result = NsmUtil.printResult(result, category)
                                    self._resultList.append([className, name, action, category, str(testCaseId)+'-'+str(updateIndex), str(result)])
                                    
                                    ### can't udpate pod name at this moment
                                    if className != 'Pod':
                                        NsmUtil.printHeadLine2(className + ' [' + name + '] - ' + action + ' name - ' + category + ' - test case ' + str(testCaseId) + '-' + str(updateIndex))
                                        updateName = 'My Default Update ' + name 
                                        requestBody, updateVerificationPatternList = NsmUtil.createRequestBodyProperty(className, updateName)
                                        result = self.testUpdate(className, requestBody, category, testCaseId, updateIndex)
                                        updateIndex += 1
                                        self._totalTestCase += 1
                                        result = NsmUtil.printResult(result, category)
                                        self._resultList.append([className, name, action, category, str(testCaseId)+'-'+str(updateIndex), str(result)])
                                    
                                    for oneMetaProperties in metaPropertiesLines:
                                        NsmUtil.printHeadLine2(className + ' [' + name + '] - ' + action + ' - ' + category + ' - test case ' + str(testCaseId) + '-' + str(updateIndex))
                                        metaPropertiesWrapperList = []
                                        metaPropertiesWrapperList.append(oneMetaProperties)
                                        requestBody, updateVerificationPatternList = NsmUtil.createRequestBodyProperty(className, thisObject.createName, None, metaPropertiesWrapperList, storage)
                                        result = self.testUpdate(className, requestBody, category, testCaseId, updateIndex)
                                        updateIndex += 1
                                        self._totalTestCase += 1
                                        result = NsmUtil.printResult(result, category)
                                        self._resultList.append([className, name, action, category, str(testCaseId)+'-'+str(updateIndex), str(result)])
                                                                        
                                        result = self.testUpdateVerification(result, thisObject, pod, updateVerificationPatternList, className, name, category, testCaseId, storage)
                                    
                                # all meta properties
                                if Define._UpdateAllMetaProperties:
                                    NsmUtil.printHeadLine2(className + ' [' + name + '] - ' + action + ' - ' + category + ' - test case ' + str(testCaseId) + '-999')
                                    fullUpdateName = name
                                    fullUpdateDescription = 'This is the description of my all meta properties update for ' + name
                                    requestBody, updateVerificationPatternList = NsmUtil.createRequestBodyProperty(className, fullUpdateName, fullUpdateDescription, metaPropertiesLines, storage)
                                    result = self.testUpdate(className, requestBody, category, testCaseId, 999)
                                    updateIndex += 1
                                    self._totalTestCase += 1
                                    result = NsmUtil.printResult(result, category)
                                    self._resultList.append([className, name, action, category, str(testCaseId)+'-999', str(result)])
                            
                                    result = self.testUpdateVerification(result, thisObject, pod, updateVerificationPatternList, className, name, category, testCaseId, storage)
                                            
                            # test.case.file is not update-all-meta-properties.csv
                            else:
                                NsmUtil.printHeadLine2(className + ' [' + name + '] - ' + action + ' - ' + category + ' - test case ' + str(testCaseId) + '-' + str(updateIndex))
                                requestBody, updateVerificationPatternList = NsmUtil.createRequestBodyProperty(className, name, None, metaPropertiesLines, storage)
                                result = self.testUpdate(className, requestBody, category, testCaseId, updateIndex)
                                updateIndex += 1
                                self._totalTestCase += 1
                                result = NsmUtil.printResult(result, category)
                                self._resultList.append([className, name, action, category, str(testCaseId)+'-'+str(updateIndex), str(result)])
                                
                                result = self.testUpdateVerification(result, thisObject, pod, updateVerificationPatternList, className, name, category, testCaseId, storage)
                            
                        ### assume it is the only place to update name so far
                        elif 'name' in testCase.keys():
                            
                            updateName = testCase['name']
                            updateDescription = testCase['description'] if 'description' in testCase.keys() else None
                            requestBody, updateVerificationPatternList = NsmUtil.createRequestBodyProperty(className, updateName, updateDescription, metaPropertiesLines, storage)
                            result = self.testUpdate(className, requestBody, category, testCaseId, 999)
                            updateIndex += 1
                            self._totalTestCase += 1
                            result = NsmUtil.printResult(result, category)
                            self._resultList.append([className, name, action, category, str(testCaseId)+'-999', str(result)])
                            result = self.testUpdateVerification(result, thisObject, pod, updateVerificationPatternList, className, name, category, testCaseId, storage)
                            
                            '''
                            1, remove old -> self._dataStore[className][name]['object'] = thisObject
                            2, add new -> self._dataStore[className][updateName]['object'] = thisObject
                            3, addUid is needed
                            '''
                            
                        ### huhe    
                        
                        ### for ip reservation and key = request.body.file (diff between request.body.file and test.case.file)
                        else:
                            NsmUtil.printHeadLine2(className + ' [' + name + '] - ' + action + ' - ' + category + ' - test case ' + str(testCaseId))
                            result = thisObject.updateByTemplate(className, testCase, category, testCaseId)
                            name = thisObject.createName
                            result = NsmUtil.printResult(result, category)
                            self._resultList.append([className, name, action, category, str(testCaseId), str(result)])
                            
                            ### update verification???
                        
                        
                            
                    elif action == 'delete':
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
                    self._logger.error('!!!!!!!!!!!!! exception in Test.run() !!!!!!!!!!!!!')
                    errorType = sys.exc_info()[0]
                    errorValue = sys.exc_info()[1]
                    errorTraceBack = traceback.extract_tb(sys.exc_info()[2])
                    self._logger.error('Error Type: ' + str(errorType))
                    self._logger.error('Error Value: ' + str(errorValue))
                    self._logger.error('Traceback: ')
                    for oneStack in errorTraceBack:
                        self._logger.error(oneStack)
                    
                    
        return self._thisObject
    
    
    
    
    
    