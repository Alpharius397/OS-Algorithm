import copy
import heapq

# just initialize the class
# page = Page()      Page Replacement Algorithm
# process = processScheduling()   Process Scheduling Algorithm

class Page():
    def __init__(self,frame:int = 0,queue:list[int] = []) -> None:
        self.frame = frame 
        self.queue = queue
        self.interface()
    
    def fifo(self) -> dict[str,int]:
        frames = []
        ans={'hit':0,'fault':0}
        for i in self.queue:
            if i in frames:
                ans['hit']+=1
                status='Hit'
            elif len(frames)<self.frame:
                ans['fault']+=1
                frames.append(i)
                status="Fault"
            else:
                frames.pop(0)
                ans['fault']+=1
                frames.append(i)
                status="Fault"
            self.display(frames,i,status)
        return ans

    def lru(self) -> dict[str,int]:
        frames = []
        ans={'hit':0,'fault':0}
        for i in self.queue:
            if i in frames:
                ans['hit']+=1
                frames.append(frames.pop(frames.index(i)))
                status='Hit'

            elif len(frames)<self.frame:
                ans['fault']+=1
                status="Fault"
                frames.append(i)
            else:
                frames.pop(0)
                ans['fault']+=1
                status="Fault"
                frames.append(i)
            self.display(frames,i,status)
        return ans
    
    def optimal(self) -> dict[str,int]:
        map={i: [k+1 for k,j in enumerate(self.queue) if j is i] for i in set(self.queue)}
        frames = []
        status="Fault"
        ans={'hit':0,'fault':0}
        for i in self.queue:
            
            if i in frames:
                ans['hit']+=1
                status='Hit'

            elif len(frames)<self.frame:
                ans['fault']+=1
                status="Fault"
                frames.append(i)
            else:
                lastOccur = max({f:map[f] for f in frames},key=lambda x:map[x][0] if map[x] else float('inf'))
                frames.remove(lastOccur)
                ans['fault']+=1
                frames.append(i)
                status="Fault"
            map[i].pop(0)
            self.display(frames,i,status)
        return ans
    
    def display(self,frames:list[int],current:int,status:str) -> None:
        print(f' {current} => {[frames[i] if i<len(frames) else None for i in range(self.frame)]} {status}')

    def interface(self) -> None:
        self.frame = int(input(' Enter the number of frames: '))
        self.queue = [int(i) for i in input(' Enter the refernce string: ').split()]
        print()
        choice=-1
        while choice!=4:
            print(' 1) FIFO Algorithm \n 2) LRU Algorithm \n 3) Optimal Algorithm \n 4) Exit \n',end='')
            choice=int(input(' Enter your Choice: '))
            if choice==1:
                ans = self.fifo()
                print(f' Page Hit = {ans['hit']} and Page Fault = {ans['fault']}')
            elif choice==2:
                ans = self.lru()
                print(f' Page Hit = {ans['hit']} and Page Fault = {ans['fault']}')
            elif choice==3:
                ans = self.optimal()
                print(f' Page Hit = {ans['hit']} and Page Fault = {ans['fault']}')
            elif choice==4:
                print(' Exiting....')
            else:
                print(' Incorrect Choice!')
            print()

class Memory():
    def __init__(self,parts:list[float]=[],tasks:dict[str,float]={}) -> None:
        self.parts = parts
        self.tasks = tasks

class processScheduling():
    def __init__(self) -> None:
        self.interface()

    def display(self,counter:int,curr:int,times:int) -> None:
        for i in range(counter,counter+times):
            self.counter.append(f'P{curr}' if curr!='NULL' else f'{curr}')
        print(f' Counter = {counter}: {self.counter}')


    def FCFS(self) -> dict[int,dict[str,int]]:
        counter=0
        task = sorted(self.task,key=lambda x: self.task[x]['arrive'])
        task = [self.task[i] for i in task]
        task[0]['wait'] = 0
        task[0]['TAT'] = task[0]['burst']
        counter+=task[0]['burst']
        self.display(counter=counter,curr=task[0]['index'],times=task[0]['burst'])
        
        for i in range(1,len(task)):
            if counter>=task[i]['arrive']:
                counter+=task[i]['burst']
                task[i]['wait'] = task[i-1]['TAT']
                task[i]['TAT'] = task[i]['wait'] + task[i]['burst']
                self.display(counter=counter,curr=task[i]['index'],times=task[i]['burst'])
            else:
                counter+=1
                self.display(counter,curr='NULL',times=1)
        
        task = {task[i]['index']:task[i] for i in range(len(task))}
        self.process(task)
        return task
    
    def taskThere(self,task:dict[int,dict[str,int]],counter:int,queue:dict[int,list[int]],minheap:list[int]) -> None:
        for i in task:
            if task[i]['arrive']==counter:
                heapq.heappush(minheap,task[i]['burst'])
                if task[i]['burst'] not in queue:
                    queue[task[i]['burst']] = []
                queue[task[i]['burst']].append(i)

    def SJF(self) -> dict[int,dict[str,int]]:
        counter = 0
        task = sorted(self.task,key=lambda x: (self.task[x]['arrive'],self.task[x]['burst'],x))
        task = {i:self.task[i] for i in task}
        minheap = []
        done = 0
        queue={}
        while done<len(task):
            self.taskThere(task,counter,queue,minheap)
            val = heapq.heappop(minheap) if minheap else False
            counter+=1
            if not val: continue
            curr = queue[val].pop(0)

            task[curr]['burst'] -= 1

            if task[curr]['burst']==0:
                task[curr]['TAT'] = counter - task[curr]['arrive']
                task[curr]['wait'] = task[curr]['TAT'] - task[curr]['org']
                done+=1
                continue

            heapq.heappush(minheap,task[curr]['burst'])

            if task[curr]['burst'] not in queue: 
                queue[task[curr]['burst']] = []
            queue[task[curr]['burst']].append(curr)

        self.process(task)
        return task
    
    def checkTask(self,counter:int,task:dict[int,dict[str,int]],queue:list[int],completed:list[int]) -> None:
        for i in task:
            if task[i]['arrive']<=counter and i not in queue and i not in completed:
                queue.append(i)

    def RoundRobin(self,quantum:int) -> dict[int,dict[str,int]]:
        print(quantum)
        counter = 0
        completed = []
        queue = []
        done=0
        task = sorted(self.task,key=lambda x: (self.task[x]['arrive']))
        task = {i:self.task[i] for i in task}

        while done<len(task):
            self.checkTask(counter,task,queue,completed)
            curr = queue.pop(0) if queue else float('inf')
            
            if curr==float('inf'): 
                counter+=1
                continue

            if task[curr]['burst']<=quantum:
                counter+=task[curr]['burst']
                task[curr]['burst'] = 0
                completed.append(curr)
                task[curr]['TAT'] = counter - task[curr]['arrive']
                task[curr]['wait'] = task[curr]['TAT'] - task[curr]['org']
                done+=1
                continue

            counter+=quantum
            task[curr]['burst'] -= quantum

        self.process(task)
        return task
    
    def process(self,task:dict[int,dict[str,int]]) -> None:
        print()
        processes = {i:task[i] for i in sorted(task)}
        for i in processes:
            print(f' Proccess P{i}: Total Waiting Time={processes[i]['wait']},Total Turnaround Time={processes[i]['TAT']}')
        print()

    def Average(self,task:dict[int,dict[str,int]]) -> dict[str,float]:
        wait,tat=0,0
        for i in task:
            wait+=task[i]['wait']
            tat+=task[i]['TAT']
        return {'wait':float(wait)/len(task),'TAT':float(tat)/len(task)}

    def interface(self) -> None:
        self.arrive = [int(i) for i in input(' Enter the arrival time: ').split()]
        self.burst = [int(i) for i in input(' Enter the burst time: ').split()]
        print()
        try:
            self.task = {i:{'index':i,'arrive':self.arrive[i],'burst':self.burst[i],'org':self.burst[i],'wait':0,'TAT':0} for i in range(max(len(self.arrive),len(self.burst)))}
            self.org = copy.deepcopy(self.task)
            self.counter = []
        except:
            print('\n Length of the arrive and burst is different!')
        else:
            data = [f' Process P{i}: Arrive={self.task[i]['arrive']}, Burst={self.task[i]['burst']}.' for i in self.task]
            for i in data:
                print(i)
            choice=-1
            while choice!=4:
                print('\n 1) FCFS Algorithm \n 2) SJF Algorithm \n 3) Round Robin Algorithm \n 4) Exit \n',end='')
                choice=int(input(' Enter your Choice: '))
                if choice==1:
                    print()
                    res = self.Average(self.FCFS())
                    print(f' Average Waiting Time = {res['wait']:0.2f} and Average Turnaround Time = {res['TAT']:0.2f}')
                    self.task = self.org
                elif choice==2:
                    res = self.Average(self.SJF())
                    print(f' Average Waiting Time = {res['wait']:0.2f} and Average Turnaround Time = {res['TAT']:0.2f}')
                    self.task = self.org
                elif choice==3:
                    quantum = int(input(' Enter the time quantum: '))
                    res = self.Average(self.RoundRobin(quantum))
                    print(f' Average Waiting Time = {res['wait']:0.2f} and Average Turnaround Time = {res['TAT']:0.2f}')
                    self.task = self.org
                elif choice==4:
                    print(' Exiting....')
                else:
                    print(' Incorrect Choice!')








               
