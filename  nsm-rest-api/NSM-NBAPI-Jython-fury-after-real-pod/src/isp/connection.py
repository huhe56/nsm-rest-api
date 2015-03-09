'''
Created on Jul 15, 2012

@author: huhe
'''

from lib import Util
from isp.element import Element
from isp.nsmUtil import NsmUtil


class Connection(Element):
    
    def verifyCreate(self):
        NsmUtil.printHeadLine2('START: create response verification')
                
        Element.verifyCreate(self)
                
        vrfDeviceName1 = 'l3.aggregation.switch.1.mgmt.addr'
        vrfDeviceName2 = 'l3.aggregation.switch.2.mgmt.addr'
        vrfDeviceIP1 = self.pod.getParameterStringValueByName(vrfDeviceName1)
        vrfDeviceIP2 = self.pod.getParameterStringValueByName(vrfDeviceName2)
        param1 = '<vrfDevice><ipv4>' + vrfDeviceIP1 + '</ipv4></vrfDevice>'
        param2 = '<vrfDevice><ipv4>' + vrfDeviceIP2 + '</ipv4></vrfDevice>'
        param3 = '<routingDevice><ipv4>' + vrfDeviceIP1 + '</ipv4>'
        param4 = '<routingDevice><ipv4>' + vrfDeviceIP2 + '</ipv4>'

        params = [param1, param2, param3, param4]
        status = Element.verifyParamemtersExist(self, params, self.createTaskXml)
        
        NsmUtil.printHeadLine2('END: create response verification')
        
        if status: 
            return True
        else:
            return False
        
        
        
    def verifyUpdate(self, updateVerificationPatternList, storage):
        NsmUtil.printHeadLine2('START: update response verification')
                
        Element.verifyUpdate(self, updateVerificationPatternList, storage)
                
        vrfDeviceName1 = 'l3.aggregation.switch.1.mgmt.addr'
        vrfDeviceName2 = 'l3.aggregation.switch.2.mgmt.addr'
        vrfDeviceIP1 = self.pod.getParameterStringValueByName(vrfDeviceName1)
        vrfDeviceIP2 = self.pod.getParameterStringValueByName(vrfDeviceName2)
        param1 = '<vrfDevice><ipv4>' + vrfDeviceIP1 + '</ipv4></vrfDevice>'
        param2 = '<vrfDevice><ipv4>' + vrfDeviceIP2 + '</ipv4></vrfDevice>'
        param3 = '<routingDevice><ipv4>' + vrfDeviceIP1 + '</ipv4>'
        param4 = '<routingDevice><ipv4>' + vrfDeviceIP2 + '</ipv4>'

        params = [param1, param2, param3, param4]
        status = Element.verifyParamemtersExist(self, params, self.updateTaskXml)
        
        NsmUtil.printHeadLine2('END: update response verification')
        
        if status: 
            return True
        else:
            return False
    
