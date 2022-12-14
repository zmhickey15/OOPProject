from builtins import float, range
from sqlite3 import Row
from textwrap import wrap
from multiprocessing.connection import wait
from queue import PriorityQueue, Queue
import queue
import random
import math
import csv 


#random number b/w 0 and 1  
def urand():
  return random.uniform(0,1)

# random num distrbution 
def genxp(lam):
  x=0
  while (x == 0):
    u = urand();
    x = ( -1/ lam )*math.log(u)
  return x

class process():
  compleationTime=0
  startProcess=0
  def __init__(self, STLamda, time, id ):
    self.ServiceTime = genxp(STLamda)
    self.timeRemaining = self.ServiceTime
    self.arrivalTime=time
    self.id=id


class event():
  def __init__(self, type, time, process ):
    self.type = type # type of event 
    self.time = time # time left to finish process
    self.process= process 

  def __lt__(self, other):
    return self.time < other.time

def compareSTRF(one, two):
  if(one.process.ServiceTime < two.process.ServiceTime): return -1
  return 1

def getdepart(one, two):
  if(one.type < two.type): return 1
  return -1

def reorderDepart(self, other):
  return self.time < other.time

def compareHRRN(one, two, ct):
  a= (two.process.ServiceTime + (ct - two.process.arrivalTime) )/ two.process.ServiceTime 
  b= (two.process.ServiceTime + (ct - two.process.arrivalTime) )/ two.process.ServiceTime 
  if (a < b ): return -1
  return 1


def genReport(processes, clockTime, scheduler,lamda,qt,printtype):
  avgTurnAround= 0
  totalThroughPut = 0
  waitTime=0
  cpuUtil = 0
  for p in processes.queue:
    avgTurnAround += (p.compleationTime - p.arrivalTime)
    waitTime += abs(((p.compleationTime - p.arrivalTime) - p.ServiceTime))
    cpuUtil += p.ServiceTime


  waitTime= waitTime / 10000
  avgTurnAround = avgTurnAround / 1000000
  totalThroughPut = 10000 / clockTime
 
  cpuUtil = 1-(( (clockTime/cpuUtil) ) * 100 )# fix cpu utilization 

  if(printtype == 0):
    f = open('data.csv', 'a')
    writer = csv.writer(f)
    row = [scheduler,lamda,avgTurnAround,totalThroughPut,cpuUtil,waitTime,qt]
    writer.writerow(row)
    f.close()
  else:
    
    print('\n \n',scheduler, 'lamda: ', lamda,' quantum used: ', qt)
    print('avg Turn Around: ', avgTurnAround)
    print('total Through put: ', totalThroughPut)
    print('cup Util: ', cpuUtil)
    print('avg number of processes in reddy queue: ', waitTime, '\n \n')


  return

def fcfs(lamService, lamArrival,printtype):    
  # fcfs(at,.04,0)
  readyqueue= Queue()
  eventqueue = PriorityQueue()
  finishedProcesses= Queue()
  processDone=0
  clockTime=0
  id=0
  cpu=0
  # first event 
  event1= event(1, clockTime, process(lamService,clockTime,id))
  id+=1
 
  eventqueue.put(event1)
  while (processDone != 10000):
    curentEvent = eventqueue.get()
    clockTime=curentEvent.time
    if (curentEvent.type==1):
      arivalTime = clockTime+genxp(lamArrival)
      nextEvent= event(1, arivalTime, process(lamService,arivalTime,id))
      eventqueue.put(nextEvent)
      id+=1
      if(cpu==0):
        curentEvent.type=2
        curentEvent.time=curentEvent.process.ServiceTime + clockTime
        eventqueue.put(curentEvent)
      if (cpu==1):
        readyqueue.put(curentEvent)
    elif( curentEvent.type==2 ):
        if(readyqueue.empty()):
          cpu=0
        else:
          depart=readyqueue.get()
          depart.type=2
          depart.time=depart.process.ServiceTime + clockTime
          eventqueue.put(depart)
        processDone += 1
        curentEvent.process.compleationTime=clockTime
        finishedProcesses.put(curentEvent.process)
        #print(processDone)

  genReport(finishedProcesses, clockTime,'fcfs',lamArrival,0,printtype)
  return

def roundRobin(lamService, lamArrival, quantum,printtype):
  readyqueue= Queue()
  eventqueue = PriorityQueue()
  finishedProcesses= Queue()
  processDone=0
  clockTime=0
  id=0
  cpu=0
  # first event 
  event1= event(1, clockTime, process(lamService,clockTime,id))
  id+=1

  eventqueue.put(event1)
  while (processDone != 10000):
    curentEvent = eventqueue.get()
    clockTime=curentEvent.time

    if (curentEvent.type==1): # arrive 
      arivalTime = clockTime+genxp(lamArrival)
      nextEvent= event(1, arivalTime, process(lamService,arivalTime,id))
      eventqueue.put(nextEvent)
      id+=1
      if(cpu==0):
        if( (curentEvent.process.timeRemaining - quantum) > 0): # need more than the quantum 
          curentEvent.type=3                                  # swap
          curentEvent.time=curentEvent.process.timeRemaining + quantum + clockTime
          curentEvent.process.timeRemaining =curentEvent.process.timeRemaining - quantum
          eventqueue.put(curentEvent)
        else:
          curentEvent.type=2
          curentEvent.time=curentEvent.process.timeRemaining + clockTime
          eventqueue.put(curentEvent)
      if (cpu==1):
        readyqueue.put(curentEvent)
    elif( curentEvent.type==2 ): # depart 
        if(readyqueue.empty()):
          cpu=0
        else:
          depart=readyqueue.get()
          if( (depart.process.timeRemaining - quantum) > 0): # need more than the quantum 
            depart.type=3                                  # swap
            depart.time= depart.process.timeRemaining +clockTime+ quantum
            depart.process.timeRemaining =depart.process.timeRemaining - quantum
            eventqueue.put(depart)
          else:
            depart.type=2
            depart.time=depart.process.timeRemaining + clockTime
            eventqueue.put(depart)
        processDone += 1
        curentEvent.process.compleationTime=clockTime        
        finishedProcesses.put(curentEvent.process)

        #print(processDone)
    elif(curentEvent.type == 3):# swap
        readyqueue.put(curentEvent)
        depart=readyqueue.get()
        if( (depart.process.timeRemaining - quantum) > 0): # need more than the quantum 
          depart.type=3                                  # swap
          depart.time=clockTime + quantum
          depart.process.timeRemaining =depart.process.timeRemaining  - quantum
          eventqueue.put(depart)
        else:
          depart.type=2
          depart.time=depart.process.timeRemaining + clockTime
          eventqueue.put(depart)
          
  genReport(finishedProcesses, clockTime, 'rr',lamArrival,quantum,printtype)
  return

def hrrn(lamService,lamArrival,printtype):
  readyqueue= Queue()
  eventqueue = PriorityQueue()
  finishedProcesses= Queue()
  processDone=0
  clockTime=0
  id=0
  cpu=0
  # first event 
  event1= event(1, clockTime, process(lamService,clockTime,id))
  id+=1
  eventqueue.put(event1)
  while (processDone != 10000):
    curentEvent = eventqueue.get()
    clockTime=curentEvent.time
    if (curentEvent.type==1):
      arivalTime = clockTime+genxp(lamArrival)
      nextEvent= event(1, arivalTime, process(lamService,arivalTime,id))
      eventqueue.put(nextEvent)
      id+=1
      if(cpu==0):
        curentEvent.type=2
        curentEvent.time=curentEvent.process.ServiceTime + clockTime
        eventqueue.put(curentEvent)
      if (cpu==1):
        readyqueue.put(curentEvent)
        sorted(readyqueue,  cmp=compareHRRN(clockTime)) #######
    elif( curentEvent.type==2 ):
        if(readyqueue.empty()):
          cpu=0
        else:
          depart=readyqueue.get()
          depart.type=2
          depart.time=depart.process.ServiceTime + clockTime
          eventqueue.put(depart)
        processDone += 1
        curentEvent.process.compleationTime=clockTime
        finishedProcesses.put(curentEvent.process)
        #print(processDone)
  genReport(finishedProcesses, clockTime, 'hrrn',lamArrival,0,printtype)  

def strf(lamService, lamArrival,printtype):
  readyqueue= Queue()
  eventqueue = PriorityQueue()
  finishedProcesses= Queue()
  processDone=0
  clockTime=0
  id=0
  cpu=0
  # first event 
  event1= event(1, clockTime, process(lamService,clockTime,id))
  id+=1
  eventqueue.put(event1)
  while (processDone != 10000):
    curentEvent = eventqueue.get()
    clockTime=curentEvent.time

    if (curentEvent.type==1):
      arivalTime = clockTime+genxp(lamArrival)
      nextEvent= event(1, arivalTime, process(lamService,arivalTime,id))
      eventqueue.put(nextEvent)
      id+=1
      
      if(cpu==0): # cpu not working 
        curentEvent.type=2
        curentEvent.time=curentEvent.process.timeRemaining + clockTime
        curentEvent.process.startProcess= clockTime
        cpu = 1
      if (cpu==1): # cpu working 
        # get depart 
        events=Queue()
        nextDepart = curentEvent
        eventqueue.put(curentEvent) # will this fix it lol  

        #for ev in range(eventqueue.qsize):
        while not readyqueue.empty():
          evt = eventqueue.get()
          if (evt.type==2):
            nextDepart=evt
          else:
            events.put(evt)
        while not events.empty():
          evt =events.get()
          eventqueue.put(evt)
            
          

       
        nextDepart.process.timeRemaining = clockTime -  nextDepart.process.startProcess # how long is left 
        readyqueue.put(nextDepart)
        
        #sorted(readyqueue,  cmp=compareSTRF)### this is a fucking prob 
        depart=readyqueue.get() # set next depart 
        depart.type=2
        depart.time=depart.process.timeRemaining + clockTime
        depart.process.startProcess= clockTime
        # reorder event queeue 
        

    elif( curentEvent.type==2 ):
        if(readyqueue.empty()):
          cpu=0
        else:
          depart=readyqueue.get()
          depart.type=2
          depart.time=depart.process.timeRemaining + clockTime
          depart.process.startProcess= clockTime
          eventqueue.put(depart)
          
        processDone += 1
        curentEvent.process.compleationTime=clockTime
        finishedProcesses.put(curentEvent.process)
        #print(processDone)
  genReport(finishedProcesses, clockTime, 'strf',lamArrival,0,printtype)

  return


def main():
  
  done = False
  while (not done):
    todo= input( '\nto create file with data for simulations press: 1 \nto run a custom simulation press: 2 \nto end program enter 3\n \nenter Value:' )
    todo =int(todo)

    if(todo == 1):
      filename = "data.csv"
      f = open(filename, "w+")
      f.close()
      f = open('data.csv', 'a')
      writer = csv.writer(f)
      row = ['scheduler','lamda','avgTurnAround','totalThroughPut','cpuUtil','waitTime','qt']
      writer.writerow(row)
      f.close()
      for at in range(10,31):
        fcfs(.04,at,0)
        print('fcfs:', at)
      for at in range(10,31):
        hrrn(.04,at,0)
        print('hrrn:', at)
      for at in range(10,31):
        strf(.04,at,0)
        print('strf:', at)
      for at in range(10,31):
        print('rrStart .01', at,)
        roundRobin(.04,at,.01,0)
        print('rrFinish .01', at,)
      for at in range(10,31):
        print('rrStart .2', at,)
        roundRobin(.04,at,.2,0)
        print('rrFinish .2', at,)

    elif(todo == 2):
      schul = input('for FCFS enter: 1 \nfor RR enter: 2 \nfor STRF enter: 3 \nfor HRRN enter 4\n\nenter Value:' )
      schul =int(schul)
      if(schul == 1):
        at = input('enter avg arrival time ')
        st = input('enter searvice time ')
        at = float (at)
        st= float(st)
        fcfs(st,at,1)

      elif(schul == 2):
        at = input('enter avg arrival time ')
        st = input('enter searvice time ')
        qt = input('enter quantum')
        at = float(at)
        st= float(st)
        qt = float(qt)
        roundRobin(st,at,qt,1)

    
      elif(schul == 3):
        at = input('enter avg arrival time ')
        st = input('enter searvice time ')
        at = float(at)
        st= float(st)
        strf(st,at,1)
  
      elif(schul == 4):
        at = input('enter avg arrival time ')
        st = input('enter searvice time ')
        at = float(at)
        st= float(st)
        hrrn(st,at,1)

    elif(todo ==3):
      done=True  

    else:
      print('could not do request please try again')

if __name__ == "__main__":
    main()