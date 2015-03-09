'''
Created on Jan 9, 2013

@author: huhe
'''

import re
from datetime import datetime
from time import strftime

if __name__ == '__main__':
    name = 'My Default Tenant Network Container pod0 tenant1'
    output = re.sub(r' pod[0-9]+ tenant[0-9]+', '', name)
    print output
    
   # print strftime("%Y-%m-%d %H:%M:%S", datetime.now())
    
    print datetime.now().strftime("%Y-%m-%d %H:%M:%S")