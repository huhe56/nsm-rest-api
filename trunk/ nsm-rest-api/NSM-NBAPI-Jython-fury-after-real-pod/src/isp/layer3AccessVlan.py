'''
Created on Jul 15, 2012

@author: huhe
'''

import ipaddr
from lib import Util
from isp import XPath, Define
from nsmUtil import NsmUtil
from isp.element import Element


class Layer3AccessVlan(Element):
    
    def verifyCreate(self):
        NsmUtil.printHeadLine2('START: create response verification')
        
        status1 = Element.verifyCreate(self)
        
        propertyVlan    = NsmUtil.getTaskResponseProperty(self.createTaskXml, 'vlan-id', 'integer')
        propertySubnet  = NsmUtil.getTaskResponseProperty(self.createTaskXml, 'subnet', 'string')
        propertyGateway = NsmUtil.getTaskResponseProperty(self.createTaskXml, 'gateway-address', 'ipv4')
        
        
        vcIpv4 = '<vc><ipv4>' + Define._VCenterIP + '</ipv4></vc>'
        dvsUuid = '<uuid>' + Define._DvsUuid + '</uuid>'
        portGroupName = '<portGroup><name>' + propertyVlan + '</name></portGroup>' 
        params = [vcIpv4, dvsUuid, portGroupName]
        status2 = Element.verifyParamemtersExist(self, params, self.createTaskXml)
        
        
        vlanStart, vlanEnd = self.pod.getVlanRange()
        status3 = NsmUtil.testVlanRange(propertyVlan, vlanStart, vlanEnd)
        
        ipSubnet = None
        if self.mySubClassName == 'Layer3ExternalAccessVlan':
            ipSubnet = Define._GlobalIPSubnet
        elif self.mySubClassName == 'Layer3PrivateAccessVlan':
            ipSubnet = Define._PrivateIPSubnet
        
        status4 = NsmUtil.testIpRange(propertySubnet, ipSubnet)
        
        status5 = NsmUtil.testIpRange(propertyGateway, propertySubnet)
        
        NsmUtil.printHeadLine2('END: create response verification')
        
        if status1 and status2 and status3 and status4 and status5: 
            return True
        else:
            return False
    

    def verifyUpdate(self, updateVerificationPatternList, storage):
        NsmUtil.printHeadLine2('START: update response verification')
        
        status1 = Element.verifyUpdate(self, updateVerificationPatternList, storage)
        
        propertyVlan    = NsmUtil.getTaskResponseProperty(self.updateTaskXml, 'vlan-id', 'integer')
        propertySubnet  = NsmUtil.getTaskResponseProperty(self.updateTaskXml, 'subnet', 'string')
        propertyGateway = NsmUtil.getTaskResponseProperty(self.updateTaskXml, 'gateway-address', 'ipv4')
        
        
        vcIpv4 = '<vc><ipv4>' + Define._VCenterIP + '</ipv4></vc>'
        dvsUuid = '<uuid>' + Define._DvsUuid + '</uuid>'
        portGroupName = '<portGroup><name>' + propertyVlan + '</name></portGroup>' 
        params = [vcIpv4, dvsUuid, portGroupName]
        status2 = Element.verifyParamemtersExist(self, params, self.updateTaskXml)
        
        
        vlanStart, vlanEnd = self.pod.getVlanRange()
        status3 = NsmUtil.testVlanRange(propertyVlan, vlanStart, vlanEnd)
        
        ipSubnet = None
        if self.mySubClassName == 'Layer3ExternalAccessVlan':
            ipSubnet = Define._GlobalIPSubnet
        elif self.mySubClassName == 'Layer3PrivateAccessVlan':
            ipSubnet = Define._PrivateIPSubnet
        
        status4 = NsmUtil.testIpRange(propertySubnet, ipSubnet)
        
        status5 = NsmUtil.testIpRange(propertyGateway, propertySubnet)
        
        NsmUtil.printHeadLine2('END: update response verification')
        
        if status1 and status2 and status3 and status4 and status5: 
            return True
        else:
            return False