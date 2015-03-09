'''
Created on Jul 21, 2012

@author: huhe
'''

import simplejson as json
from pprint import pprint
import re

from isp import Define
from lib import Util
from isp.nsmUtil import NsmUtil
from isp.element import Element
from isp.top import Top
from isp.nsmV1 import NsmV1
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


def setup(currentElementObject, data, catalog, uidDictionary):
    logger.debug('\n\n---------------------> setup() is called <------------------------\n')
    logger.debug('current element object: ' + currentElementObject)
    
    childCatalog = None
    if currentElementObject == 'Top':
        
        nsmV1 = NsmV1(None, None, None, None, None)
        nsmV1.createName = 'My Setup NsmV1'
        nsmV1Catalog = nsmV1.getCatalog()
        
        createName = 'My Setup Top'  
        myTop = eval(currentElementObject)(nsmV1Catalog, createName, None, None, None)
        #myTop.setOffLine
        if data:
            for key, value in data.items():
                if key == 'offline' and value == 'true':
                    myTop.setOffLine()
        childCatalog = myTop.getCatalog()
    else:
        uidParam = {}
        currentElementClass = re.sub(r'^[0-9]{2}\-', '', currentElementObject)
        requestBodyFileName = None
        try:
            requestBodyFileName = Define._ElementClassDefaultRequestBodyFileMapping[currentElementClass]
        except:
            logger.info(currentElementClass + ' is not in mapping, it will be retrieved from json setup request.body.file')
        isOffLine = False
        isOnLine = False
        if (data):
            for key, value in data.items():
                if key == 'offline' and value == 'true':
                    isOffLine = True
                elif key == 'online' and value == 'true':
                    isOnLine = True
                elif key == 'request.body.file':
                    requestBodyFileName = value
                elif key == 'uid':
                    for uidKey, uidValue in value.items():
                        try:
                            uidParam[uidKey] = uidDictionary[uidValue]
                        except:
                            print uidDictionary
        
        myObject = eval(currentElementClass)(catalog)
        myObject.setRequestBodyFile(requestBodyFileName)
        
        ### set all objects off-line
        if not Define._SetupGlobalOnLine:
            myObject.setOffLine()
        
        # online over offline
        if isOffLine:
            myObject.setOffLine()
        if isOnLine:
            myObject.setOnLine()
            
        myObject.setRequestBodyParams(uidParam)
        myObject.create()
        myObject.getDetail()
        uidDictionary[myObject.createName] = myObject.uid
        childCatalog = myObject.getCatalog()
                
    if data:
        for childElementClass, childElementData in sorted(data.items()):
            if (childElementClass != 'request.body.file' and childElementClass != 'uid' and childElementClass != 'offline' and childElementClass != 'online'):
                setup(childElementClass, childElementData, childCatalog, uidDictionary)
                

if __name__ == '__main__': 
    
    NsmUtil.mkPresetDir()
    
    jsonFileName = Define._SetupJsonFileName
    
    logger = Util.getLogger(__file__)
    
    Define._PathRequestBodyCreateDefault    = Define._PathRequestBodyCreateSetup
    Define._PathResponseCreateDefault       = Define._PathResponseCreateSetup
    
    Define._PathUidDefault  = Define._PathUidSetup
    
    json_data = open(Define._SetupJsonFileName)
    logger.debug('json setup file name: ' + jsonFileName)
    data = json.load(json_data)
    ### pprint(data)
    json_data.close()

    
    requestBodyParameter = None
    uidDictionary = {}
    setup('Top', data['Top'], requestBodyParameter, uidDictionary)
    
    line = ''
    for objectName, uid in uidDictionary.items():
        line += uid + ';' + objectName + '\n'
    logger.debug('\n\n' + line)
    Util.writeFile(Define._PathUidSetup, line)
    
    print '\n\n================== setup completed ====================\n'
    