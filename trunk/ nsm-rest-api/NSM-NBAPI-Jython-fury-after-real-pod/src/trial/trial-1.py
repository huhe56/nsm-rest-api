'''
Created on Aug 10, 2012

@author: huhe
'''


from lib import HttpUtil, Util
from isp import Define, XPath
from isp.nsmUtil import NsmUtil
from pprint import pprint
from isp.responseVerification import ResponseVerification

import subprocess
import simplexml


if __name__ == '__main__':
    #xsdString = HttpUtil.doGet(Define._UrlHostPortEngineSchema, Define._credential)
    #print xsdString
    
    #updateTestCaseFilePath = Define._PathTestCase + '/update-all-meta-properties.csv'
    #data = NsmUtil.getMetaProperties(updateTestCaseFilePath)
    #pprint(data)
    
    '''
    xmlFilePath =  '/Users/huhe/Install/workspace/NSM-NBAPI-Jython/response/create/response-create-default/My-Default-IP-Address-of-Infrastructure-Reservation-Range-reservations-111.xml'
    ipaddr = NsmUtil.getIpAddress(xmlFilePath)
    print ipaddr
    print
    
    
    ipAddressList = NsmUtil.getIpAddressListByReservation(xmlFilePath, 5)
    
    print ipAddressList
    '''
    
    '''
    str = NsmUtil.getCurrentTimeString()
    print str
    NsmUtil.moveLogResponse()
    '''
    '''
    filePath1 = '/Users/huhe/Install/workspace/NSM-NBAPI-Jython/response/create/response-create-default/My-Default-Provider-create-001.xml'
    filePath2 = '/Users/huhe/Install/workspace/NSM-NBAPI-Jython/response-golden-data/create/response-create-default/My-Default-Provider-create-001.xml'
    #ResponseVerification.verifyCreate(filePath1, filePath2)
    ResponseVerification.formalize(Util.readFile(filePath2))
    '''
    
    '''
    perl = '/usr/local/ActivePerl-5.16/bin/perl'
    
    dirNSMPerl = '/Users/huhe/Install/workspace/NSM-NBAPI-Perl'
    dirDeviceVerification = dirNSMPerl + '/device-verification'
    
    cmdPerlNSM = dirDeviceVerification + '/NSM.pl'
    cmdPerlParse = dirDeviceVerification + '/Parse.pl'
    cmdPerlProcess = dirDeviceVerification + '/Process.pl'
    
    p = subprocess.Popen(perl + ' ' + cmdPerlProcess, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p.stdout.readlines():
        print line
    retval = p.wait()
    '''
    
    person = {'person':{'name':'joaquim','age':15,'cars':[{'id':1},{'id':2}]}}
    print simplexml.dumps(person)
    
    person = simplexml.loads('<?xml version="1.0" ?><person><cars><car><id>1</id></car><car><id>2</id></car></cars><age>15</age><name>joaquim</name></person>')
    print person['person']['name']


    