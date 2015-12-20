'''
Created on Jul 24, 2015

@author: hassan
'''
#import pickle
import copy
from constraint import Constraint,ConstraintEnforcement
from propagator import Propagation
from eventSelection import Selection
from attrPresentation import AttributeCoding
from loganalysis import LogFileAnalysis
import random

class Cspsolver():
    assignment = {} 
    totalnumberOfEventLog = 0
    #patLength = 1
    
    
    def __init__(self):
        #assignment = dict() 
        pass
       

    def Solver(self): 
        log = LogFileAnalysis()
        select = Selection()
        cons = Constraint()
        group = Propagation()
        numberOfGroup = group.propagate()
        cons.load_constraint()
        cons.assignweight()
        patLength = cons.lengthOfTargetPattern
        
        #find user trace participating in all groups
        # numberOfValue
        userDomain = []
        userDomain = log.userDomainValue(numberOfGroup) #define in loganalysis
        outputfile = open("output/instances.txt", "w")
        
        for key in cons.constraints:
            outputfile.write("%s: type=%s, weight=%s \n "   % (key,cons.constraints[key]["effect"], cons.constraints[key]["weight"] ) )    
        outputfile.write("*******************************************\n")    
            
        
        solutionnum = 1
        # search trace of each user to find pattern
        for r in userDomain: 
            findSolution = False
            self.totalnumberOfEventLog = log.extractUserEvents(numberOfGroup, r)  #create trace.txt for each user
            numberofinitialize = 1
            while numberofinitialize < int(self.totalnumberOfEventLog) / int(patLength): #the number of initialization
                numberofinitialize += 1 
                numtry = 0 #number of try to find a suitable initial solution
                find = False
                while numtry < self.totalnumberOfEventLog * int(patLength):  #initialize a solution without violating hard constraints
                    numtry += 1
                    self.initAssignment(int(patLength))
                    #numberOfEventLog = select.numberOfEvent()
                    maxstep = self.totalnumberOfEventLog #* int(patLength) 
                    enforce = ConstraintEnforcement(cons.constraints, self.assignment, cons.boundVar)
                        
                    if enforce.process() != -1: # otherwise a hard constraint is violated
                        find = True
                        break
                #print enforce.satisfied_violated
                if find == True :
                    cost = self.costFunction(enforce.satisfied_violated, cons.constraints)
                    tempcost = cost 
#                     findSolution = True   
#                     bestAssignment = copy.deepcopy(self.assignment)    #bestAssignment = self.assignment
#                     voilationList = copy.deepcopy(enforce.satisfied_violated) #voilationList = enforce.satisfied_violated
#                     iterateNum = 1
                    
                         
                    #maxstep is the size of trace. to give chance to test more events this step will be increased
                    for step in range(maxstep * int(patLength) ):         
                        if tempcost == 0:
                            break         
                        #find the first violated constraint for initializing selectedConst to use in next for
                        for key, value in enforce.satisfied_violated.iteritems():
                            if value == "violated":
                                selectedConst = key
                                break
                        #find a violated constraint with high weight
                        for key, value in enforce.satisfied_violated.iteritems():
                            if value == "violated" and cons.constraints[selectedConst]["weight"] < cons.constraints[key]["weight"]:
                                selectedConst = key
                        
                        #choose an event from relevant file. The filename was defined based on operand name
                        #filename = cons.constraints[selectedConst]["operand1"] + ".txt"
                        filename = "trace.txt"
                        numberOfEventLog = select.numberOfEvent(filename)  
                                              
                        #find the list of event index in current assignment to prevent duplicating during replacing       
                        eventlist = []
                        for key, value in self.assignment.iteritems():
                            eventlist.append(value[0])
                        #generate a random number to select an event from log file    
                        eventindex = random.randint(1, numberOfEventLog) 
                        #find the event ID of selected event
                        eventid = select.returneventid(eventindex, filename)
                        while eventid in eventlist:
                            eventindex = random.randint(1, numberOfEventLog)
                            eventid = select.returneventid(eventindex, filename) 
                        
                        self.assignment[cons.constraints[selectedConst]["operand1"]] = copy.deepcopy(select.readevent(eventid,filename))
                        if enforce.process() != -1:  #otherwise hard constraint is violated
                            #print enforce.satisfied_violated
                            tempcost = self.costFunction(enforce.satisfied_violated, cons.constraints)
                                                        
                            if tempcost <= cost:                    
                                bestAssignment = copy.deepcopy(self.assignment)    #bestAssignment = self.assignment
                                cost = tempcost
                                voilationList = copy.deepcopy(enforce.satisfied_violated) #voilationList = enforce.satisfied_violated
                                #print cost
                                iterateNum = step
                                findSolution = True
                
                    #print  self.assignment 
                    if findSolution == True:
                        print "solution %d%s" % (solutionnum,":")
                        outputfile.write("solution %d%s \n" % (solutionnum,":"))
                        solutionnum = solutionnum + 1
                        #print bestAssignment 
                        s = sorted(bestAssignment.keys())
                        for key in s:
                            print(key, bestAssignment[key])
                            outputfile.write("%s: %s \n" %(key, bestAssignment[key]))
                        print voilationList # is a dictionary
                        
                        for i in voilationList.keys():            
                            outputfile.write(i + ": " + voilationList[i]  + ", ")
                        outputfile.write("\n")
                        
                        print "cost:%d" % (cost)
                        outputfile.write("cost:%d \n" % (cost))
                        print "Iteration: %d" % (iterateNum)
                        outputfile.write("Iteration: %d \n" % (iterateNum))
                        print "*********************************"
                        outputfile.write("*******************************************\n")
                        findSolution = False
                
        outputfile.close()
        print "end of search!"
                    
                
    def costFunction(self,voilation ,constList):  
        weight = 0
        for key, value in voilation.iteritems():
                if value == "violated" :
                    weight = weight + int (constList[key]["weight"])
                    
        return weight
              
        
    def initAssignment(self, length):   #length: length of pattern
        select = Selection()
        eventindexlist = [] 
        for i in range(0,length):
            n= select.numberOfEvent("trace.txt")
            self.totalnumberOfEventLog = n
            while True:  #prevent from duplicating
                eventindex = random.randint(1,n)
                if not eventindex in eventindexlist:
                    eventindexlist.append(eventindex)
                    break
            eventid = select.returneventid(eventindex, "trace.txt")
            e = select.readevent(eventid, "trace.txt")
            assVar = "event" + str(i+1)
            self.assignment[assVar] = e
            
            #assVar = "event" + str(i+1)
            #n= select.numberOfEvent(assVar+".txt")
            #self.totalnumberOfEventLog = self.totalnumberOfEventLog + n
            
            #eventindex = random.sample(range(1,n), int(length))
            #eventindex = random.randint(1,n)
            #eventid = select.returneventid(eventindex, assVar+".txt")
            #e = select.readevent(eventid, assVar + ".txt")
            #self.assignment[assVar] = e[1:]  #remove the local id 
            #self.assignment[assVar] = e
#         random.randint(1,n)
#         n= select.numberOfEvent()
#         eventindex = random.sample(range(1,n), int(length))
#         for i in range(0,int(length)):
#             assVar = "event" + str(i+1)
#             self.assignment[assVar] = select.readevent(eventindex[i], assVar)
          
        #print self.assignment   


if __name__ == '__main__':
    
    csp = Cspsolver()
    csp.Solver()  