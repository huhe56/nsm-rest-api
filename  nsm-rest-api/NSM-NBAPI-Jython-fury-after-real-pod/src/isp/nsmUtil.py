'''
Created on Aug 3, 2012

@author: huhe
'''

import sys, csv, os, traceback, re
from time import gmtime, strftime
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom
from lib import Util, HttpUtil
from isp import Define, XPath
import ipaddr


class NsmUtil(object):
    '''
    classdocs
    '''
    __logger = Util.getLogger(Util.getFileNameWithoutSuffix(__file__))

    def __init__(self):
        '''
        Constructor
        '''
    
    
    @staticmethod
    def isPerfClass(className):
        if className in ['NsmV1', 'Top', 'Provider', 'Tenant']:
            return False
        elif className.startswith('Pod'):
            return False
        else:
            return True
        
        
    @staticmethod
    def getStressObjectName(name, className):
        if className in ['NsmV1', 'Top', 'Provider']:
            return name
        elif className.startswith('Pod'):
            name += ' pod' + str(Define._PodIndex)
            return name
        else:
            name += ' pod' + str(Define._PodIndex) + ' tenant' + str(Define._TenantIndex)
            return name
        
        
    @staticmethod
    def getStressObjectName1(name, className):
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
        
        
    @staticmethod
    def testVlanRange(vlanTested, vlanStart, vlanEnd):
        if int(vlanStart) <= int(vlanTested) <= int(vlanEnd):
            NsmUtil.printStatusHeadLine2('Passed: ' + vlanTested + ' is in vlan range (' + vlanStart + ', ' + vlanEnd + ')')
            return True
        else:
            NsmUtil.printStatusHeadLine2('Failed: ' + vlanTested + ' is not in vlan range (' + vlanStart + ', ' + vlanEnd + ')')
            return False
       
       
    @staticmethod 
    def testIpRange(ipTestedStr, ipRangeStr):
        ipTested = None
        if ipTestedStr.find('/') > 0:
            ipTested = ipaddr.ip_network(ipTestedStr)
        else:
            ipTested = ipaddr.ip_address(ipTestedStr)
            
        ipRange  = ipaddr.ip_network(ipRangeStr)
        
        if ipTested in ipRange:
            NsmUtil.printStatusHeadLine2('Passed: ' + ipTestedStr + ' is in ' + ipRangeStr)
            return True
        else:
            NsmUtil.printStatusHeadLine2('Failed: ' + ipTestedStr + ' is not in ' + ipRangeStr)
            return False
        
        
    @staticmethod
    def getTaskResponseProperty(responseXml, propertyName, propertyType):
        xpath = XPath._TaskResponseProperty
        xpath = xpath.replace('${property-name}', propertyName)
        xpath = xpath.replace('${property-type}', propertyType)
        propertyValue = Util.getXpathValue(responseXml, xpath)
        return propertyValue
    
    
    @staticmethod
    def getStackTrace():
        NsmUtil.__logger.error('!!!!!!!!!!!!! something is wrong !!!!!!!!!!!!!')
        errorType = sys.exc_info()[0]
        errorValue = sys.exc_info()[1]
        errorTraceBack = traceback.extract_tb(sys.exc_info()[2])
        NsmUtil.__logger.error('Error Type: ' + str(errorType))
        NsmUtil.__logger.error('Error Value: ' + str(errorValue))
        NsmUtil.__logger.error('Traceback: ')
        for oneStack in errorTraceBack:
            NsmUtil.__logger.error(oneStack)
            
    
    @staticmethod
    def getCurrentTimeString():
        timeStr = strftime("%Y%m%d-%H%M%S")
        return timeStr
        
        
    @staticmethod
    def moveLogResponse():
        pathNewTmp = Define._PathTmp + '/' + NsmUtil.getCurrentTimeString()
        os.mkdir(pathNewTmp)
        pathNewLog = pathNewTmp + '/log'
        pathNewResponse = pathNewTmp + '/response'
        if os.path.exists(Define._PathLog): os.rename(Define._PathLog, pathNewLog)
        if os.path.exists(Define._PathResponse): os.rename(Define._PathResponse, pathNewResponse)
        #shutil.rmtree(Define._PathLog)
        #shutil.rmtree(Define._PathResponse)
        
    
    @staticmethod 
    def mkPresetDir():
        Util.mkdir(Define._PathResponseCreateDefault)
        Util.mkdir(Define._PathResponseCreateSetup)
        Util.mkdir(Define._PathResponseUpdate)
        Util.mkdir(Define._PathResponseDelete)
        Util.mkdir(Define._PathLog)
        
        
    @staticmethod
    def saveUid(uidList):
        line = ''
        NsmUtil.__logger.debug('')
        for pair in uidList:
            objectUid   = pair[0]
            objectClass = pair[1]
            objectName  = pair[2]
            NsmUtil.__logger.debug('uid: ' + objectUid + ' ------> ' + objectClass + ' [' + objectName + ']')
            line += objectUid + ';' + objectClass + ';' + objectName + "\n"
        Util.writeFile(Define._PathUidDefault, line)
        NsmUtil.__logger.debug('')
        
        
    @staticmethod
    def getUid(uidList, name):
        for pair in uidList:
            objectUid   = pair[0]
            objectName  = pair[2]
            if name == objectName: return objectUid
        return None
            
            
    @staticmethod
    def getMetaProperties(testCaseFilePath):
        data = {}
        lines = csv.reader(open(testCaseFilePath, 'rU'))
        currentClassName = None
        currentObjectName = None
        for items in lines:
            if items[0] == 'class' or items[0] == '#': continue
            joinStr = ''.join(items)
            if joinStr != '':
                if items[0] != '' and items[1] != '':
                    currentClassName = items[0]
                    currentClassName = currentClassName.replace(' ', '')
                    currentObjectName = items[1]
                    #print '---------> ' + currentClassName + ': ' + currentObjectName
                    if not currentClassName in data.keys(): data[currentClassName] = {}
                    if not currentObjectName in data[currentClassName].keys(): data[currentClassName][currentObjectName] = []
                else:
                    if not currentClassName or not currentObjectName:
                        NsmUtil.__logger.error('current class name or object name can not be None')
                        sys.exit()
                    else:
                        if items[4].strip() and items[4] != 'none': 
                            if items[3] == 'string' or items[3] == 'integer':
                                if items[4].find('=') < 0: items[4] = items[3] + '=' + items[4]
                            data[currentClassName][currentObjectName].append(items[2:])
        return data
    
    
    @staticmethod
    def createRequestBodyProperty(className, objectName, objectDescription=None, metaPropertiesList=None, storage=None):
        
        updateVerificationPatternList = []
        
        xmlHeadLine = '<?xml version="1.0" encoding="UTF-8"?>'
        topAttributeMap = {
            'xmlns': 'http://www.cisco.com/NetworkServicesManager/1.1', 
            'xmlns:ns2': 'http://www.w3.org/2005/Atom'
        }
        className = className[0].lower() + className[1:]
        #NsmUtil.__logger.debug(metaPropertiesList)
        #NsmUtil.__logger.debug('class name: ' + className)
        if className.endswith('Zone'): className = 'zone'
        elif className.endswith('AccessVlan'): className = 'networkSegment'
        elif className.endswith('Connection'): className = 'externalNetworkConnection'
        elif className.endswith('Service'): className = 'servicePolicy'
        
        tagTop = Element(className, topAttributeMap)
        
        ### name can't be None
        if not objectName: 
            NsmUtil.__logger.error('Name can not be None')
            return None
        
        tagName = SubElement(tagTop, 'name')
        tagName.text = objectName
        updateVerificationPatternList.append('<name>' + objectName + '</name>')
        
        if objectDescription:
            tagDescription = SubElement(tagTop, 'description')
            tagDescription.text = objectDescription
            updateVerificationPatternList.append('<description>' + objectDescription + '</description>')
        
        tagProperties = SubElement(tagTop, 'properties')
        if metaPropertiesList and storage: 
            for metaProperties in metaPropertiesList:
                tagProperty = SubElement(tagProperties, 'property')
                
                tagName = SubElement(tagProperty, 'name')
                tagName.text = metaProperties[0]
                updateVerificationPatternList.append('<name>' + tagName.text + '</name>')
                
                tagType = SubElement(tagProperty, 'type')
                tagType.text = metaProperties[1]
                updateVerificationPatternList.append('<type>' + tagType.text + '</type>')
                
                grandParentTag = tagProperties
                parentTag = tagProperty
                for oneItem in metaProperties[2:]:
                    #NsmUtil.__logger.debug('oneItem: ' + oneItem)
                    if not oneItem:
                        continue
                    elif oneItem == '<up>':
                        parentTag = grandParentTag
                        # after <up>, no way to find the grandParentTag
                    elif oneItem.find('=') > 0:
                        subItems = oneItem.split('=')
                        tag = subItems[0]
                        text = subItems[1]
                        if tag == 'uid' and text.find('{') == 0:
                            text = text.replace('{', '')
                            text = text.replace('}', '')
                            text = NsmUtil.getUid(storage['_uidList'], text)
                            thisTag = SubElement(parentTag, tag)
                            thisTag.text = text
                            updateVerificationPatternList.append('<' + tag + '>' + text + '</' + tag + '>')
                        elif tag.endswith('ipv4Start'):
                            ipv4AddressList = None
                            if text == '{InternetEdgeZoneLayer3VlanReservedIpAddress}':
                                ipv4AddressList = storage['_internetEdgeZoneLayer3VlanReservedIpAddressList']
                            elif text == '{SecuredInternetEdgeZoneLayer3VlanReservedIpAddress}':
                                ipv4AddressList = storage['_securedInternetEdgeZoneLayer3VlanReservedIpAddressList']
                            text = ipv4AddressList.pop()
                            thisStartTag = SubElement(parentTag, tag)
                            thisStartTag.text = text
                            updateVerificationPatternList.append('<' + tag + '>' + text + '</' + tag + '>')
                            thisEndTag = SubElement(parentTag, 'ipv4End')
                            thisEndTag.text = text
                            updateVerificationPatternList.append('<' + tag + '>' + text + '</' + tag + '>')
                        else:
                            thisTag = SubElement(parentTag, tag)
                            thisTag.text = text
                            updateVerificationPatternList.append('<' + tag + '>' + text + '</' + tag + '>')
                    else:
                        thisTag = SubElement(parentTag, oneItem)
                        grandParentTag = parentTag
                        parentTag = thisTag
        
        #print tostring(tagTop)
        xmlStr = Util.prettifyXmlByElement(tagTop)
        NsmUtil.__logger.info('update request body: \n\n' + xmlStr)
        return xmlHeadLine + tostring(tagTop), updateVerificationPatternList
        
        
    
    
        
    @staticmethod
    def getRequest(getUrl):   
        NsmUtil.__logger.info('get request url: ' + getUrl)
        getResponseXml = HttpUtil.doGet(getUrl, Define._credential)
        return getResponseXml
        
    
    @staticmethod
    def getIpAddress(xmlStr):
        ipAddressPairList = []
        dom = minidom.parseString(xmlStr)
        ipv4RangeList = dom.getElementsByTagName('ipv4AddressRange')
        for ipv4Range in ipv4RangeList:
            ipv4StartElement = ipv4Range.getElementsByTagName('ipv4Start')[0]
            ipv4EndElement   = ipv4Range.getElementsByTagName('ipv4End')[0]
            ipv4Start = NsmUtil.getText(ipv4StartElement)
            ipv4End =NsmUtil.getText(ipv4EndElement)
            ipAddressPairList.append([ipv4Start, ipv4End])
        return ipAddressPairList
    
    
    @staticmethod 
    def getText(node):
        nodeList = node.childNodes
        node = nodeList[0]
        return node.data
    
    
    @staticmethod 
    def getIpAddressListByPairList(ipAddressPairList, count):
        
        index = 0
        returnIpAddressList = []
        for onePair in ipAddressPairList:
            ipv4Start = onePair[0]
            ipv4End = onePair[1]
            ipv4StartNumber = Util.dottedQuadToNum(ipv4Start)
            ipv4EndNumber = Util.dottedQuadToNum(ipv4End)
            for oneIpNumber in range(ipv4StartNumber, ipv4EndNumber+1):
                returnIpAddressList.append(Util.numToDottedQuad(oneIpNumber))
                index += 1
                if index == count: return returnIpAddressList
        return None
    
    
    @staticmethod 
    def getIpAddressListByReservation(xmlString, count):
        ipAddressPairList = NsmUtil.getIpAddress(xmlString)
        return NsmUtil.getIpAddressListByPairList(ipAddressPairList, count)
        

    @staticmethod 
    def saveResult(resultList):
        index = 0
        passedTotal = 0
        failedTotal = 0
        skippedTotal = 0
        line = ''
        lineHtml = '<table border="0" cellspacing="0" cellpadding="2" style="font-size:14px">'
        lineHtml += '<tr><th align="left" width="210">API</th><th align="left" width="100">CRUD</th><th align="left" width="100">Result</th></tr>'
        NsmUtil.__logger.info('')
        for oneResult in resultList:
            index += 1
            oneLine = ' - '.join(oneResult)
            NsmUtil.__logger.info(str(index) + ' - ' + oneLine)
            line += oneLine + "\n"
            
            resultHtml = None
            if oneResult[-1] == 'True': 
                passedTotal += 1
                resultHtml = '<font color="green">Passed</font>'
            elif oneResult[-1] == 'skipped': 
                skippedTotal += 1
                resultHtml = '<font color="red">Failed</font>'
            elif oneResult[-1] == 'False': 
                failedTotal += 1
                resultHtml = 'Skipped'
            
            lineHtml += '<tr>'
            lineHtml += '<td>' + oneResult[0] + '</td><td>' + oneResult[2] + '</td><td>' + resultHtml + '</td>'
            lineHtml += '</tr>'
            
            
        Util.writeFile(Define._PathResultDefault, line)
        NsmUtil.__logger.info('')
        NsmUtil.printHeadLine2(str(passedTotal) + ' test cases passed, ' + str(failedTotal) + ' test cases failed, ' + str(skippedTotal) + ' test cases skipped')
        
        lineHtml += '</table>'
        Util.writeFile(Define._PathResultDefault+'.html', lineHtml)
        
    @staticmethod
    def printHeadLine1(headLine):
        NsmUtil.__logger.info('')
        NsmUtil.__logger.info('')
        NsmUtil.__logger.info('================================ $$$$$$$$$ ' + headLine + " $$$$$$$$$$ ================================")
        NsmUtil.__logger.info('')
        NsmUtil.__logger.info('')
        
    
    @staticmethod    
    def printHeadLine2(headLine):
        NsmUtil.__logger.info('')
        NsmUtil.__logger.info('')
        NsmUtil.__logger.info('---------------- ' + headLine + " -----------------")
        NsmUtil.__logger.info('')
        NsmUtil.__logger.info('')
        
    
    @staticmethod    
    def printStatusHeadLine(headLine):
        NsmUtil.__logger.info('')
        NsmUtil.__logger.info('')
        NsmUtil.__logger.info('-------------->>>>>>>>>>>>> ' + headLine)
        NsmUtil.__logger.info('')
        NsmUtil.__logger.info('')
        
    @staticmethod
    def printStatusHeadLine2(headLine):
        NsmUtil.__logger.info('-------------->>> ' + headLine)
        
    
    @staticmethod    
    def printResult(result, category):
        if (category == 'positive' and result) or (category == 'negative' and not result):
            NsmUtil.printStatusHeadLine(category + ' test result: PASSED')
            return True
        else:
            NsmUtil.printStatusHeadLine(category + ' test result: FAILED')
            return False
            
        
        