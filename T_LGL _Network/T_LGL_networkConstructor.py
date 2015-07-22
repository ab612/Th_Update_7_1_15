#Madison Soden
#6/19/15 created
#Notation Updates and oppositenodes function added 7/07/15
#7/13/15  corrections w/ Jorge
#7/14/15 added inputCNodes function, deleted the semicolons I keep putting every where for continuitys sake, and added opposite coposit node removal for cycle network

# Optional print data checks are commented using '''
# Explantiroy comments are comented with #

# On Notation:
# Node IDs are recorded as strings of numbers: 
# - normal nodes are integers with their negations being represented as the negative of the Node ID
#                                 i.e. nodes V and ~V could be represented as 1 and -1 respectivly
# - composit node IDs are represented as decimal #s that do not corrispond to the Node IDs of their parent Nodes
#                  i.e. node A's ID could be 1 and nodee B's ID could be 2 with composit node AB's ID being 12.5
# - composite node IDs  are only ever positive decimal #s

import networkx as nx
import math 
import sets

stabelMotifs=[]
            
# in progress function to identifie opposit nodes in cycle networks
def oppositenodes(C,cnode1,cnode2,cyclesdict):
    oppnodes=False;
    cyc1=cyclesdict[cnode1]
    cyc2=cyclesdict[cnode2]
    for n in cyc1:
        for m in cyc2:
            if float(n) == (-1*float(m)):
                oppnodes=True
                break
        if oppnodes: break
    return oppnodes


#finds inputs of a composit nodes, inode is a list of incoming edges

def inputCNodes(G,g):
   # for g in G.nodes():
        #print g
        if(float(g)!=math.floor(float(g))):
            innod=G.in_edges(g)
            return innod

def opositeCnodes(C,G,cnode1, cnode2,cyclesdict):
    oppnodes=False;
    cyc1=cyclesdict[cnode1]
    cyc2=cyclesdict[cnode2]
    for n in cyc1:
        if(float(n)!=math.floor(float(n))):
            inputn = inputCNodes(G,n)
            for m in cyc2:
                if(float(m)!=math.floor(float(m))):                    
                    inputm = inputCNodes(G,m)
                    for m1 in inputm:
                        for n1 in inputn:
                            if float(n1[0]) == (-1*float(m1[0])):
                              oppnodes=True
                              break  
                        if oppnodes: break
                    if oppnodes: break
                else:
                    for n1 in inputn:
                            if float(n1[0]) == (-1*float(m)):
                              oppnodes=True
                              break
            if oppnodes: break
        if oppnodes: break
    return oppnodes

def oppositExpanNodes(G, node1, node2):
    oppnodes=False;
    if(float(node1)!=math.floor(float(node1))):
        inputn = inputCNodes(G,node1)
        if(float(node2)!=math.floor(float(node2))):                    
            inputm = inputCNodes(G,node2)
            for m1 in inputm:
                for n1 in inputn:
                    if float(n1[0]) == (-1*float(m1[0])):
                      oppnodes=True
                      return oppnodes  
        else:
            for n1 in inputn:
                if float(n1[0]) == (-1*float(node2)):
                    oppnodes=True
                    return oppnodes
    return oppnodes

#cn is a list of all the elements within possible cycles

def isStableMotif(C,G,cn,cyclesdict):
    isSM=True
    setcn=set(cn)
    for x in range(len(cn)):
       if (float(cn[x])!=math.floor(float(cn[x]))):
           ieofx = G.in_edges(cn[x])
           ###check for parent edges contained w/i the stable moti
           for e in ieofx:
               if not (setcn.__contains__(e[0])):
                   isSM = False
                   return isSM 
           for y in range(x+1, len(cn)):
                if oppositExpanNodes(G, cn[y], cn[x]):
                    isSM = False
                    return isSM        
       elif (float(cn[x])==math.floor(float(cn[x]))):
            for y in range(x+1, len(cn)):
                if (float(cn[y])!=math.floor(float(cn[y]))):
                    if oppositExpanNodes(G, cn[y], cn[x]):
                        isSM = False
                        return isSM
                else:
                    if (cn[x] == -1*cn[y]):
                        isSM = False
                        return isSM 
      
    if isSM:
        print cn,
    return isSM
        
def redundantCnodeReduction(C, cyclesdict):
    removeC =set()
    for cn1 in range(len(C.nodes())):
        if isStableMotif(C,G,cyclesdict[C.nodes()[cn1]],cyclesdict):
            stabelMotifs.append(C.nodes()[cn1])
            cyc1=cyclesdict[C.nodes()[cn1]]
            s1=set(cyc1)
            for cn2 in range(cn1+1,len(C.nodes())): 
                cyc2=cyclesdict[C.nodes()[cn2]]
                s2=set(cyc2)
                if(len(s1)<len(s2)):
                    if s1.issubset(s2):
                        #stabelMotifs.append(C.nodes()[cn1])
                        removeC.add(C.nodes()[cn2])
                        removeC.add(C.nodes()[cn1])
    C.remove_nodes_from(list(removeC))
    
# "TH_node_names" is written NodNumber(i.e identifier) \t NodName(i.e. the actual protien or whatever) \n
# reading in "TH_node_names as a string name
f = open("TLGLNetwork_names.txt", "r")
name=f.read()
f.close()

#creating a nodname list of the form names[NodNumber][protien name or whatever]
names=name.split('\n')
lines=[]
for line in names:
    lines.append(line.split("\t"))  
    
    
#"TH_adjacency list is written NodeNumber \t downstream NodNumbers (spererated by \t) \n
#creating a adjacency list adjlist[NodNumber][Downstreaam NodeNumbers]
fadf=open("TLGLNetwork_adjlist.txt", "r")
adjlist=[]
fad=fadf.read().split("\n")
fadf.close()
for line in fad:
    adjlist.append(line.split("\t"))
  
    
# creating a directed network G as the network of Nodes
G=nx.DiGraph()

#creating Nodes in node network with string(node ID attribute) 
# and string(nodename atribute) 
for line in lines:
    G.add_node(line[0],nodname=line[1])

#for all node IDs in adjacencey list
for line in adjlist:
    # add each downstream connection to adjacent Node IDs
    for i in range(len(line)-1):
        G.add_edge(line[0], line[i+1])
        
'''for g in G.nodes():
    #print g, nx.get_node_attributes(G, 'nodname')[g]'''
        
nx.write_gml(G, "TLGL_nodeNetwork.gml")


#end node network creation 
#start Cycle network creation


#Opens Cycle Network file, creats a list lines of line, line is in turn a list of strings 
# from the Cycle Network file where [0] is the cycle node name and [1:] are the unordered nodes contained w/i that cycle
fcy=open("TLGLNetwork_cycles.txt", "r")
cycles=fcy.read()
fcy.close()

lines=[]
for line in cycles.split('\n'):
    lines.append(line.split("\t"))

# creates undirected cycle network
C=nx.Graph()
#The export feature wasn't liking us putting the cycles as a node attribute, so I just created a separate dictionary for it
#I also replaced all instances of "nx.get_node_attributes(C, 'cycles')" with "cycles", which should do the job
cyclesdict={}

# declares a cycle node for each line in lines, delets the cycle node data from each line and then renames each line cycles 
# bc that is the data they still contain
for line in lines:
    node=line[0]
    cycledict=line
    cycledict.remove(node)
    #ands a cycle node with the attribute of having its list of network nodes
    C.add_node(node)
    cyclesdict[node]=line
   # print node,line

dic={}
#creates a dictionary for each expanded node in  each cycle node
for c in C.nodes():
    '''print c, cycles[c]'''
    for expnode in cyclesdict[c]:
        if(float(expnode)!= math.floor(float(expnode))):
            dic[expnode]=[]

# assigns a cycle node for each expanded node
for c in C.nodes():
    '''print c, cycles[c]'''
    for expnode in cyclesdict[c]:
        if(float(expnode)!=math.floor(float(expnode))):
            current=dic[expnode]
            current.append(c)
            dic[expnode]=current

#doing complicated stuff to print expanded node, it's inputs and then a list of cycles containg those inputs 

for key in  dic.keys():
    cycnodes=dic[key]
    inputs=G.in_edges(key)
    print "INPUT",key,inputs
    for cnode1 in  range(len(cycnodes)):    
        cyc1=cyclesdict[cycnodes[cnode1]]    
        for cnode2 in  range(len(cycnodes)):
            if(cnode2>cnode1):            
                cyc2=cyclesdict[cycnodes[cnode2]]   
                #print "cyc1",cycnodes[cnode1],cyc1
                #print "cyc2",cycnodes[cnode2],cyc2            
                inters1=[]
                inters2=[]
                trueboth=True               
                for input in inputs:
                    true1=cyc1.__contains__(input[0])
                    true2=cyc2.__contains__(input[0])
                    if(true1): inters1.append(input[0])
                    if(true2): inters2.append(input[0])
                    trueboth=((true1 and true2) or (not true1 and not true2)) and trueboth
                if(len(inters1)!=len(inters2)): C.add_edge(cycnodes[cnode1], cycnodes[cnode2]); #print "NODE",cycnodes[cnode2],cycnodes[cnode1]             
                elif(len(inters1)==len(inters2) and trueboth): C.add_edge(cycnodes[cnode1], cycnodes[cnode2]); #print "NODE",cycnodes[cnode2],cycnodes[cnode1]

#removing edges that connect cycles with opposite nodes            
edgesremove=[]
for e in C.edges():
    cnode1=e[0]
    cnode2=e[1]
    if oppositenodes(C,cnode1,cnode2,cyclesdict):
        edgesremove.append(e)
C.remove_edges_from(edgesremove);

#removing edges that connect cycles with opposite composit nodes
edgesremove1=[]
for e in C.edges():
     cnode1=e[0]
     cnode2=e[1]
     if opositeCnodes(C,G,cnode1, cnode2,cyclesdict):
         edgesremove1.append(e)
C.remove_edges_from(edgesremove1)
'''
for v in C.nodes():
    if(isStableMotif(C, G, cyclesdict[v], cyclesdict)):
        print v, cyclesdict[v]
        stabelMotifs.append(v)'''
redundantCnodeReduction(C, cyclesdict)

#check for double cycle stable motifs    
'''for e in C.edges():
    v1 =e[0]
    v2 =e[1]
    listofcyclelist=[]
    v = list(set(cyclesdict[v1] + cyclesdict[v2])) 
    if isStableMotif(C, G, v, cyclesdict):
        cycleList = (v1, v2)
        listofcyclelist.append(cycleList)
        
C.remove_edges_from(listofcyclelist)
for c in listofcyclelist:
    stabelMotifs.append(c)        '''
    
nx.write_gml(C, "TLGL_cycleNetwork_removedCedes.gml")
setM=set(stabelMotifs)
print(list(setM))
    
print('Ding')
 