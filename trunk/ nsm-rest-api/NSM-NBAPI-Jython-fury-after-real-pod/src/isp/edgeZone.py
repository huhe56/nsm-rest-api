'''
Created on Jul 15, 2012

@author: huhe
'''

from lib import Util
from isp.element import Element
from isp.nsmUtil import NsmUtil


class EdgeZone(Element):
    
        
    def verifyCreate(self):
        NsmUtil.printHeadLine2('START: create response verification')
                
        vrfDeviceName1 = 'l3.aggregation.switch.1.mgmt.addr'
        vrfDeviceName2 = 'l3.aggregation.switch.2.mgmt.addr'
        vrfDeviceIP1 = self.pod.getParameterStringValueByName(vrfDeviceName1)
        vrfDeviceIP2 = self.pod.getParameterStringValueByName(vrfDeviceName2)
        param1 = '<ipv4>' + vrfDeviceIP1 + '</ipv4>'
        param2 = '<ipv4>' + vrfDeviceIP2 + '</ipv4>'
        params = [param1, param2]
        status = Element.verifyParamemtersExist(self, params, self.createTaskXml)
        
        NsmUtil.printHeadLine2('END: create response verification')
        
        if status: 
            return True
        else:
            return False
    

    def verifyUpdate(self, updateVerificationPatternList, storage):
        NsmUtil.printHeadLine2('START: update response verification')
                
        vrfDeviceName1 = 'l3.aggregation.switch.1.mgmt.addr'
        vrfDeviceName2 = 'l3.aggregation.switch.2.mgmt.addr'
        vrfDeviceIP1 = self.pod.getParameterStringValueByName(vrfDeviceName1)
        vrfDeviceIP2 = self.pod.getParameterStringValueByName(vrfDeviceName2)
        param1 = '<ipv4>' + vrfDeviceIP1 + '</ipv4>'
        param2 = '<ipv4>' + vrfDeviceIP2 + '</ipv4>'
        params = [param1, param2]
        status = Element.verifyParamemtersExist(self, params, self.updateTaskXml)
        
        NsmUtil.printHeadLine2('END: update response verification')
        
        if status: 
            return True
        else:
            return False