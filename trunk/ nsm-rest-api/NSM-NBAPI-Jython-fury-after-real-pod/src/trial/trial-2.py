'''
Created on Aug 10, 2012

@author: huhe
'''


from lib import HttpUtil, Util
from isp import Define, XPath
from isp.nsmUtil import NsmUtil
from pprint import pprint
from isp.responseVerification import ResponseVerification

import simplexml


if __name__ == '__main__':
    
    person = {'person':{'name':'joaquim','age':15,'cars':[{'id':1},{'id':2}]}}
    print simplexml.dumps(person)
    
    person = simplexml.loads('<?xml version="1.0" ?><person><cars><car><id>1</id></car><car><id>2</id></car></cars><age>15</age><name>joaquim</name></person>')
    print person['person']['name']
    print person
    
    filePath = '/Users/huhe/Install/workspace/NSM-NBAPI-Jython/response/create/response-create-default/My-Default-Internet-Edge-Zone-Layer-3-VLAN-create-001.xml'
    result = simplexml.loads(Util.readFile(filePath))
    print result
    
    print result['task']['result']['name']
    
    print result['task']['result']['properties']


    