'''
Created on Sep 25, 2012

@author: huhe
'''

from device.main.mainReset import Reset
    
if __name__ == '__main__':
    
    Reset.copyRunningConfigToTFTPServer()
    Reset.copyRunningConfigToTemp('copy-to-tmp-delete')
    