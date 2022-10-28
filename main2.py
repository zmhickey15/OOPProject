def strf2(lamService, lamArrival):
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
  print(event1.time)
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
            print(nextDepart.type)
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
          
  print(clockTime)
  genReport(finishedProcesses, clockTime)

  return