import queue as Q
import sys


def video_parser(fileName):
    # list of V1,..,VN-1 - MB per video
    # list of Ld0,...Ldn-1 - milli
    # Mec Ei, Cj -> Latency between endpoint and cache or -1 in milli
    # Rev -> number of requests for this video from this endpoint. (int)
    with open(fileName) as f:
        content = f.readlines()
    V, E, R, C, X = content[0].split()
    V = int(V)
    E = int(E)
    R = int(R)
    C = int(C)
    X = int(X)
    content = content[1:]
    videos = content[0].split()
    videos = [int(i) for i in videos]
    content = content[1:]
    Ldarr = []
    Mec = [[-1 for c in range(C)] for e in range(E)]
    jjj =0
    for i in range(E):
        Ld, K = content[jjj].split()
        Ld = int(Ld)
        K = int(K)
        Ldarr.append(Ld)
        jjj+=1
        for j in range(K):
            c, Lc = content[jjj].split()
            c = int(c)
            Lc = int(Lc)
            Mec[i][c] = Lc
            jjj += 1
            if j%100 == 0 : print(j,"/",K)
    Rev = [[0 for v in range(V)] for i in range(E)]
    for i in range(R):
        Rv, Re, Rn = content[jjj+i].split()
        Rv = int(Rv)
        Re = int (Re)
        Rn = int(Rn)
        Rev[Re][Rv] = Rn
        if i%100 == 0: print(i,"/",R)
    print("PARSER DONE")
    return V, E, R, C, X, videos, Ldarr, Mec, Rev



def sol(numberOfVideos,numberOfEndPoints,numberOfRequests,numberOfServers,serverSize,VideoSize,ServerLatency,Mec,RequestMatrix):
    #serverSize = 100
    #numberOfServers = 3
    #numberOfVideos = 5

    #RequestMatrix = [[0,1000,0,1500,500],[1000,0,0,0,0]]
    #ServerLatency = [1000,500]
    #VideoSize = [50,50,80,30,100]
    pq = Q.PriorityQueue()
    #Mec = [[100,200,300],[-1,-1,-1]]
    max = 0
    progress = 0
    for e in range(len(RequestMatrix)):
        for v in range(len(RequestMatrix[0])):
            if RequestMatrix[e][v] == 0 :continue
            for c in range(len(Mec[e])):
                ecLatency = Mec[e][c]

                if ecLatency == -1:continue
                score = RequestMatrix[e][v]*(ServerLatency[e]-ecLatency)
                if score < max/10:continue
                if score>max : max = score

                myTuple = (-score,e,v,c)
                #print(myTuple)
                pq.put(myTuple)
                progress += 1
                #if progress%5000 == 0 :print(progress%5000)
    solution = dict()
    accessEV = dict()
    print("-----------")
    for c in range(numberOfServers):
        solution[c] = (serverSize,list())
    for e in range(numberOfVideos):
        accessEV[e] = list()
    count = 0
    while not pq.empty():
        p,e,v,c = pq.get()
        #print(p,"e=",e,"v=",v,"c=",c)
        #print(solution[c])
       #print(solution[c][0]>VideoSize[v] , e not in solution[c][1] , v not in accessEV[e])
        if solution[c][0]>VideoSize[v] and e not in solution[c][1] and v not in accessEV[e]:
            if v not in solution[c][1]:
                solution[c] = (solution[c][0] - VideoSize[v],solution[c][1]+[v])
            accessEV[e].append(v)
            count += 1
            print("added",count)
    #print("DANNY")
    return solution

def output(solution):
    counter = 0
    for i in solution:
        if len(solution[i][1]) != 0:
            counter += 1
    print("-------------------")
    print(counter)
    for i in solution:
        if len(solution[i][1]) != 0:
            sol = [str(x) for x in solution[i][1] ]
            print(i, ' '.join(sol))


output(sol(*video_parser("kittens.in")))


