'''
Created on Jul 30, 2015

@author: hassan
'''

from constraint import Constraint
from attrPresentation import AttributeCoding

class Propagation(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''

    def propagate(self):
       
        cons = Constraint()
        cons.load_constraint()
        listofoperand = []
        listofconst = []
        attribute = AttributeCoding()
        num = 0;
        
                    
        #get the list of unary constraints affects on the target event(main seed) for grouping 
        for i in range(int (cons.lengthOfTargetPattern)):
            eventFile=open('input/events.txt', 'r')
            listofoperand.append("event"+str(i+1))   
            #listofoperand.append("group"+str(i+1))       
            for c in cons.constraints:
                const = cons.constraints[c]
                if const["type"] == "unary" and listofoperand[i] == const['operand1']:
                    listofconst.append(c)
            group = open("input/"+ listofoperand[i]+".txt", 'w') 
            num = num + 1;
            #localid = 1 # assign a new id to event in new file  
            for c in listofconst:
                const = cons.constraints[c]
                if const['operator'] == "==":
                    for line in eventFile.readlines():
                        e = line.rstrip('\r\n').split(' ') #convert to a list, otherwise "in" cannot find exact substring for value
                        if const['value'] in e:                            
                            group.write(line)
                            #group.write(str(localid)+" "+line)
                            #localid = localid + 1
                           
                #... develop for other operators 
                if const['operator'] == "<=" or const['operator'] == "<":
                    value = attribute.mapping_atter_value(const['attr'], line)
                    if value == const['value']:
                        group.write(line)
                        #group.write(str(localid)+" "+line)
                        #localid = localid + 1
                         
                if const['operator'] == ">=" or const['operator'] == ">":
                    value = attribute.mapping_atter_value(const['attr'], line)
                    if value == const['value']:
                        group.write(line)
                        # group.write(str(localid)+" "+line) 
                        # localid = localid + 1                        
                             
            
            listofconst = []               
            group.close() 
            eventFile.close() 
        return num    
  
 
if __name__ == '__main__':
   
    p = Propagation()
    p.propagate()   
    