'''
Created on Jul 20, 2015

@author: hassan
'''
from random import randint
#from constraint import Constraint

class Selection():
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
     
    def readevent(self, eventId, filename):
        
        eventFile=open("input/"+filename, 'r')
        for line in eventFile.readlines():
            if line.startswith (str(eventId)): 
                e = line.rstrip('\r\n').split(' ')            
                break
        #event["event1"] = e
        eventFile.close() 
        return e     
     
    def numberOfEvent(self,filename):
        eventfile = open("input/"+filename)
        num = sum(1 for line in eventfile if line.rstrip())   
        eventfile.close()
        return num
    
    def returneventid(self,linenumber, filename):
        cnt = 0
        eventfile = open("input/"+filename)
        for line in eventfile.readlines():
            cnt = cnt + 1
            if cnt == linenumber: 
                break
        e = line.rstrip('\r\n').split(' ')
        return e[0]   # event index in original file
            
        
   
                
        
            
         
        
if __name__ == '__main__':
    select = Selection()
        
    print select.numberOfEvent()
    