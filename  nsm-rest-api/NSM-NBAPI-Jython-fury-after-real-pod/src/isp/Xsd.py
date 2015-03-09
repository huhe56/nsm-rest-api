'''
Created on Aug 8, 2012

@author: huhe
'''

from lib import HttpUtil
from isp import Define


xsdUrl = Define._UrlHostPortEngine + '/NetworkServicesManagerAPI/schema/NetworkServicesManager-1.1.0.xsd'
_XsdString = HttpUtil.doGetWoV(xsdUrl, Define._credential)

