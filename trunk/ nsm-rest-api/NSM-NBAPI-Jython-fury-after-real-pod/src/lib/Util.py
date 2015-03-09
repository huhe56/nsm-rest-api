'''
Created on Jul 15, 2012

@author: huhe
'''

import socket, struct
import logging
import os.path
import fnmatch
import re
import simplejson as json
#from pprint import pprint

from xml.etree import ElementTree
from xml.dom import minidom

from isp import Define

from javax.xml.xpath import XPathFactory
from org.xml.sax import InputSource
from java.io import StringReader


def getJsonData(jsonFilePath):
    json_data = open(jsonFilePath)
    data = json.load(json_data)
    json_data.close()
    #pprint(data)
    return data


def getFileNameWithoutSuffix(filePath):
    baseName = os.path.basename(filePath)
    fileNames = baseName.split('.')
    return fileNames[0]


def getAllFiles(rootPath, fileNameFilter):
    matches = []
    for root, dirnames, filenames in os.walk(rootPath):
        for filename in fnmatch.filter(filenames, fileNameFilter):
            matches.append(os.path.join(root, filename))
    return matches


def prettfyXmlByString(xmlStr):
    xml = minidom.parseString(xmlStr)
    uglyXml = xml.toprettyxml('        ')
    text_re = re.compile('>\n\s+([^<>\s].*?)\n\s+</', re.DOTALL)    
    prettyXml = text_re.sub('>\g<1></', uglyXml)
    return prettyXml


def prettifyXmlByElement(elem):
    rough_string = ElementTree.tostring(elem, encoding='utf-8')
    return prettfyXmlByString(rough_string)


def getLogger(filename):
    logger = logging.getLogger(os.path.basename(filename));
    logger.propagate = False
    if (len(logger.handlers) == 0):
        #formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        mkdir(Define._PathLog)
        loggerHandler2 = logging.FileHandler(Define._PathLogFile)
        loggerHandler2.setFormatter(formatter)
        logger.addHandler(loggerHandler2)
        
        loggerHandler = logging.StreamHandler()
        loggerHandler.setFormatter(formatter)
        logger.addHandler(loggerHandler)
        
        logger.setLevel(logging.DEBUG)
        
    return logger


def readFile(filename):
    fh =  open(filename, 'r')
    content = fh.read()
    fh.close
    return content


def writeFile(filename, content): 
    fh = open(filename, 'w')
    fh.write(content)
    fh.close
    
    
def getXpathValue(xmlStr, xpathPattern):
    #print('xml string: ' + xmlStr)
    #print('xpath pattern: ' + xpathPattern)
    xpathObj = XPathFactory.newInstance().newXPath()
    expression = xpathObj.compile(xpathPattern);
    inputSource = InputSource(StringReader(xmlStr))
    result = expression.evaluate(inputSource)
    return result
    
    
def mkdir(myDir):
    if not os.path.exists(myDir):
        os.makedirs(myDir)
    
    
def dottedQuadToNum(ip):
    "convert decimal dotted quad string to long integer"
    return struct.unpack('L',socket.inet_aton(ip))[0]

def numToDottedQuad(n):
    "convert long int to dotted quad string"
    return socket.inet_ntoa(struct.pack('L',n))
      
def makeMask(n):
    "return a mask of n bits as a long integer"
    return (2L<<n-1)-1

def ipToNetAndHost(ip, maskbits):
    "returns tuple (network, host) dotted-quad addresses given IP and mask size"
    # (by Greg Jorgensen)

    n = dottedQuadToNum(ip)
    m = makeMask(maskbits)

    host = n & m
    net = n - host

    return numToDottedQuad(net), numToDottedQuad(host)
