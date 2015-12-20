'''
Created on Jul 21, 2015

@author: hassan

-- Read constraints from JSON file
-- Assign weight to each constraint according to the number different values assigned to the bound variables
-- enforce constraints  

'''
import json
from eventSelection import Selection
from attrPresentation import AttributeCoding
from loganalysis import LogFileAnalysis

class Constraint():
    
    constraints = dict()
    boundVar=[]
    lengthOfTargetPattern = 1  
    
    def __init__(self):
        pass
    
    def load_constraint(self):
        variables = []
        dataFile=open('input/constraints.json')
        data = json.load(dataFile)
        dataFile.close()
                
        for entity in data:            
            if "length" in entity:
                self.lengthOfTargetPattern = entity["length"]
                               
            num=1          
            if "constraint" in entity:
                for value in entity["constraint"]:
                    self.constraints["cons" + str(num)]= value     
                    num = num +1                      
                             
            if "bound_variable" in entity:
                for value in entity["bound_variable"]:
                    variables.append(value)                
                for i in range(0, len(variables)):
                    self.boundVar.append(variables[i]["var"+ str(i+1)])
                    
    def assignweight(self):  
        sel = Selection()
        numberofevents = sel.numberOfEvent("events.txt")
        log = LogFileAnalysis()
        for c in self.constraints:
            const = self.constraints[c]
            if const["type"] == "unary" :
                attrname = const["attr"]
                w = log.numberOfValue(attrname,"input/events.txt")
                if const["effect"] == "hard":
                    #const["weight"] = str(w*numberofevents) #assign a high weight
                    const["weight"] = str(1000000)
                else:
                    const["weight"] = str(w)
                
            # binary constraint type1: define a condition for two different events on same attribute 
            # binary constraint type2: define a condition for one event on two different attributes
            if const["type"] == "binary" : 
                attrname = const["attr"]
                w = log.numberOfValue(attrname,"input/events.txt")
                if const["effect"] == "hard":
                    #const["weight"] = str(w*numberofevents)
                    const["weight"] = str(1000000)
                else:
                    const["weight"] = str(w)
        
                    
class ConstraintEnforcement():
    constraints = {}
    assignment = {}
    variables = []
    satisfied_violated = {}
    
    def __init__(self, cons, ass, var):
        self.constraints = cons
        self.assignment = ass
        self.variables = var
    
    def process(self):
        
        for c in self.constraints:
            const = self.constraints[c]
            if const["type"] == "unary" :
                if self.unaryconstraint(const,c) == -1:
                    return -1   # hard constraint is violated
                                
            elif const["type"] == "binary" :
                if self.binaryconstraint(const,c) == -1:
                    return -1   # hard constraint is violated
                
            else:
                print "constraint.process() --> Error in type of constraint!"
        return 1
    
            
    def unaryconstraint(self,const,constNum):       
        attrCode = AttributeCoding()        
        
        assignValue = attrCode.mapping_atter_value(const['attr'], self.assignment[const['operand1']])
              
        if const['operator'] == "==":
            if  assignValue == const['value']:
                self.satisfied_violated[constNum] = "satisfied" 
            else:
                self.satisfied_violated[constNum] = "violated"
                if const["effect"] == "hard":
                    return -1
                else:
                    return 1
               
        #if const['operator'] == "<=":
        
        #if const['operator'] == ">=":
        
        #if const['operator'] == "!=":
               
     
    def binaryconstraint(self,const,constNum): 
        attrCode = AttributeCoding()                 
        assignValue1 = attrCode.mapping_atter_value(const['attr'], self.assignment[const['operand1']]) 
        assignValue2 = attrCode.mapping_atter_value(const['attr'], self.assignment[const['operand2']])         
        if const['operator'] == "==":
            if assignValue1 == assignValue2:
                self.satisfied_violated[constNum] = "satisfied" 
            else:
                self.satisfied_violated[constNum] = "violated"
                if const["effect"] == "hard":
                    return -1
                else:
                    return 1
                
        if const['operator'] == "!=":
            if assignValue1 != assignValue2:
                self.satisfied_violated[constNum] = "satisfied" 
            else:
                self.satisfied_violated[constNum] = "violated"
                if const["effect"] == "hard":
                    return -1
                else:
                    return 1  
                
        if const['operator'] == "::":     #duration   
            duration = int(const['value'])
            temp = assignValue1.split('-')
            starttime = int(temp[1])
            temp = assignValue2.split('-')
            endtime = int(temp[1])
            if starttime <= endtime:
                if endtime-starttime <= duration: 
                    self.satisfied_violated[constNum] = "satisfied" 
                    # events between first and last event should be checked as well
                    num = len(self.assignment)
                    if num>2: # length of target pattern greater than 2 
                        if self.verify_time_middle_events(num, starttime, endtime) == -1:
                            self.satisfied_violated[constNum] = "violated" 
                    
                    # for example T-23  and T-2 has duration 3. (T-23, T-24, T-1,T-2) 
                else:
                    self.satisfied_violated[constNum] = "violated"
                    if const["effect"] == "hard":
                        return -1
                    else:
                        return 1    
            else:
                if (starttime + duration) % 24 == endtime:
                    self.satisfied_violated[constNum] = "satisfied" 
                else:
                    self.satisfied_violated[constNum] = "violated"
                    if const["effect"] == "hard":
                        return -1
                    else:
                        return 1     
            
          
     # 29/10/2015: should be tested   
    def verify_time_middle_events(self,num, starttime, endtime):
        attrCoding = AttributeCoding() 
        for i in range(2,num): #each event between first and last event should happen between start and end time
            assignValue = attrCoding.mapping_atter_value('time', self.assignment['event' + str(i) ]) 
            temp = assignValue.split('-')
            if int(temp[1]) > endtime and int(temp[1]) < starttime:
                return -1
            
        return 1
        
        
        
                        
        
if __name__ == '__main__':
    cons = Constraint()
    cons.load_constraint()
    cons.assignweight()
    print cons.lengthOfTargetPattern
    print cons.constraints
    sel = Selection()
    enforce = ConstraintEnforcement(cons.constraints, sel.readevent(), cons.boundVar)
    enforce.process()
    
    
    