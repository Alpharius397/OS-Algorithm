# Just initialize the class Page() : for page replacement algorithm or processScheduling() : for process scheduling or diskScheduling() : disk scheduling
# page = Page()
# process = processScheduling()
# disk = diskScheduling()
from bisect import bisect_right
from collections import defaultdict
import copy
import heapq

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
        print(f" {current} => {[frames[i] if i<len(frames) else None for i in range(self.frame)]} {status}")

    def interface(self) -> None:
        self.frame = int(input(' Enter the number of frames: '))
        self.queue = [int(i) for i in input(' Enter the refernce string: ').split()]
        choice=-1

        while choice!=4:
            print('\n 1) FIFO Algorithm \n 2) LRU Algorithm \n 3) Optimal Algorithm \n 4) Exit \n',end='')
            choice=int(input(' Enter your Choice: '))

            if choice==1:
                ans = self.fifo()
                print(f" Page Hit = {ans['hit']} and Page Fault = {ans['fault']}")

            elif choice==2:
                ans = self.lru()
                print(f" Page Hit = {ans['hit']} and Page Fault = {ans['fault']}")

            elif choice==3:
                ans = self.optimal()
                print(f" Page Hit = {ans['hit']} and Page Fault = {ans['fault']}")     

            elif choice==4:
                print(' Exiting....')

            else:
                print(' Incorrect Choice!')

"""
class Memory():
    def __init__(self,parts:list[int]=[],tasks:dict[str,int]={}) -> None:
        self.parts = parts
        self.tasks = tasks

    def firstFit(self) -> None:
        notAlloc = [i for i in self.parts]
        for i in self.tasks:
            for j in notAlloc:
                if self.parts[j]<=self.tasks[i]:
                    self.tasks[i] -= self.parts[j]
                    self.parts[j]['allocated'] = i
                    notAlloc.remove(j)
        return self.parts
"""""

class processScheduling():
    def __init__(self) -> None:
        self.interface()

    def display(self,counter:int,curr:int,times:int) -> None:
        for i in range(counter,counter+times):
            self.counter.append(f"P{curr}" if curr!='NULL' else f"{curr}")

        print(f' Counter = {counter}: {self.counter}')


    def FCFS(self) -> dict[int,dict[str,int]]:
        counter, task = 0, [self.task[i] for i in sorted(self.task,key=lambda x: self.task[x]['arrive'])]
        task[0]['wait'], task[0]['TAT'] = 0, task[0]['burst']
        counter += task[0]['burst']

        self.display(counter=counter,curr=task[0]['index'],times=task[0]['burst'])
        
        for i in range(1,len(task)):
            if counter>=task[i]['arrive']:
                counter+=task[i]['burst']
                task[i]['wait'], task[i]['TAT'] = task[i-1]['TAT'], task[i]['wait'] + task[i]['burst']
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
        counter, task = 0, {i:self.task[i] for i in sorted(self.task,key=lambda x: (self.task[x]['arrive'],self.task[x]['burst'],x))}
        minheap, done, queue = [], 0, {}

        while done<len(task):
            self.taskThere(task,counter,queue,minheap)
            val = heapq.heappop(minheap) if minheap else False
            counter+=1

            if not val: 
                self.display(counter,'NULL',1)
                continue

            curr = queue[val].pop(0)
            self.display(counter,curr,1)
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
            if (task[i]['arrive']<=counter) and (i not in queue) and (i not in completed):
                queue.append(i)

    def RoundRobin(self,quantum:int) -> dict[int,dict[str,int]]:
        done,counter,completed,queue = 0, 0, [], []
        task = {i:self.task[i] for i in sorted(self.task,key=lambda x: (self.task[x]['arrive']))}

        while done<len(task):
            self.checkTask(counter,task,queue,completed)
            curr = queue.pop(0) if queue else float('inf')
            
            if curr==float('inf'): 
                counter+=1
                self.display(counter,'NULL',1)
                continue
            
            if task[curr]['burst']<=quantum:
                counter+=task[curr]['burst']
                self.display(counter,curr,task[curr]['burst'])
                task[curr]['burst'], task[curr]['TAT'] = 0, counter - task[curr]['arrive']
                task[curr]['wait'] = task[curr]['TAT'] - task[curr]['org']
                completed.append(curr)
                done+=1
                continue

            counter+=quantum
            self.display(counter,curr,quantum)
            task[curr]['burst'] -= quantum

        self.process(task)
        return task
    
    def process(self,task:dict[int,dict[str,int]]) -> None:
        print()
        processes = {i:task[i] for i in sorted(task)}
        for i in processes:
            print(f" Proccess P{i}: Total Waiting Time={processes[i]['wait']},Total Turnaround Time={processes[i]['TAT']}")
        print()

    def Average(self,task:dict[int,dict[str,int]]) -> dict[str,float]:
        wait, tat = 0, 0
        for i in task:
            wait += task[i]['wait']
            tat += task[i]['TAT']

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
            for i in self.task:
                print(f" Process P{i}: Arrive={self.task[i]['arrive']}, Burst={self.task[i]['burst']}.")

            choice=-1

            while choice!=4:
                print('\n 1) FCFS Algorithm \n 2) SJF Algorithm \n 3) Round Robin Algorithm \n 4) Exit \n',end='')
                choice=int(input(' Enter your Choice: '))
                print()

                if choice==1:
                    res = self.Average(self.FCFS())
                    self.task = copy.deepcopy(self.org)
                    print(f" Average Waiting Time = {res['wait']:0.2f} and Average Turnaround Time = {res['TAT']:0.2f}")
                    self.counter = []

                elif choice==2:
                    res = self.Average(self.SJF())
                    self.task = copy.deepcopy(self.org)
                    print(f" Average Waiting Time = {res['wait']:0.2f} and Average Turnaround Time = {res['TAT']:0.2f}")
                    self.counter = []

                elif choice==3:
                    quantum = int(input(' Enter the time quantum: '))
                    res = self.Average(self.RoundRobin(quantum))
                    print(f" Average Waiting Time = {res['wait']:0.2f} and Average Turnaround Time = {res['TAT']:0.2f}")
                    self.task = copy.deepcopy(self.org)
                    self.counter = []

                elif choice==4:
                    print(' Exiting....')

                else:
                    print(' Incorrect Choice!')

class diskScheduling():
    def __init__(self) -> None:
        self.interface()
    def dist(self,prev:int,next:int) -> int:
        return abs(prev - next)
    
    def fcfs(self) -> dict[int,list[int]]:
        queue,dis,head = [self.head], 0, self.head

        for i in self.request:
            dis += self.dist(head,i)
            head = i
            queue.append(i)

        return {'total':dis, 'request':queue}
    
    def sstf(self) -> dict[int,list[int]]:
        queue,dis=[self.head], 0

        temp = sorted(self.request + [self.head])
        index = temp.index(self.head)

        while len(temp)>1:
            head = temp.pop(index)
            
            if index==0:
                dis += self.dist(head,temp[index])
            
            elif index==(len(temp)):
                dis += self.dist(head,temp[index-1])
                index-=1
            
            else:
                l,r = temp[index-1], temp[index]

                if abs(head - l) < abs(head - r):
                    dis += self.dist(head,l)
                    index-=1
                else:
                    dis += self.dist(head,r)
            
            head = temp[index]
            queue.append(head)
        
        return {'total':dis, 'request':queue}
    
    def scan(self) -> dict[str,dict[int,list[int]]]:
        lqueue,ldis,rqueue,rdis = [self.head], 0, [self.head], 0
        temp = sorted(self.request)
        index = bisect_right(temp,self.head)

        ldis = self.dist(0,self.head) + self.dist(0,temp[-1])
        lqueue = [self.head] + temp[:index][::-1] + [0] + temp[index:]

        rdis = self.dist(self.diskEnd,self.head) + self.dist(self.diskEnd,temp[0])
        rqueue = [self.head] + temp[index:] + [self.diskEnd] + temp[:index][::-1] 

        return {'left':{'total':ldis, 'request':lqueue}, 'right':{'total':rdis, 'request':rqueue}}        
    

    def look(self) -> dict[str,dict[int,list[int]]]:
        temp = sorted(self.request)
        index = bisect_right(temp,self.head)

        ldis = self.dist(temp[0],self.head) + self.dist(temp[0],temp[-1])
        lqueue = [self.head] + temp[:index][::-1] + temp[index:]

        rdis = self.dist(temp[-1],self.head) + self.dist(temp[-1],temp[0])
        rqueue = [self.head] + temp[index:] + temp[:index] 

        return {'left':{'total':ldis, 'request':lqueue}, 'right':{'total':rdis, 'request':rqueue}} 

    def Cscan(self) -> dict[str,dict[int,list[int]]]:
        temp = sorted(self.request)
        index = bisect_right(temp,self.head)

        ldis = self.dist(0,self.head) + self.diskEnd + self.dist(self.diskEnd,temp[index])
        lqueue = [self.head] + temp[:index][::-1] + [0,self.diskEnd] + temp[index:][::-1]

        rdis = self.dist(self.diskEnd,self.head) + self.diskEnd + self.dist(0,temp[index-1])
        rqueue = [self.head] + temp[index:] + [self.diskEnd,0]+ temp[:index] 

        return {'left':{'total':ldis, 'request':lqueue}, 'right':{'total':rdis, 'request':rqueue}}        
    

    def Clook(self) -> dict[str,dict[int,list[int]]]:
        temp = sorted(self.request)
        index = bisect_right(temp,self.head)

        ldis = self.dist(temp[0],self.head) + self.dist(temp[-1],temp[0]) + self.dist(temp[-1],temp[index])
        lqueue = [self.head] + temp[:index][::-1] + temp[index:][::-1]

        rdis = self.dist(temp[-1],self.head) + self.dist(temp[0],temp[-1]) + self.dist(temp[0],temp[index-1])
        rqueue = [self.head] + temp[index:] + temp[:index] 

        return {'left':{'total':ldis, 'request':lqueue}, 'right':{'total':rdis, 'request':rqueue}}   
      
    def interface(self) -> None:
        self.diskEnd = int(input(' Enter the disk size: ')) - 1

        if self.diskEnd<0:
            print(' Disk Size cannot be negative!')
            return 
        
        self.request = [int(i) for i in input(' Enter the request queue: ').split()]
        if min(self.request)<0 or max(self.request)>self.diskEnd:
            print(f' The requests are out of bound (0,{self.diskEnd})!')
            return
        self.head = int(input(' Enter the current head position: '))

        if self.head<0 or self.diskEnd>self.diskEnd:
            print(f' The head is out of bound (0,{self.diskEnd})!')
        print()
        choice=-1
        while choice!=7:
            print('\n 1) FCFS Disk Scheduling\n 2) SSTF Disk Scheduling\n 3) SCAN Disk Scheduling\n 4) LOOK Disk Scheduling\n 5) CSCAN Disk Scheduling\n 6) CLOOK Disk Scheduling\n 7) Exit from menu\n')
            choice=int(input(' Enter your choice: '))

            if choice==1:
                res = self.fcfs()
                print(f" Total Overhead Movement: {res['total']} and Request queue: {res['request']}")
            elif choice==2: 
                res = self.sstf()
                print(f" Total Overhead Movement: {res['total']} and Request queue: {res['request']}")
            elif choice==3:
                res = self.scan()
                print(f" Total Overhead Movement: Left-Side = {res['left']['total']} and Request queue: {res['left']['request']}, Right-Side = {res['right']['total']} and Request queue: {res['right']['request']}")
            elif choice==4:
                res = self.look()
                print(f" Total Overhead Movement: Left-Side = {res['left']['total']} and Request queue: {res['left']['request']}, Right-Side = {res['right']['total']} and Request queue: {res['right']['request']}")
            elif choice==5:
                res = self.Cscan()
                print(f" Total Overhead Movement: Left-Side = {res['left']['total']} and Request queue: {res['left']['request']}, Right-Side = {res['right']['total']} and Request queue: {res['right']['request']}")
            elif choice==6:
                res = self.Clook()
                print(f" Total Overhead Movement: Left-Side = {res['left']['total']} and Request queue: {res['left']['request']}, Right-Side = {res['right']['total']} and Request queue: {res['right']['request']}")
            elif choice==7:
                print(' Exiting....')
            else:
                print(' Invalid Choice!')

