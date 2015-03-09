'''
Created on Jul 15, 2012

@author: huhe
'''

from datetime import datetime
import os.path
from lib import Util, HttpUtil
import Define, XPath
from isp.task import Task
from isp.nsmUtil import NsmUtil


class Element():
    '''
    classdocs
    '''
    
    _uidList = []
    
    def __init__(self):
        '''
        Constructor
        '''
        self.logger = Util.getLogger(self.__class__.__name__)
        
        self.mySubClassName = self.__class__.__name__
        self.logger.info('')
        self.logger.info('')
        self.logger.info('======================>>>>>> class name: ' + self.mySubClassName + ' <<<<<<<======================')
        self.logger.info('')
        self.logger.info('')
        
        self.getCatalogUrl = ''
        
        # for matching catalog
        self.catalogServiceOfferingType = ''
        self.catalogServiceOfferingName = ''
        self.catalogLinkTitle = ''
        
        # get from parent catalog for this child creation
        self.catalogUid = ''
        self.catalogName = ''
        self.catalogDescription = ''
        self.catalogVersion = ''
        self.catalogSelfUrl = ''
        self.catalogCreateUrl = ''
        
        self.createUid = ''
        self.createName = ''
        self.createDescription = ''
                
        self.createTaskXml = None
        self.getDetailUrl = ''
        self.detailXml = ''
        self.catalogXml = ''
        
        self.deleteUrl = ''
        self.deleteTaskXml = ''
        
        self.updateUrl = ''
        self.updateTaskXml = ''
        
        self.requestBodyFileName = ''
        self.requestBodyFilePath = ''
        self.requestParams = {}
        
        # get from detail
        self.uid = ''
        
        self.pod = None
        
        # debug switch, online by default
        self.isOffLine = False
        
            
    def setOffLine(self):
        self.isOffLine = True
        
        
    def setOnLine(self):
        self.isOffLine = False
        
        
    def setCatalogMatchParameter(self, offeringType, offeringName, linkTitle):
        self.catalogServiceOfferingType = offeringType
        self.catalogServiceOfferingName = offeringName
        self.catalogLinkTitle = linkTitle
        
        
    def setCreateParameter(self, name, description, requestFileName, requestParams):
        self.createName = name
        if self.createName:
            self.logger.info('-----------> element object name: ' + self.createName)
        self.logger.info('')
        self.createDescription = description
        self.requestBodyFileName = requestFileName
        self.requestParams = requestParams
        
        
    def setCreateName(self, name):
        self.createName = name
        self.logger.info('-----------> element object name: ' + self.createName)
        self.logger.info('')
        
        
    def setCreateDescription(self, description):
        self.createDescription = description
        
        
    def setRequestBodyParams(self, requestParams):
        self.requestParams = requestParams
            
            
    def setRequestBodyFile(self, requestBodyFileName):
        self.requestBodyFileName = requestBodyFileName
        
        
    def setUid(self, uid):
        self.uid = uid
        
        
    def setPod(self, pod):
        self.pod = pod
        
        
    def populateCreateParameter(self):
        Element.populateRequestBodyFile(self)
        Element.populateRequestBodyParams(self)
        Element.populateCreateName(self, self.createName)
        Element.populateCreateDescription(self, self.createDescription)
    

    def populateRequestBodyFile(self):
        if not self.requestBodyFileName:
            raise ValueError('request body file is not defined')
        self.requestBodyFilePath = Define._PathRequestBodyCreateDefault + '/' + self.requestBodyFileName
        if (not os.path.isfile(self.requestBodyFilePath)):
            raise ValueError('request body file ' + self.requestBodyFilePath + ' is not a file or not existing')
        self.logger.info('request body file is set to ' + self.requestBodyFilePath)
        
        
    def populateRequestBodyParams(self):
        if not self.requestParams:
            self.requestParams = {}
            
            
    def populateCreateName(self, name):
        if not name:
            try:
                self.createName = self.requestParams['name']
            except KeyError:
                self.createName = Util.getXpathValue(Util.readFile(self.requestBodyFilePath), XPath._RequestBodyName)
                if (self.createName.startswith('$')):
                    raise ValueError('request body name [' + self.createName + '] is not defined in file ' + self.requestBodyFilePath)
        self.logger.info('-----------> element object name or create name: ' + self.createName)
        
            
    def populateCreateDescription(self, description):
        if not description:
            try:
                self.createDescription = self.requestParams['description']
            except KeyError:
                self.createDescription = Util.getXpathValue(Util.readFile(self.requestBodyFilePath), XPath._RequestBodyDescription)
                if (self.createDescription.startswith('$')):
                    raise ValueError('request body description [' + self.createDescription + '] is not defined in file ' + self.requestBodyFilePath)
        
        
    def getCatalog(self, testCaseId='000'):
        
        NsmUtil.printHeadLine2('START: get catalog test case ' + testCaseId)
        
        self.logger.debug('get catalog request: ' + self.getCatalogUrl)
        nameDash = self.createName.replace(' ', '-')
        debugCatalogFilePath = Define._PathResponseCreateDefault + '/' + nameDash + '-catalog-' + testCaseId + '.xml'
        
        if (self.isOffLine):
            self.logger.debug('get catalog from file: ' + debugCatalogFilePath)
            self.catalogXml = Util.readFile(debugCatalogFilePath)
        else:
            self.catalogXml = HttpUtil.doGet(self.getCatalogUrl, Define._credential) if self.getCatalogUrl and self.getCatalogUrl != '' else None
            if self.catalogXml:
                self.logger.debug('catalog output file: ' + debugCatalogFilePath)
                Util.writeFile(debugCatalogFilePath, self.catalogXml)
            
        NsmUtil.printHeadLine2('END: get catalog test case ' + testCaseId)
        return self.catalogXml
    
    
    def evaluateXpath(self, xpath):
        xpath = xpath.replace('${offering-type}', self.catalogServiceOfferingType)
        xpath = xpath.replace('${offering-name}', self.catalogServiceOfferingName)
        xpath = xpath.replace('${link-title}', self.catalogLinkTitle)
        return xpath
    
    
    # for generic catalog with only one services
    def parseCatalog(self, catalog):
        evalXpath = Element.evaluateXpath(self, XPath._CatalogUid)
        self.catalogUid = Util.getXpathValue(catalog, evalXpath)
        self.logger.info('catalog uid: ' + self.catalogUid)
        self.createUid = self.catalogUid
        
        evalXpath = Element.evaluateXpath(self, XPath._CatalogName)
        self.catalogName = Util.getXpathValue(catalog, evalXpath)
        self.logger.info('catalog name: ' + self.catalogName)
        
        evalXpath = Element.evaluateXpath(self, XPath._CatalogDescription)
        self.catalogDescription = Util.getXpathValue(catalog, evalXpath)
        self.logger.info('catalog description: ' + self.catalogDescription)
        
        evalXpath = Element.evaluateXpath(self, XPath._CatalogVersion)
        self.catalogVersion = Util.getXpathValue(catalog, evalXpath)
        self.logger.info('catalog version: ' + self.catalogVersion)
        
        evalXpath = Element.evaluateXpath(self, XPath._CatalogLinkSelf)
        self.catalogSelfUrl = Util.getXpathValue(catalog, evalXpath)
        self.logger.info('catalog self url: ' + self.catalogSelfUrl)
        
        evalXpath = Element.evaluateXpath(self, XPath._CatalogLinkCreate)
        self.catalogCreateUrl = Util.getXpathValue(catalog, evalXpath)
        self.logger.info('catalog create url: ' + self.catalogCreateUrl)
        
        
    def create(self, testCaseId):
        
        NsmUtil.printHeadLine2('START: create test case ' + testCaseId)
        
        Element.populateCreateParameter(self)
        
        requestBody = Util.readFile(self.requestBodyFilePath)
        requestBody = requestBody.replace('${uid}', self.createUid)
        requestBody = requestBody.replace('${name}', self.createName)
        requestBody = requestBody.replace('${description}', self.createDescription)
        
        for key, value in self.requestParams.items():
            keyStr = '${' + key + '}'
            requestBody = requestBody.replace(keyStr, value)
        
        self.logger.info('create request: ' + self.catalogCreateUrl)
        
        # pod creation request body is too huge, skip it
        if self.mySubClassName != 'Pod':
            self.logger.info('request body: ' + "\n\n" + requestBody +"\n")
        
        nameDash = self.createName.replace(' ', '-')
        debugCreateFilePath = Define._PathResponseCreateDefault + '/' + nameDash + '-create-' + testCaseId + '.xml'
        
        status = None
        if (self.isOffLine):
            timeStart = datetime.now()
            
            self.logger.debug('get create task from file: ' + debugCreateFilePath)
            self.createTaskXml = Util.readFile(debugCreateFilePath)
            
            myTask = Task(self.createTaskXml)
            status = myTask.checkResult()
            self.createTaskXml = myTask.taskXml
            
            if Define._Performance and Define._CurrentPerfAction:
                timeEnd = datetime.now()
                Define._PerformanceData.setCurrentTenantClassLog(Define._CurrentPerfClassName, Define._CurrentPerfObjectName, Define._CurrentPerfAction, timeStart, timeEnd)
            
        else:
            timeStart = datetime.now()
            
            self.createTaskXml = HttpUtil.doPost(self.catalogCreateUrl, Define._credential, requestBody)
            self.logger.debug('write pending create task to file: ' + debugCreateFilePath + '-pending.xml')
            Util.writeFile(debugCreateFilePath+'-pending.xml', self.createTaskXml)
            
            myTask = Task(self.createTaskXml)
            status = myTask.checkResult()
            self.createTaskXml = myTask.taskXml
    
            if Define._Performance and Define._CurrentPerfAction:
                timeEnd = datetime.now()
                Define._PerformanceData.setCurrentTenantClassLog(Define._CurrentPerfClassName, Define._CurrentPerfObjectName, Define._CurrentPerfAction, timeStart, timeEnd)
    
            self.logger.info('write final create task to file ' + debugCreateFilePath)
            #self.logger.info(self.createTaskXml)
            Util.writeFile(debugCreateFilePath, self.createTaskXml)
            
        NsmUtil.printHeadLine2('END: create test case ' + testCaseId)
        return status
        
        
    def getDetail(self, testCaseId):
        
        NsmUtil.printHeadLine2('START: get detail test case ' + testCaseId)
        
        nameDash = self.createName.replace(' ', '-')
        debugDetailFilePath = Define._PathResponseCreateDefault + '/' + nameDash + '-detail-' + testCaseId + '.xml'
        
        if (self.isOffLine):
            self.logger.debug('get detail from file: ' + debugDetailFilePath)
            self.detailXml = Util.readFile(debugDetailFilePath)
        else:    
            try:
                self.getDetailUrl = Util.getXpathValue(self.createTaskXml, XPath._TaskElementUid)
            except:
                self.getDetailUrl = self.uid
            self.logger.info('get detail url: ' + self.getDetailUrl)
            self.detailXml = HttpUtil.doGet(self.getDetailUrl, Define._credential) if self.getDetailUrl and self.getDetailUrl != '' else None
            if self.detailXml:
                self.logger.debug('write detail to file: ' + debugDetailFilePath)
                Util.writeFile(debugDetailFilePath, self.detailXml)
                    
        if self.detailXml:
            self.uid = Util.getXpathValue(self.detailXml, XPath._DetailUid)
            self.logger.info('uid for ' + self.createName + ': ' + self.uid)
            self.getCatalogUrl = Util.getXpathValue(self.detailXml, XPath._DetailLinkCatalog)
            Element._uidList.append([self.uid, self.mySubClassName, self.createName])
        
        NsmUtil.printHeadLine2('END: get detail test case ' + testCaseId)
        return self.detailXml
    
    
    ### for ip pool & resvervation
    def getRequest(self, getUrl, debugDetailFilePath):
            
        getResponseXml = None
        self.logger.info('get request url: ' + getUrl)
        if (self.isOffLine):
            self.logger.debug('get response from file: ' + debugDetailFilePath)
            getResponseXml = Util.readFile(debugDetailFilePath)
        else:    
            getResponseXml = HttpUtil.doGet(getUrl, Define._credential)
            self.logger.debug('write response to file: ' + debugDetailFilePath)
            Util.writeFile(debugDetailFilePath, getResponseXml)
        
        '''
        uid = Util.getXpathValue(getResponseXml, XPath._DetailUid)
        self.logger.info('uid: ' + uid)
        getCatalogUrl = Util.getXpathValue(getResponseXml, XPath._DetailLinkCatalog)
        return getCatalogUrl
        '''
        return getResponseXml
    
    
    ### for provider and pod list
    def getList(self, getUrl, listClassName, testCaseId):
        
        NsmUtil.printHeadLine2('START: get ' + listClassName + ' list test case ' + testCaseId)
        
        nameDash = self.createName.replace(' ', '-')
        debugDetailFilePath = Define._PathResponseCreateDefault + '/' + nameDash + '-' + listClassName + '-list-' + testCaseId + '.xml'
        
        getResponseXml = None
        self.logger.info('get list url: ' + getUrl)
        if (self.isOffLine):
            self.logger.debug('get ' + listClassName + ' list response from file: ' + debugDetailFilePath)
            getResponseXml = Util.readFile(debugDetailFilePath)
        else:    
            getResponseXml = HttpUtil.doGet(getUrl, Define._credential)
            self.logger.debug('write ' + listClassName + ' list response to file: ' + debugDetailFilePath)
            Util.writeFile(debugDetailFilePath, getResponseXml)
        
        NsmUtil.printHeadLine2('END: get ' + listClassName + ' list test case ' + testCaseId)
        return getResponseXml
    
    
    def delete(self, testCaseId):
        
        NsmUtil.printHeadLine2('START: delete test case ' + testCaseId)

        self.deleteUrl = self.uid + '/delete'
        nameDash = self.createName.replace(' ', '-')
        debugDeleteFilePath = Define._PathResponseDelete + '/' + nameDash + '-delete-' + testCaseId + '.xml'
        self.logger.info('delete url: ' + self.deleteUrl)
        
        status = None
        if (self.isOffLine):
            self.logger.debug('get delete task from file: ' + debugDeleteFilePath)
            self.deleteTaskXml = Util.readFile(debugDeleteFilePath)
            
            myTask = Task(self.deleteTaskXml)
            status = myTask.checkResult()
            self.deleteTaskXml = myTask.taskXml
        else:
            self.deleteTaskXml = HttpUtil.doPost(self.deleteUrl, Define._credential)
            self.logger.debug('write pending delete task to file: ' + debugDeleteFilePath + '-pending.xml')
            Util.writeFile(debugDeleteFilePath+'-pending.xml', self.deleteTaskXml)
            
            myTask = Task(self.deleteTaskXml)
            status = myTask.checkResult()
            self.deleteTaskXml = myTask.taskXml
    
            self.logger.info('write to file ' + debugDeleteFilePath)
            #self.logger.info(self.deleteTaskXml)
            Util.writeFile(debugDeleteFilePath, self.deleteTaskXml)
             
        NsmUtil.printHeadLine2('END: delete test case ' + testCaseId)
        return status
    
    
    def updateByTemplate(self, objectClassName, updateRequestBodyParams, category, testCaseId):
        
        NsmUtil.printHeadLine2('update by template test case ' + testCaseId)
        
        self.updateUrl = self.uid + '/put'
        paramKeys = updateRequestBodyParams.keys()
        
        # priority: updateRequestBodyParams, update-tenant-all.xml
        requestBodyFileName = None
        if 'request.body.file' in paramKeys:
            requestBodyFileName = updateRequestBodyParams['request.body.file']
        requestBodyFilePath = Define._PathReqeustBodyUpdate + '/' + objectClassName + '/' + requestBodyFileName
        requestBody = Util.readFile(requestBodyFilePath)
        
        # priority: built-in request body file, updateRequestBodyParams, self.createName
        name = self.createName + ' Update ' + category + ' ' + str(testCaseId) 
        if 'name' in paramKeys:
            name = updateRequestBodyParams['name']
            
        description = self.createDescription.replace('Default', 'Default Update')
        if 'description' in paramKeys:
            description = updateRequestBodyParams['description']
                
        requestBody = requestBody.replace('${uid}', self.uid)
        requestBody = requestBody.replace('${name}', name)
        requestBody = requestBody.replace('${description}', description)
        for key, value in updateRequestBodyParams.items():
            if key == 'uid':
                for uidKey, uidValue in value.items():
                    keyStr = '${' + uidKey + '}'
                    main_module = __import__("__main__")
                    varObj = getattr(main_module, uidValue)
                    requestBody = requestBody.replace(keyStr, varObj.uid)                 
            else:   
                keyStr = '${' + key + '}'
                requestBody = requestBody.replace(keyStr, value)
        self.update(objectClassName, requestBody, category, testCaseId)
    
    
    def update(self, objectClassName, requestBody, category, testCaseId):
        
        NsmUtil.printHeadLine2('START: update test case ' + str(testCaseId))
        
        self.updateUrl = self.uid + '/put'
        self.logger.info('update request url: ' + self.updateUrl)
        if self.mySubClassName != 'Pod':
            self.logger.info('request body: ' + "\n\n" + requestBody +"\n")
        else:
            podRequestFilePath = Define._PathLog + '/pod-request-body.xml'
            Util.writeFile(podRequestFilePath, requestBody)
        
        name = self.createName + ' Update ' + category + ' ' + str(testCaseId) 
        nameDash = name.replace(' ', '-')
        
        debugUpdateClassPath = Define._PathResponseUpdate + '/' + objectClassName
        Util.mkdir(debugUpdateClassPath)
        debugUpdateFilePath = debugUpdateClassPath + '/' + nameDash + '.xml'
        
        status = None
        if (self.isOffLine):
            self.logger.debug('get update task from file: ' + debugUpdateFilePath)
            self.updateTaskXml = Util.readFile(debugUpdateFilePath)
            
            myTask = Task(self.updateTaskXml)
            status = myTask.checkResult()
            self.updateTaskXml = myTask.taskXml
        else:
            self.updateTaskXml = HttpUtil.doPost(self.updateUrl, Define._credential, requestBody)
            if not self.updateTaskXml:
                return False
                
            self.logger.debug('write pending update task to file: ' + debugUpdateFilePath + '-pending.xml')
            Util.writeFile(debugUpdateFilePath+'-pending.xml', self.updateTaskXml)
            
            myTask = Task(self.updateTaskXml)
            status = myTask.checkResult()
            self.updateTaskXml = myTask.taskXml

            self.logger.info('write final update task to file ' + debugUpdateFilePath)
            #self.logger.info(self.updateTaskXml)
            Util.writeFile(debugUpdateFilePath, self.updateTaskXml)
                
        NsmUtil.printHeadLine2('END: update test case ' + str(testCaseId))
        return status
        
    ### the following three are for pool and reservation only
    def getAllocated(self, testCaseId):
        
        NsmUtil.printHeadLine2('START: get ip allocated test case ' + str(testCaseId))
        
        allocatedUrl = self.relLinkDictionary['nsmr:ipallocated']
        responseFileName = self.createName + '-allocated-' + testCaseId + '.xml'
        responseFilePath = Define._PathResponseCreateDefault + '/' + responseFileName
        responseFilePath = responseFilePath.replace(' ', '-')
        responseXml = Element.getRequest(self, allocatedUrl, responseFilePath)
    
        NsmUtil.printHeadLine2('END: get ip allocated test case ' + str(testCaseId))
        return responseXml
    
    
    def getAvailable(self, testCaseId):
        
        NsmUtil.printHeadLine2('START: get ip available test case ' + str(testCaseId))
        
        allocatedUrl = self.relLinkDictionary['nsmr:ipavailable']
        responseFileName = self.createName + '-available-' + testCaseId + '.xml'
        responseFilePath = Define._PathResponseCreateDefault + '/' + responseFileName
        responseFilePath = responseFilePath.replace(' ', '-')
        responseXml = Element.getRequest(self, allocatedUrl, responseFilePath)
    
        NsmUtil.printHeadLine2('END: get ip available test case ' + str(testCaseId))
        return responseXml
    
    
    def getReservations(self, testCaseId):
        
        NsmUtil.printHeadLine2('START: get ip reservation test case ' + str(testCaseId))
        
        allocatedUrl = self.relLinkDictionary['nsmr:ipreservations']
        responseFileName = self.createName + '-reservations-' + testCaseId + '.xml'
        responseFilePath = Define._PathResponseCreateDefault + '/' + responseFileName
        responseFilePath = responseFilePath.replace(' ', '-')
        responseXml = Element.getRequest(self, allocatedUrl, responseFilePath)
    
        NsmUtil.printHeadLine2('END: get ip reservation test case ' + str(testCaseId))
        return responseXml
    
    
    def verifyUpdate(self, updateVerificationPatternList, storage):
        if self.mySubClassName != 'Pod' and self.isOffLine and self.updateTaskXml: self.logger.info(Util.prettfyXmlByString(self.updateTaskXml))
        
        NsmUtil.printHeadLine2('START: update response verification: parameters from request body')
        
        status = True
        for pattern in updateVerificationPatternList:
            if self.updateTaskXml.find(pattern) < 0:
                status = False
                NsmUtil.printStatusHeadLine2('Failed: pattern not found: ' + pattern)
            else:
                NsmUtil.printStatusHeadLine2('Passed: pattern found: ' + pattern)
        
        NsmUtil.printHeadLine2('END: update response verification: parameters from request body')
        return status
    
    
    def verifyCreate(self):
        if self.mySubClassName != 'Pod' and self.isOffLine and self.createTaskXml: self.logger.info(Util.prettfyXmlByString(self.createTaskXml))
        
        NsmUtil.printHeadLine2('START: create response verification: parameters from request body')
        
        status = True
        for key, value in self.requestParams.items():
            keyItems = key.split('.')
            pattern = None
            if key.endswith('.ipv4.start'):
                pattern = '<ipv4Start>' + value + '</ipv4Start>'
            elif key.endswith('.ipv4.end'):
                pattern = '<ipv4End>' + value + '</ipv4End>'
            elif key.endswith('.ipv4') or key.endswith('.mask') or key.endswith('.protocol') or key.endswith('.start') or key.endswith('.end') or key.endswith('.ASNumber') or key.endswith('.uid') or key == 'name' or key == 'description':
                pattern = '<' + keyItems[-1] + '>' + value + '</' + keyItems[-1] + '>'
            elif key.endswith('.netmask'):
                pattern = '<integer>' + value + '</integer>'
            elif key.startswith('serverfarm.probe.') or key == 'lb.algorithm':
                pattern = '<string>' + value + '</string>'
            elif key.endswith('redirect.port'):
                pattern = '<redirectPort>' + value + '</redirectPort>'
            
            if pattern:
                if self.createTaskXml.find(pattern) < 0:
                    status = False
                    NsmUtil.printStatusHeadLine2('Failed: pattern not found: ' + pattern)
                else:
                    NsmUtil.printStatusHeadLine2('Passed: pattern found: ' + pattern)
                
        NsmUtil.printHeadLine2('END: create response verification: parameters from request body')
        return status
    
    
    def verifyParamemtersExist(self, params, responseXml):
        NsmUtil.printHeadLine2('START: response verification: paramemters exist in response verification')
        #if self.mySubClassName != 'Pod': self.logger.info(responseXml)
        status = True
        for param in params:
            if responseXml.find(param) < 0:
                status = False
                NsmUtil.printStatusHeadLine2('Failed: pattern not found: ' + param)
            else:
                NsmUtil.printStatusHeadLine2('Passed: pattern found: ' + param)
                
        NsmUtil.printHeadLine2('END: response verification: paramemters exist in response verification')
        return status
    
    
        
        