'''
Created on Jul 23, 2015

@author: 
'''


class AttributeCoding(object):
    '''
    classdocs
    '''
    attrName = {}
    attrCode = {}

    def __init__(self):
        '''
        Constructor
        '''
        pass
    
    def load_attr_cvs(self, attr):
        #for key in self.distribution.keys():
            file = "input/" + attr + ".csv"
            with open(file, 'rb') as csvfile:
                for line in csvfile.readlines():
                    item = line.rstrip('\r\n').split(',')
                    self.attrName[item[1]] = item[0]
                    self.attrCode[item[0]] = item[1]
            csvfile.close()    
            
    def mapping_atter_value(self, attr, event):
        for item in event:
            if attr.lower()=='location' and item.startswith("L-"):   #item.find("L-") != -1: 
                return item
            if attr.lower()=='role' and item.startswith("R-"): 
                return item
            if attr.lower()=='user' and item.startswith("U-"): 
                return item
            if attr.lower()=='patient' and item.startswith("P-"): 
                return item
            if attr.lower()=='date' and item.startswith("D-"): 
                return item
            if attr.lower()=='time' and item.startswith("T-"): 
                return item            
            if attr.lower()=='action' and item.startswith("A-"): 
                return item
            if attr.lower()=='resource' and item.startswith("S-"): 
                return item
           
if __name__ == '__main__':
    coding = AttributeCoding()
    coding.load_attr_cvs("user")
    e= ['U-1', 'D-3', 'T-6', 'P-2', 'A-2', 'L-1']
    print coding.mapping_atter_value("location", e)
    
            
                       