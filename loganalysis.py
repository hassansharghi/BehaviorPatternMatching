'''
Created on Aug 2, 2015

@author: hassan
- Analysis the event log to determine the number of different values(domain) for a attribute. 
- Use the result to assign weight to unary constraints

'''
from attrPresentation import AttributeCoding

class LogFileAnalysis(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
    def numberOfValue(self, attr, filename):
        attrCode = AttributeCoding() 
        domain = []
        eventfile = open(filename,"r")
        for line in eventfile.readlines():
            e = line.rstrip('\r\n').split(' ') 
            value = attrCode.mapping_atter_value(attr,e)
            if not(value in domain):
                domain.append(value)
        eventfile.close()
        return len(domain)
        
         
    def userDomainValue(self, numgroup):   
        attrCode = AttributeCoding()      
        domainvalue = [] 
        for i in range(1,numgroup+1):
            eventfile = open("input/event" + str(i) + ".txt","r")
            for line in eventfile.readlines():
                e = line.rstrip('\r\n').split(' ') 
                value = attrCode.mapping_atter_value("user",e)
                if not(value in domainvalue):
                    domainvalue.append(value)
            eventfile.close()
        return domainvalue
    
    # search all groups to find trace of particular user
    def extractUserEvents (self,numgroup, userid):   
        eventnum = 0
        usertrace = open("input/"+ "trace.txt", 'w')
        for i in range(1,numgroup+1):           
            
            eventfile = open("input/event" + str(i) + ".txt","r")
            for line in eventfile.readlines():
                e = line.rstrip('\r\n').split(' ') 
                if userid in e:
                    usertrace.write(line)
                    eventnum += 1
            eventfile.close()
                               
        usertrace.close()
        return eventnum    
                   
            
if __name__ == '__main__':
    L = LogFileAnalysis()
    L.extractUserTrace(3,"U-1")
            