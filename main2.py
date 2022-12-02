


done = False
while (not done):
  todo= input( 'to create file with data for simulations press: 1 \nto run a custom simulation press: 2 \nto end program enter 3\n')
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
    schul = input('for FCFS enter: 1 \n for RR enter: 2 \n for STRF enter: 3 \n for HRRN enter 4\n' )
    schul =int(schul)
    if(schul == 1):
      at = input('enter avg arrival time ')
      st = input('enter searvice time')
      at = int(at)
      st= int(st)
      fcfs(st,at,1)

    elif(schul == 2):
      at = input('enter avg arrival time ')
      st = input('enter searvice time')
      qt = input('enter quantum')
      at = int(at)
      st= int(st)
      qt = int(qt)
      roundRobin(st,at,qt,1)

    
    elif(schul == 3):
      at = input('enter avg arrival time ')
      st = input('enter searvice time')
      at = int(at)
      st= int(st)
      strf(st,at,1)
  
    elif(schul == 4):
      at = input('enter avg arrival time ')
      st = input('enter searvice time')
      at = int(at)
      st= int(st)
      hrrn(st,at,1)

  elif(todo ==3):
    done=True  

  else:
    print('could not do request please try again')

    