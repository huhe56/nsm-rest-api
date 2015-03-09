'''
Created on Sep 6, 2012

@author: huhe
'''

from javax.xml.transform.stream import StreamSource
from java.io import FileReader

from lib import Util, HttpUtil
from lib import XmlSchemaValidator
from isp import Define
from isp.nsmUtil import NsmUtil



if __name__ == '__main__':
    
    #skippedXml = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><serviceOfferings xmlns="http://www.cisco.com/NetworkServicesManager/1.1" xmlns:ns2="http://www.w3.org/2005/Atom"/>'
    
    if False:
        xsdString1 = HttpUtil.doGet(Define._UrlSchemaNSM, Define._credential)
        Util.writeFile(Define._PathSchemaNsm, xsdString1)
        xsdString2 = HttpUtil.doGet(Define._UrlSchemaAtom, Define._credential)
        Util.writeFile(Define._PathSchemaAtom, xsdString2)
        xsdString3 = HttpUtil.doGet(Define._UrlSchemaNameSpace, Define._credential)
        Util.writeFile(Define._PathSchemaNameSpace, xsdString3)
    
    xdsFilePaths = [Define._PathSchemaNsm, Define._PathSchemaAtom, Define._PathSchemaNameSpace]
    
    files = Util.getAllFiles(Define._PathResponse, '*.xml')
    for file in files:
        print '\n'
        print file
        xmlString = Util.readFile(file)
        XmlSchemaValidator.validateByFile(xdsFilePaths, file)
        
        
        