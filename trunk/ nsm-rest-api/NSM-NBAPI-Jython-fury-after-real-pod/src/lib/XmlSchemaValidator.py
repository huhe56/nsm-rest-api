'''
Created on Aug 8, 2012

@author: huhe
'''
import sys, traceback

from javax.xml.parsers import DocumentBuilderFactory
from javax.xml.parsers import DocumentBuilder
from org.xml.sax import InputSource
from org.xml.sax import SAXException
from java.io import StringReader, FileReader
from javax.xml import XMLConstants
from javax.xml.transform.stream import StreamSource
from javax.xml.transform.dom import DOMSource
from javax.xml.validation import Validator
from javax.xml.validation import SchemaFactory
    
from lib import Util


def validateByFile(xsdFilePaths, xmlFilePath):
    xsdStreamSources = []
    for xsdFilePath in xsdFilePaths:
        xsdStreamSource = StreamSource(FileReader(xsdFilePath))
        xsdStreamSources.append(xsdStreamSource)
    xmlStreamSource = StreamSource(StringReader(Util.readFile(xmlFilePath)))
    return validate(xsdStreamSources, xmlStreamSource)
    

def validate(xsdStreamSources, xmlStreamSource):
    # create a SchemaFactory capable of understanding WXS schemas
    factory = SchemaFactory.newInstance(XMLConstants.W3C_XML_SCHEMA_NS_URI);
    # load a WXS schema, represented by a Schema instance
    schema = factory.newSchema(xsdStreamSources);
    # create a Validator instance, which can be used to validate an instance document
    validator = schema.newValidator()
    # validate the DOM tree
    try:
        validator.validate(xmlStreamSource)
        print '------- PASSED -------'
        return True
    except SAXException:
        # instance document is invalid!
        print '------- FAILED -------'
        print('!!!!!!!!!!!!! something is wrong !!!!!!!!!!!!!')
        errorType = sys.exc_info()[0]
        errorValue = sys.exc_info()[1]
        errorTraceBack = traceback.extract_tb(sys.exc_info()[2])
        print('Error Type: ' + str(errorType))
        print('Error Value: ' + str(errorValue))
        print('Traceback: ')
        for oneStack in errorTraceBack:
            print(oneStack)
        return False
    
    
        