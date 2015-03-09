'''
Created on Jul 15, 2012

@author: huhe
'''

import jarray, os
from java.security import Security
from java.io import DataOutputStream
from java.io import ByteArrayOutputStream
from java.net import URL
from javax.net.ssl import HttpsURLConnection;

from lib import Util
import MySSLProvider
import MyHostnameVerifier

logger = Util.getLogger(Util.getFileNameWithoutSuffix(__file__))

def doGet(url, credential):
    httpMethod = "GET"
    return doService(httpMethod, url, credential)

def doPost(url, credential, requestBody=None):
    httpMethod = "POST"
    return doService(httpMethod, url, credential, requestBody)

def doService(httpMethod, url, credential, requestBody=None):
    
    Security.addProvider(MySSLProvider())
    Security.setProperty("ssl.TrustManagerFactory.algorithm", "TrustAllCertificates")
    HttpsURLConnection.setDefaultHostnameVerifier(MyHostnameVerifier())
    
    urlObj = URL(url)
    con = urlObj.openConnection()
    con.setRequestProperty("Accept", "application/xml")
    con.setRequestProperty("Content-Type", "application/xml")
    con.setRequestProperty("Authorization", credential)
    con.setDoInput(True);
    
    if httpMethod == 'POST':
        con.setDoOutput(True)
        con.setRequestMethod(httpMethod)
        output = DataOutputStream(con.getOutputStream()); 
        if requestBody:
            output.writeBytes(requestBody); 
        output.close();
        
    responseCode = con.getResponseCode()
    logger.info('response code: ' + str(responseCode))
    responseMessage = con.getResponseMessage()
    logger.info('response message: ' + str(responseMessage))
    contentLength = con.getHeaderField('Content-Length')
    logger.info('content length: ' + str(contentLength))        
    
    stream = None
    if responseCode == 200 or responseCode == 201 or responseCode == 202:
        stream = con.getInputStream()
    elif contentLength:
        stream = con.getErrorStream()
        
    if stream:
        dataString = getStreamData(stream)
        logger.info(httpMethod + ' url: ' + url)
        if not url.endswith('.xsd') and len(dataString) < 4096: 
            xmlStr = Util.prettfyXmlByString(dataString)
            logger.info(httpMethod + ' result: \n\n' + xmlStr)
        else:
            logger.info('response body too big, no print out')
        if responseCode == 200 or responseCode == 201 or responseCode == 202:
            return dataString
        else:
            ''' to mark the case failed if response code is not 200-202 '''
            return None
    else:
        logger.error('')
        logger.error('---------------------------------------------------------------------------------------------------')
        logger.error('-------->>>  Input or Error stream is None, it may be a defect if it is positive test case')
        logger.error('---------------------------------------------------------------------------------------------------')
        logger.error('')
        return None
    
    
def getStreamData(stream):
    baos = ByteArrayOutputStream()
    lenRead = 0
    while lenRead >= 0:
        bytes = jarray.zeros(4096, 'b')
        lenRead = stream.read(bytes, 0, 4096)
        if lenRead > 0:
            baos.write(bytes, 0, lenRead)
    stream.close();  
    return baos.toString()

